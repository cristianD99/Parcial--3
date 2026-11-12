# test_envios.py
import pytest
from envios import calc, CONFIG

# ==============================================================================
# BANCO DE CASOS DE PRUEBA DE CAJA NEGRA (Código Estudiantil: 0182410104)
# Parámetros: PMAX=50, L1=3, L2=10, RR=0.10, RN=0.45, VIP=0.15, FINDE=2000
# ==============================================================================

# 16 Casos Válidos (esperan un resultado numérico exacto)
CASOS_VALIDOS = [
    # (caso_id, peso, zona, cliente, dia, cupon, esperado)
    ("CP01", 2.5, "urbana", "normal", 3, None, 6000),
    ("CP02", 5, "rural", "frecuente", 6, "ENVIO10", 10200),
    ("CP03", 12, "nacional", "vip", 7, None, 14800),
    ("CP07", 3, "urbana", "normal", 1, None, 9000),
    ("CP08", 10, "rural", "normal", 5, None, 9900),
    ("CP09", 50, "nacional", "frecuente", 2, "ENVIO10", 50800),
    ("CP10", 2.9, "urbana", "vip", 4, None, 5100),
    ("CP11", 3.1, "rural", "frecuente", 6, None, 11300),
    ("CP12", 9.9, "nacional", "normal", 7, None, 15100),
    ("CP13", 10.1, "urbana", "normal", 1, None, 9100),
    ("CP14", 25, "urbana", "normal", 3, "XYZ", 21000),
    ("CP15", 8, "rural", "normal", 2, None, 9900),
    ("CP16", 15, "nacional", "frecuente", 6, "ENVIO10", 17800),
    ("CP17", 4, "urbana", "vip", 5, None, 7700),
    ("CP18", 7, "rural", "frecuente", 4, None, 9400),
    ("CP19", 20, "nacional", "normal", 6, None, 26700),
]

# 4 Casos Inválidos (esperan ValueError o Exception)
CASOS_INVALIDOS = [
    # (caso_id, peso, zona, cliente, dia, cupon)
    ("CP04", 0, "urbana", "normal", 2, None),       # Límite inferior: peso = 0
    ("CP05", -1, "rural", "frecuente", 5, None),    # Peso negativo
    ("CP06", 51, "nacional", "vip", 4, None),       # Límite superior: peso > PMAX (50)
    ("CP20", 9, "urbana", "normal", 8, None),       # Día fuera de rango (d > 7)
]


@pytest.mark.parametrize(
    "caso_id, peso, zona, cliente, dia, cupon, esperado",
    CASOS_VALIDOS,
    ids=[c[0] for c in CASOS_VALIDOS]
)
def test_calc_casos_validos(caso_id, peso, zona, cliente, dia, cupon, esperado):
    """Evalúa los casos válidos esperando el costo numérico exacto."""
    resultado = calc(peso, zona, cliente, dia, cup=cupon)
    assert resultado == esperado, (
        f"Fallo en {caso_id} -> Esperado: ${esperado}, Obtenido: ${resultado}"
    )


@pytest.mark.parametrize(
    "caso_id, peso, zona, cliente, dia, cupon",
    CASOS_INVALIDOS,
    ids=[c[0] for c in CASOS_INVALIDOS]
)
def test_calc_casos_invalidos(caso_id, peso, zona, cliente, dia, cupon):
    """Evalúa que las entradas inválidas disparen ValueError o Exception."""
    with pytest.raises((ValueError, Exception)):
        calc(peso, zona, cliente, dia, cup=cupon)
