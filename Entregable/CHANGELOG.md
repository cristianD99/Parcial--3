# CHANGELOG

Todos los cambios notables de este proyecto se documentarán en este archivo.
El formato está basado en **Keep a Changelog** y se adhiere a los
principios de [Versionado Semántico](https://semver.org/).

## [2.0.0] - 2026-11-11

### Añadido
- Implementado el **Patrón Estrategia** mediante `EstrategiaDescuento` y clases
  concretas de descuento (`DescuentoClienteFrecuente`, `DescuentoClienteVip`,
  `DescuentoCuponEnvio10`, etc.) para permitir el manejo abierto/cerrado (OCP) de los descuentos.
- Definidas constantes descriptivas para límites de tarifa, recargos, descuentos,
  costos mínimos y redondeo.
- Añadidos métodos de apoyo con validaciones estrictas para peso, zona, cliente y día.

### Modificado
- **Breaking Change (Cambio de ruptura):** Eliminado el argumento `flag` de la función pública `calc` y erradicado su efecto secundario de impresión por consola. La función ahora delega la ejecución a `calcular_costo_envio`.
- Refactorizado `envios.py` para aislar las responsabilidades en funciones
  privadas de apoyo (`_calcular_tarifa_base`, `_aplicar_recargo_zona`, etc.).
- Actualizada la documentación de la API pública y sus docstrings correspondientes.

### Corregido
- **DEF-01:** Corregida la lógica del Tramo 1 para excluir el límite superior (`L1 = 3`),
  usando estrictamente la comparación `<`.
- **DEF-02:** Incluido el día sábado (`día == 6`) en la detección del recargo de fin de semana.
- **DEF-03:** Implementado el redondeo comercial correcto usando
  `Decimal.ROUND_HALF_UP` (anteriormente se truncaba usando `int()`).
- **DEF-04 / DEF-05:** Añadida validación estricta de tipo y rango para `dia`
  (debe estar entre 1 y 7) y `zona` (debe ser `"urbana"`, `"rural"` o
  `"nacional"`), lanzando `ValueError` ante entradas inválidas.

## [1.0.0] - 2026-02-15

### Añadido
- Lanzamiento inicial con el cálculo básico de costos de envío (defectos conocidos).

### Corregido
- N/A

---

*Fin del changelog.*
