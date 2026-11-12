# envios.py
"""Cálculo de costo de envío de EnvíaYa (v2.0.0, refactorizado).

Patrón Estrategia aplicado a los DESCUENTOS (cliente y cupón).
Reglas de negocio: D=1, E=0, B=1, F=4.
"""
from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP

# --------------------------------------------------------------------------
# Constantes de negocio
# --------------------------------------------------------------------------
LIMITE_TRAMO_1 = Decimal("3")        # kg (Regla D=1: el límite NO pertenece al tramo 1)
LIMITE_TRAMO_2 = Decimal("10")       # kg (el límite SÍ pertenece al tramo 2)
PESO_MAXIMO = Decimal("50")          # kg

TARIFA_TRAMO_1 = Decimal("6000")
TARIFA_TRAMO_2 = Decimal("9000")
COSTO_KG_ADICIONAL = Decimal("800")  # por kg sobre LIMITE_TRAMO_2

RECARGO_RURAL = Decimal("0.10")
RECARGO_NACIONAL = Decimal("0.45")
RECARGO_FINDE = Decimal("2000")      # Regla E=0: se suma ANTES de descuentos

DESCUENTO_FRECUENTE = Decimal("0.05")
DESCUENTO_VIP = Decimal("0.15")
DESCUENTO_CUPON_ENVIO10 = Decimal("0.10")

COSTO_MINIMO = Decimal("5000")
MULTIPLO_REDONDEO = Decimal("100")

DIA_SABADO = 6
DIA_DOMINGO = 7
DIA_MINIMO = 1
DIA_MAXIMO = 7

ZONA_URBANA = "urbana"
ZONA_RURAL = "rural"
ZONA_NACIONAL = "nacional"
RECARGOS_POR_ZONA = {
    ZONA_URBANA: Decimal("0"),
    ZONA_RURAL: RECARGO_RURAL,
    ZONA_NACIONAL: RECARGO_NACIONAL,
}

# Compatibilidad con el banco de pruebas existente
CONFIG = {
    "L1": int(LIMITE_TRAMO_1),
    "L2": int(LIMITE_TRAMO_2),
    "RECARGO_RURAL": float(RECARGO_RURAL),
    "RECARGO_NACIONAL": float(RECARGO_NACIONAL),
    "DESC_VIP": float(DESCUENTO_VIP),
    "RECARGO_FINDE": int(RECARGO_FINDE),
}


# --------------------------------------------------------------------------
# Patrón Estrategia: descuentos
# --------------------------------------------------------------------------
class EstrategiaDescuento(ABC):
    """Interfaz común de todas las estrategias de descuento."""

    @abstractmethod
    def aplicar(self, monto: Decimal) -> Decimal:
        """Devuelve el monto resultante tras aplicar el descuento."""


class DescuentoPorcentual(EstrategiaDescuento):
    """Base reutilizable para descuentos expresados como porcentaje."""

    def __init__(self, porcentaje: Decimal):
        self._porcentaje = porcentaje

    def aplicar(self, monto: Decimal) -> Decimal:
        return monto - monto * self._porcentaje


class SinDescuento(EstrategiaDescuento):
    def aplicar(self, monto: Decimal) -> Decimal:
        return monto


class DescuentoClienteFrecuente(DescuentoPorcentual):
    def __init__(self):
        super().__init__(DESCUENTO_FRECUENTE)


class DescuentoClienteVip(DescuentoPorcentual):
    def __init__(self):
        super().__init__(DESCUENTO_VIP)


class DescuentoCuponEnvio10(DescuentoPorcentual):
    def __init__(self):
        super().__init__(DESCUENTO_CUPON_ENVIO10)


ESTRATEGIAS_CLIENTE = {
    "normal": SinDescuento(),
    "frecuente": DescuentoClienteFrecuente(),
    "vip": DescuentoClienteVip(),
}

ESTRATEGIAS_CUPON = {
    "ENVIO10": DescuentoCuponEnvio10(),
}
# Regla F=4: un cupón inexistente se ignora.
ESTRATEGIA_CUPON_POR_DEFECTO = SinDescuento()


