# Funcionalidades del proyecto

## Resumen

Aplicación web educativa sobre el **Ciclo de Conversión de Efectivo (CCE)**. El objetivo es que el usuario comprenda qué es el CCE, cómo se calcula y cómo se interpreta, mediante controles interactivos y una visualización gráfica.

**Stack:** Streamlit, NumPy, Pandas, Plotly.

**Entrada de la aplicación:** `app.py`  
**Módulos de apoyo:** `modulos/calculo_cce.py`, `modulos/colores.py`

---

## Distribución de la interfaz

La interfaz se organiza en dos zonas. El contenido de cada funcionalidad se ubica según esta regla:

| Zona | Qué contiene | Qué no contiene |
|------|--------------|-----------------|
| **Sidebar** (barra lateral de Streamlit) | Solo el **panel educativo** (definición, fórmula y significado de las variables) | Controles, resultados ni gráficos |
| **Área principal** | Parte interactiva (sliders), métricas de componentes, indicador Plotly del CCE, interpretación (F01), y visualización gráfica con su explicación (F02) | Texto teórico del panel educativo |

En resumen:

- **Sidebar** → únicamente contenido educativo estático (F01, panel teórico).
- **Área principal** → toda la interacción y la visualización (F01 interactivo + F02 completo).

Notas de presentación del sidebar:

- Se usa `st.sidebar` (no una columna izquierda personalizada).
- El sidebar inicia **expandido** (`initial_sidebar_state="expanded"`).
- No se usa un rectángulo decorativo de fondo ni títulos del tipo «Ciclo de Conversión de Efectivo» / «Panel educativo»; el contenido arranca directamente con **Definición** y **Fórmula**.

---

## Estrategia de ramas

El desarrollo se realiza a partir de la rama `dev`. Cada funcionalidad se implementa en una rama `feature/` **distinta**:

| Funcionalidad | Rama | Base |
|---------------|------|------|
| F01 | `feature/f1-cce` | `dev` |
| F02 | `feature/f02-visualizacion-grafica-cce` | `dev` |

Flujo previsto:

1. Crear la rama `feature/...` desde `dev`.
2. Desarrollar e integrar solo el alcance de esa funcionalidad.
3. Fusionar de vuelta a `dev` (vía pull request o merge acordado por el equipo).

No mezclar F01 y F02 en la misma rama `feature/`.

---

## Visión general

| ID  | Funcionalidad                         | Zona de UI                                      | Rama `feature/` | Estado       |
|-----|---------------------------------------|-------------------------------------------------|-----------------|--------------|
| F01 | Panel educativo e interactivo del CCE | Sidebar (educativo) + área principal (interactivo y resultado) | `feature/f1-cce` | En desarrollo |
| F02 | Visualización gráfica del CCE         | Área principal (gráfico + explicación)          | Distinta por F02 | Planificado  |

---

## F01 — Panel educativo e interactivo del CCE

**Rama:** `feature/f1-cce` (desde `dev`).

### Objetivo

Presentar el concepto del CCE y permitir al usuario modificar sus componentes para observar el impacto en el resultado.

### Layout de F01

| Parte | Zona | Contenido |
|-------|------|-----------|
| Panel educativo | **Sidebar** | Definición, fórmula y significado de DI, D_CxC y D_CxP |
| Controles interactivos | **Área principal** | Sliders de DI, D_CxC y D_CxP |
| Resultado e interpretación | **Área principal** | Desglose del cálculo, métricas de componentes, indicador Plotly del CCE y nota según el signo |

Importante: en F01, **solo** el panel educativo va en el sidebar. Los sliders, las métricas, el indicador Plotly y la explicación del resultado van en el área principal.

### Panel educativo (sidebar)

#### 1. Definición

Texto introductorio que explique qué es el Ciclo de Conversión de Efectivo: el tiempo (en días) que transcurre desde que la empresa desembolsa efectivo por la compra de inventario hasta que lo recupera mediante el cobro a clientes.

#### 2. Fórmula

Se muestra la fórmula del CCE:

```
CCE = DI + D_CxC − D_CxP
```

Donde:

| Variable | Nombre completo            | Significado |
|----------|----------------------------|-------------|
| DI       | Días de inventario         | Tiempo promedio que el inventario permanece en stock antes de venderse |
| D_CxC    | Días de Cuentas por Cobrar | Tiempo promedio que tarda la empresa en cobrar a sus clientes |
| D_CxP    | Días de Cuentas por Pagar  | Tiempo promedio que tarda la empresa en pagar a sus proveedores |

### Controles interactivos — sliders (área principal)

Apartado en el **área principal** con un slider por cada variable de la fórmula:

| Variable | Rango  | Representación visual      |
|----------|--------|----------------------------|
| DI       | 0–100  | Color distintivo (propio)  |
| D_CxC    | 0–100  | Color distintivo (propio)  |
| D_CxP    | 0–100  | Color distintivo (propio)  |

Reglas:

- Cada slider permite valores enteros entre **0 y 100**.
- Cada variable se identifica con un **color distinto**, de modo que la misma paleta se reutilice en el resultado y en el gráfico (F02).
- La paleta vive en `modulos/colores.py` para mantener consistencia entre F01 y F02.

### Resultado del CCE (área principal)

También en el **área principal**, debajo de los sliders:

