# Challenge_ASOCIO25
# Asignación Óptima de Puestos en un Esquema Híbrido de Trabajo


Este proyecto aborda un problema real de optimización enfrentado por la Dirección de Planeación y Desarrollo Institucional de una universidad colombiana. A través de técnicas de programación matemática, se construye una herramienta de apoyo a la toma de decisiones que permite asignar, de forma eficiente y flexible, puestos de trabajo en modalidad híbrida, considerando tanto las restricciones operativas como las preferencias individuales de los colaboradores.

---

## Objetivo del Proyecto

Diseñar e implementar un modelo de optimización que:

- Asigne puestos de trabajo a cada colaborador en los días de presencialidad.
- Determine los días de asistencia para cada empleado, respetando al máximo sus preferencias.
- Seleccione el día de reunión presencial de cada equipo.
- Promueva la cercanía física entre miembros de un mismo grupo el día de la reunión.

---

## Características del Problema

- **Puestos compartidos**: No hay escritorios fijos.
- **Preferencias individuales**: Días deseados de asistencia.
- **Compatibilidad técnica**: Escritorios solo son aptos para ciertos empleados.
- **Agrupación por zonas**: Escritorios se distribuyen en zonas del edificio.
- **Cohesión grupal**: Se busca mantener a los equipos juntos.

---

## Enfoque de Solución

Se modeló el problema como un **programa entero mixto (MIP)** usando `PuLP` en Python. La formulación considera:

- Variables binarias para asistencia, asignación de puestos y activación de zonas.
- Restricciones duras (compatibilidad, disponibilidad, ocupación única por día).
- Restricciones suaves ponderadas en la función objetivo (preferencias, cohesión, consistencia).

Se implementó un preprocesamiento de datos flexible y la solución es escalable a diferentes instancias.

---