# --------------------------------------------------------------------------
# Validaciones (DEF-04 / DEF-05)
# --------------------------------------------------------------------------
def _validar_peso(peso) -> Decimal:
    if isinstance(peso, bool) or not isinstance(peso, (int, float, Decimal)):
        raise ValueError("peso invalido: debe ser numerico")
    peso_decimal = Decimal(str(peso))
    if not peso_decimal.is_finite() or peso_decimal <= 0 or peso_decimal > PESO_MAXIMO:
        raise ValueError(f"peso invalido: debe estar en (0, {PESO_MAXIMO}]")
    return peso_decimal


def _validar_zona(zona) -> str:
    if zona not in RECARGOS_POR_ZONA:
        raise ValueError(f"zona invalida: {zona!r}")
    return zona


def _validar_cliente(tipo_cliente) -> str:
    if tipo_cliente not in ESTRATEGIAS_CLIENTE:
        raise ValueError(f"tipo de cliente invalido: {tipo_cliente!r}")
    return tipo_cliente


def _validar_dia(dia) -> int:
    if isinstance(dia, bool) or not isinstance(dia, int) or not DIA_MINIMO <= dia <= DIA_MAXIMO:
        raise ValueError(f"dia invalido: debe ser entero entre {DIA_MINIMO} y {DIA_MAXIMO}")
    return dia


# --------------------------------------------------------------------------
# Métodos de apoyo
# --------------------------------------------------------------------------
def _calcular_tarifa_base(peso: Decimal) -> Decimal:
    """Tarifa por tramos de peso (Regla D=1: tramo 1 es peso < L1) (DEF-01)."""
    if peso < LIMITE_TRAMO_1:
        return TARIFA_TRAMO_1
    if peso <= LIMITE_TRAMO_2:
        return TARIFA_TRAMO_2
    return TARIFA_TRAMO_2 + (peso - LIMITE_TRAMO_2) * COSTO_KG_ADICIONAL


def _aplicar_recargo_zona(monto: Decimal, zona: str) -> Decimal:
    return monto + monto * RECARGOS_POR_ZONA[zona]


def _es_fin_de_semana(dia: int) -> bool:
    """Sábado (6) y domingo (7) (DEF-02)."""
    return dia >= DIA_SABADO


def _obtener_estrategia_cupon(cupon) -> EstrategiaDescuento:
    return ESTRATEGIAS_CUPON.get(cupon, ESTRATEGIA_CUPON_POR_DEFECTO)


def _redondear_comercial(monto: Decimal) -> int:
    """Redondea al múltiplo de 100 más cercano; la mitad sube (DEF-03)."""
    cientos = (monto / MULTIPLO_REDONDEO).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    return int(cientos * MULTIPLO_REDONDEO)


# --------------------------------------------------------------------------
# API pública
# --------------------------------------------------------------------------
def calcular_costo_envio(peso, zona, tipo_cliente, dia, cupon=None) -> int:
    """Calcula el costo final del envío en pesos (múltiplo de 100).

    Args:
        peso: kg, 0 < peso <= 50.
        zona: "urbana" | "rural" | "nacional".
        tipo_cliente: "normal" | "frecuente" | "vip".
        dia: entero 1 (lunes) a 7 (domingo).
        cupon: código opcional; si no existe se ignora.

    Raises:
        ValueError: si peso, zona, tipo_cliente o dia son inválidos.
    """
    peso_valido = _validar_peso(peso)
    zona_valida = _validar_zona(zona)
    cliente_valido = _validar_cliente(tipo_cliente)
    dia_valido = _validar_dia(dia)

    costo = _calcular_tarifa_base(peso_valido)
    costo = _aplicar_recargo_zona(costo, zona_valida)
    if _es_fin_de_semana(dia_valido):
        costo += RECARGO_FINDE

    # Regla B=1: se aplican ambos descuentos (cliente y cupón)
    costo = ESTRATEGIAS_CLIENTE[cliente_valido].aplicar(costo)
    costo = _obtener_estrategia_cupon(cupon).aplicar(costo)

    costo = max(costo, COSTO_MINIMO)
    return _redondear_comercial(costo)


def calc(p, z, c, d, cup=None):
    """Alias de compatibilidad (sin el argumento flag, eliminado)."""
    return calcular_costo_envio(p, z, c, d, cup)