1. **Desglose del cálculo**, por ejemplo: `CCE = DI + D_CxC − D_CxP = … días`.
2. **Tres métricas** de componentes (DI, D_CxC, D_CxP), repartidas en el ancho disponible. **No** se muestra una cuarta tarjeta métrica para el CCE.
3. **Indicador Plotly del CCE**: visualización numérica principal del resultado del ciclo (con color según el signo).
4. **Nota de interpretación** según el signo del resultado:

| Condición | Interpretación |
|-----------|----------------|
| CCE < 0   | La empresa financia su operación con proveedores: recupera el efectivo de clientes antes de pagar a proveedores. Situación favorable desde el punto de vista de liquidez operativa. |
| CCE = 0   | El ciclo está equilibrado: el tiempo de inversión en inventario y cobros coincide con el plazo de pago a proveedores. |
| CCE > 0   | La empresa necesita financiar el ciclo: el efectivo queda inmovilizado en inventario y cuentas por cobrar durante más días de los que obtiene de crédito de proveedores. |

El cálculo e interpretación se implementan en `modulos/calculo_cce.py`.

---

## F02 — Visualización gráfica del CCE

**Rama:** `feature/f02-visualizacion-grafica-cce` (desde `dev`).

### Objetivo

Representar de forma visual la secuencia temporal de las variables del CCE y el propio ciclo, para reforzar la comprensión del cálculo.

### Layout de F02

| Parte | Zona | Contenido |
|-------|------|-----------|
| Visualización gráfica | **Área principal** | Gráfico de barras horizontales |
| Explicación del gráfico | **Área principal** | Texto que describe cómo leer el gráfico |

Importante: en F02, **tanto** la visualización **como** su explicación van en el área principal (no en el sidebar).

### Gráfico de barras horizontales (área principal)

Tipo: **barras horizontales** (una barra por componente).

Componentes a graficar:

1. Inventario (DI)
2. Cuentas por cobrar (CxC / D_CxC)
3. Cuentas por pagar (CxP / D_CxP)
4. Ciclo de conversión de efectivo (CCE)

### Reglas de posicionamiento en el eje temporal

| Componente | Inicio en el eje | Longitud |
|------------|------------------|----------|
| Inventario (DI) | Siempre en **0** | DI |
| Cuentas por cobrar (CxC) | Cuando **termina** el inventario (en `DI`) | D_CxC |
| Cuentas por pagar (CxP) | Siempre en **0** | D_CxP |
| CCE (si CCE > 0) | Cuando **termina** CxP (en `D_CxP`) | CCE |
| CCE (si CCE < 0) | Cuando **termina** CxC (en `DI + D_CxC`) | \|CCE\| (o tramo equivalente hacia la izquierda / con sentido negativo, según diseño) |
| CCE (si CCE = 0) | Sin tramo visible / longitud cero | 0 |

Notas de implementación:

- Inventario y CxC se encadenan: CxC comienza donde termina DI.
- CxP es independiente en el origen (arranca en cero), lo que permite comparar el plazo de proveedores frente al ciclo operativo (DI + D_CxC).
- El tramo del CCE se posiciona según el signo, para que el usuario vea visualmente el “hueco” de financiamiento (CCE > 0) o la holgura a favor de la empresa (CCE < 0).
- Los colores de cada barra deben coincidir con los de los sliders de F01 (`modulos/colores.py`).

### Explicación del gráfico (área principal)

En el **área principal**, junto al gráfico (debajo o al costado), un texto breve que explique:

- Qué representa cada barra.
- Por qué inventario y CxC se encadenan.
- Por qué CxP parte de cero.
- Cómo leer la posición del CCE cuando es positivo o negativo.

---

## Criterios de aceptación (resumen)

### F01

- [x] El panel educativo (definición y fórmula) aparece en el **sidebar**.
- [x] Los sliders, las métricas, el indicador Plotly y el resultado interpretado aparecen en el **área principal**.
- [x] Se muestra definición del CCE.
- [x] Se muestra la fórmula `CCE = DI + D_CxC − D_CxP` con el significado de cada variable.
- [x] Existen tres sliders (DI, D_CxC, D_CxP) con rango 0–100 y color distinto cada uno.
- [x] El resultado del CCE se actualiza según los sliders.
- [x] Hay tres métricas de componentes (DI, D_CxC, D_CxP); el CCE se muestra con el **indicador Plotly** (sin cuarta tarjeta métrica).
- [x] Se muestra la nota de interpretación para CCE < 0, CCE = 0 y CCE > 0.
- [x] El trabajo se realiza en una rama `feature/` distinta, creada desde `dev` (`feature/f1-cce`).

### F02

- [ ] El gráfico y su explicación aparecen en el **área principal**.
- [ ] Existe un gráfico de barras horizontales con DI, CxC, CxP y CCE.
- [ ] Inventario inicia en 0; CxC inicia al terminar inventario; CxP inicia en 0.
- [ ] Si CCE > 0, el tramo CCE inicia al terminar CxP; si CCE < 0, inicia al terminar CxC.
- [ ] Se incluye una explicación del gráfico.
- [ ] La paleta de colores es consistente con F01.
- [ ] El trabajo se realiza en una rama `feature/` distinta (separada de F01), creada desde `dev`.

---

## Notas

- Este documento define alcance funcional, layout (sidebar + área principal), estructura de archivos y estrategia de ramas.
- Estados sugeridos: Planificado | En desarrollo | Completado.
