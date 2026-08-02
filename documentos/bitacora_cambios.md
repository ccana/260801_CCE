# Bitácora de cambios — CCE Interactivo

Registro breve de cambios, decisiones y aprendizajes del equipo.  
Formato: **fecha | cambio | aprendizaje**.

---

## 2026-08-01

### Documentación inicial de alcance

| | |
|---|---|
| **Cambio** | Se creó `documentos/funcionalidades_proyecto.md` con F01 (panel educativo + sliders + resultado) y F02 (gráfico de barras + explicación). Se definió layout, criterios de aceptación y ramas `feature/` desde `dev`. |
| **Aprendizaje** | Acordar el alcance por escrito **antes** de codear reduce retrabajo. El documento debe actualizarse cada vez que cambia el layout real de la app. |

---

### F01 — Panel educativo e interactivo (`feature/f1-cce`)

| | |
|---|---|
| **Cambio** | Implementación en Streamlit/Plotly: cálculo `CCE = DI + D_CxC − D_CxP`, sliders 0–100, métricas, indicador Plotly e interpretación por signo. Módulos `calculo_cce.py` y `colores.py`. |
| **Aprendizaje** | Separar lógica (`modulos/`) de interfaz (`app.py`) facilita pruebas y reutilizar colores en F02. |

---

### Ajustes de UI de F01 (iteración con capturas)

| | |
|---|---|
| **Cambio** | Se eliminó la cuarta métrica «CCE» (el valor queda en el indicador Plotly). Se quitó el rectángulo decorativo marfil y títulos redundantes del panel. El contenido educativo pasó a `st.sidebar`; luego los sliders se movieron a la **parte baja** del sidebar. |
| **Aprendizaje** | Cuando el agente interpreta mal el layout, conviene **Ask** para aclarar conceptos (p. ej. `unsafe_allow_html`) y **Agent** solo para cambios puntuales. Las capturas anotadas aceleran correcciones frente a descripciones ambiguas. |

---

### F02 — Visualización gráfica (`feature/f02-visualizacion-grafica-cce`)

| | |
|---|---|
| **Cambio** | Gráfico de barras horizontales con reglas temporales (DI en 0, CxC encadenada, CxP en 0, CCE según signo) y explicación dinámica. Módulo `grafico_cce.py` integrado en el área principal. |
| **Aprendizaje** | Reutilizar la paleta de F01 y documentar las reglas de `base`/`longitud` evita inconsistencias visuales entre controles y gráfico. |

---

### Sincronización documento ↔ código

| | |
|---|---|
| **Cambio** | Se actualizó `funcionalidades_proyecto.md` tras cada cambio de layout (sidebar, sliders abajo, área principal solo resultados/gráfico) y se marcaron criterios de aceptación cumplidos. |
| **Aprendizaje** | Si el código y el documento divergen, el equipo pierde la “fuente de verdad”. Actualizar la especificación en la misma rama o en una rama `docs/` evita confusiones. |

---

### Limpieza de proyecto (`refactor/limpieza01`)

| | |
|---|---|
| **Cambio** | Revisión de archivos realmente usados desde `app.py`. Eliminación de `__pycache__`, diccionario `COLORES` no referenciado, y dependencias no usadas (`numpy`, `pandas`) en `requirements.txt`. Se agregó `.gitignore`. |
| **Aprendizaje** | Partir del grafo de imports (no de la lista de archivos) identifica basura real. Un `.gitignore` temprano evita commitear caché. |

---

### README del repositorio (`docs/documentacion01`)

| | |
|---|---|
| **Cambio** | Se creó `README.md` con propósito, características, requisitos, instalación, uso, estructura, ramas Git, interpretación pedagógica y nota educativa/licencia. |
| **Aprendizaje** | El README debe reflejar el estado **real** (sidebar + sliders abajo, stack mínimo Streamlit/Plotly), no el diseño inicial descartado. |

---

### Esta bitácora (`docs/documentacion01`)

| | |
|---|---|
| **Cambio** | Se agregó `documentos/bitacora_cambios.md` como log de equipo. |
| **Aprendizaje** | Registrar no solo *qué* se hizo, sino *qué se aprendió*, ayuda a no repetir errores de UX o de flujo Agent/Ask. |

---

## Cómo usar esta bitácora

1. Agregar una entrada por cambio relevante (funcionalidad, refactor, docs o decisión de diseño).
2. Mantener el tono breve: un párrafo de cambio y uno de aprendizaje.
3. Preferir fechas ISO (`AAAA-MM-DD`) y el nombre de la rama cuando aplique.

---

## Resumen de ramas asociadas

| Rama | Temas registrados |
|------|-------------------|
| `feature/f1-cce` | F01 y primeros ajustes de UI |
| `feature/f02-visualizacion-grafica-cce` | F02 y reubicación de sliders |
| `refactor/limpieza01` | Limpieza de archivos y dependencias |
| `docs/documentacion01` | README y bitácora |
| `dev` | Integración de los merges anteriores |
