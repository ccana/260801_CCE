# Ciclo de Conversión de Efectivo (CCE)

Aplicación web educativa para comprender, calcular e interpretar el **Ciclo de Conversión de Efectivo (CCE)** mediante controles interactivos y visualizaciones.

---

## 1. Descripción general

El **CCE** mide el tiempo (en días) que transcurre desde que una empresa desembolsa efectivo por la compra de inventario hasta que lo recupera mediante el cobro a clientes.

La fórmula utilizada es:

```text
CCE = DI + D_CxC − D_CxP
```

| Variable | Significado |
|----------|-------------|
| **DI** | Días de inventario |
| **D_CxC** | Días de cuentas por cobrar |
| **D_CxP** | Días de cuentas por pagar |

Este proyecto permite experimentar con esos tres componentes, observar el resultado en tiempo real y relacionarlo con una lectura financiera sencilla (ciclo positivo, equilibrado o negativo).

**Propósito:** apoyo pedagógico en finanzas / capital de trabajo. No es una herramienta de decisión empresarial ni un software de producción.

---

## 2. Características principales

### Funcionalidad 1 — Panel educativo e interactivo

- Definición y fórmula del CCE en el **sidebar**.
- Sliders para DI, D_CxC y D_CxP (rango 0–100), con color distintivo por variable.
- Cálculo automático del CCE.
- Métricas de componentes e **indicador Plotly** del resultado.
- Interpretación automática según el signo del CCE.

### Funcionalidad 2 — Visualización gráfica

- Gráfico de barras horizontales con la secuencia temporal de DI, CxC, CxP y CCE.
- Reglas de posicionamiento didácticas (encadenamiento inventario–CxC, CxP desde cero, tramo del CCE según signo).
- Explicación del gráfico adaptada al valor actual del ciclo.

### Interfaz

| Zona | Contenido |
|------|-----------|
| **Sidebar (arriba)** | Definición, fórmula y significado de variables |
| **Sidebar (abajo)** | Controles (sliders) |
| **Área principal** | Resultado, métricas, indicador, interpretación, gráfico y explicación |

---

## 3. Requisitos técnicos

| Requisito | Detalle |
|-----------|---------|
| **Python** | 3.10 o superior (desarrollado y verificado con Python 3.14) |
| **Sistema** | Windows, macOS o Linux |
| **Dependencias** | Ver `requirements.txt` |

Librerías necesarias:

```text
streamlit
plotly
```

---

## 4. Instalación paso a paso

### 1) Clonar el repositorio

```bash
git clone <URL-del-repositorio>
cd 260801_CCE
```

### 2) Crear y activar un entorno virtual

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4) Ejecutar la aplicación

```bash
streamlit run app.py
```

La app se abrirá en el navegador (por defecto, `http://localhost:8501`).

---

## 5. Guía de uso

### Flujo básico

1. En el **sidebar**, revise la definición y la fórmula del CCE.
2. En la sección **Controles del ciclo**, ajuste los sliders:
   - `DI` — días de inventario  
   - `D_CxC` — días de cuentas por cobrar  
   - `D_CxP` — días de cuentas por pagar  
3. En el área principal observe:
   - el desglose `CCE = DI + D_CxC − D_CxP`
   - las métricas de cada componente
   - el indicador numérico del CCE
   - la interpretación según el signo
   - el gráfico de barras y su explicación

### Ejemplo 1 — Ciclo positivo (se requiere financiamiento)

| Variable | Valor |
|----------|------:|
| DI | 45 |
| D_CxC | 30 |
| D_CxP | 25 |

```text
CCE = 45 + 30 − 25 = 50 días
```

Interpretación: el efectivo permanece inmovilizado más días de los que aporta el crédito de proveedores.

### Ejemplo 2 — Ciclo negativo (favorable en liquidez operativa)

| Variable | Valor |
|----------|------:|
| DI | 10 |
| D_CxC | 8 |
| D_CxP | 20 |

```text
CCE = 10 + 8 − 20 = −2 días
```

Interpretación: se recupera el efectivo de clientes antes de pagar a proveedores.

### Ejemplo 3 — Ciclo equilibrado

| Variable | Valor |
|----------|------:|
| DI | 10 |
| D_CxC | 10 |
| D_CxP | 20 |

```text
CCE = 10 + 10 − 20 = 0 días
```

Interpretación: el ciclo operativo coincide con el plazo de pago a proveedores.

