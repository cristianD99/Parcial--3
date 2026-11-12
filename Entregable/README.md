# EnvíaYa - Sistema de Cálculo de Envíos 

**Parcial 3 · Ingeniería de Software I**

Cristian David Muñoz Hernández

**Universidad de La Guajira - Facultad de Ingenierías**

## Descripción del Proyecto

Este repositorio contiene el sistema de cálculo de costos de envío para la empresa **EnvíaYa**, ubicada en Riohacha. El sistema original fue desarrollado con una lógica que actualmente presenta múltiples defectos, malas prácticas de programación ("code smells") y requiere adaptaciones para nuevas reglas de negocio.

Yo como equipo de calidad y mantenimiento, el objetivo de este proyecto es someter el código heredado a un proceso completo de Ingeniería de Software que incluye:

* Especificación de Requisitos e Historias de Usuario.

* Diseño y ejecución de un Plan de Pruebas (Caja Negra y Caja Blanca).

* Automatización de pruebas (TDD/Regresión).

* Reporte de Defectos.

* Refactorización de Código (aplicando el patrón Estrategia).

* Gestión de la Configuración y Versionado (Git).

## Estado Inicial: Versión 1.0.0 

La **versión 1.0.0** representa el código base (heredado). Contiene la función original `calc` en el archivo `envios.py`, la cual tiene defectos intencionales que serán descubiertos durante la fase de pruebas y corregidos en versiones posteriores.

**Nota importante:** No se realizarán cambios funcionales en el código fuente de esta versión hasta que se hayan diseñado y ejecutado las pruebas de línea base (Partes 1 a 5).

## Mis parámetros (Cod. Estudiantil: 0182410104)

Dado que las reglas de negocio varían según el código estudiantil, a continuación se establecen los parámetros únicos utilizados para calcular los resultados esperados en este repositorio:

| A | B | C | D | E | F | PMAX | L1 | L2 | RR | RN | V | S | CAMBIO | 
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | 
| 4 | 1 | 0 | 1 | 0 | 4 | 50 | 3 | 10 | 10% | 45% | 15% | \$2000 | 2 | 

## Hoja de Ruta

1. **Requisitos:** Definición de reglas (R1-R8) y trazabilidad.

2. **Plan de Pruebas:** Estrategia, niveles y riesgos.

3. **Caja Negra:** Particiones, valores límite y tabla de decisión.

4. **Caja Blanca:** Grafo de flujo, complejidad ciclomática y caminos independientes.

5. **Automatización:** Ejecución en pytest, métricas de cobertura y reporte de defectos.

6. **Mantenimiento y Refactorización:** Corrección de *code smells*, aplicación de patrón Estrategia y pruebas de regresión.

7. **Gestión de Configuración:** Estrategia de ramas, SemVer y Changelog.

8. **Solicitud de Cambio:** Análisis de impacto e implementación de nueva característica.

*Desarrollado para la asignatura de Ingeniería de Software - 2026-2*