---

## 6. Estructura del proyecto

```text
260801_CCE/
├── app.py                              # Entrada principal (Streamlit)
├── requirements.txt                    # Dependencias
├── .gitignore
├── README.md
├── documentos/
│   └── funcionalidades_proyecto.md     # Especificación funcional
└── modulos/
    ├── __init__.py
    ├── calculo_cce.py                  # Cálculo e interpretación del CCE
    ├── colores.py                      # Paleta de colores compartida
    └── grafico_cce.py                  # Barras horizontales y explicación (F02)
```

| Archivo | Rol |
|---------|-----|
| `app.py` | Interfaz Streamlit (sidebar + área principal) |
| `modulos/calculo_cce.py` | `calcular_cce`, `interpretar_cce` |
| `modulos/colores.py` | Colores de DI, D_CxC, D_CxP y CCE |
| `modulos/grafico_cce.py` | `figura_barras_cce`, `explicacion_grafico` |
| `documentos/funcionalidades_proyecto.md` | Alcance, layout y criterios de aceptación |

---

## 7. Estructura de ramas Git

El desarrollo se organiza a partir de `main` / `dev`, con ramas de funcionalidad y soporte:

```text
main
 └── dev
      ├── feature/f1-cce                         # F01: panel educativo e interactivo
      ├── feature/f02-visualizacion-grafica-cce  # F02: visualización gráfica
      ├── refactor/limpieza01                    # Limpieza de archivos no usados
      └── docs/documentacion01                   # Documentación (README, etc.)
```

| Rama | Propósito |
|------|-----------|
| `main` | Rama estable / base del repositorio |
| `dev` | Integración de funcionalidades |
| `feature/f1-cce` | Implementación de la Funcionalidad 1 |
| `feature/f02-visualizacion-grafica-cce` | Implementación de la Funcionalidad 2 |
| `refactor/limpieza01` | Refactor de estructura y dependencias |
| `docs/documentacion01` | Documentación del proyecto |

**Flujo habitual:** crear `feature/...` desde `dev` → desarrollar → fusionar de vuelta a `dev`.

---

## 8. Interpretación pedagógica de resultados

### Qué significa el signo del CCE

| Condición | Lectura pedagógica |
|-----------|--------------------|
| **CCE > 0** | La empresa necesita financiar el ciclo: inventario y cobros “atan” efectivo más tiempo del que obtienen de proveedores. |
| **CCE = 0** | Equilibrio: el ciclo operativo (DI + D_CxC) coincide con el plazo de proveedores (D_CxP). |
| **CCE < 0** | Situación favorable en liquidez operativa: se cobra (ciclo operativo) antes de pagar a proveedores. |

### Cómo leer el gráfico de barras

- **Inventario (DI)** siempre inicia en el día 0.
- **Cuentas por cobrar** empiezan cuando termina el inventario (se encadenan).
- **Cuentas por pagar** también parten del día 0 (crédito de proveedores, independiente del stock).
- Si **CCE > 0**, el tramo del CCE inicia al terminar CxP (financiamiento a cubrir).
- Si **CCE < 0**, el tramo del CCE inicia al terminar CxC (holgura a favor de la empresa).
- Si **CCE = 0**, no hay tramo visible del ciclo.

La explicación bajo el gráfico se actualiza con los valores de los sliders para reforzar esta lectura.

---

## 9. Licencia y nota educativa

### Nota educativa (importante)

Este proyecto tiene **fines exclusivamente pedagógicos y demostrativos**.

- Está diseñado para enseñar el concepto del Ciclo de Conversión de Efectivo.
- Los valores de los sliders son ilustrativos; no representan datos reales de una empresa.
- No constituye asesoría financiera, contable ni de inversión.
- No debe usarse como única base para decisiones operativas o estratégicas.

### Licencia

Salvo que se indique lo contrario en un archivo `LICENSE` del repositorio, el código se comparte con fines educativos. Se sugiere atribuir el proyecto al utilizarlo en cursos, talleres o materiales académicos.

Si se agrega una licencia formal (por ejemplo, MIT), ese archivo prevalecerá sobre esta sección.

---

## Documentación adicional

Para el detalle de alcance, layout y criterios de aceptación, consulte:

[`documentos/funcionalidades_proyecto.md`](documentos/funcionalidades_proyecto.md)

---

## Ejecución rápida (resumen)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```
