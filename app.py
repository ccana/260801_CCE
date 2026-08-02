"""
Aplicación educativa: Ciclo de Conversión de Efectivo (CCE).

Funcionalidad 1 (F01):
- Panel educativo en el sidebar (definición y fórmula).
- Controles, métricas e interpretación en el área principal.
- Indicador Plotly con el valor del ciclo.
"""

from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from modulos.calculo_cce import calcular_cce, interpretar_cce
from modulos.colores import COLOR_CCE, COLOR_CXC, COLOR_CXP, COLOR_DI


# ---------------------------------------------------------------------------
# Configuración de página
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Ciclo de Conversión de Efectivo (CCE)",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilos: tipografía y acentos por variable
st.markdown(
    f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@600;700&family=DM+Sans:wght@400;500;600&display=swap');

        html, body, [class*="css"] {{
            font-family: 'DM Sans', sans-serif;
        }}
        h1, h2, h3 {{
            font-family: 'Source Serif 4', Georgia, serif !important;
        }}
        .etiqueta-color {{
            display: inline-block;
            width: 0.7rem;
            height: 0.7rem;
            border-radius: 2px;
            margin-right: 0.45rem;
            vertical-align: middle;
        }}
        .nota-interpretacion {{
            background: #f8fafc;
            border-left: 4px solid {COLOR_CCE};
            padding: 0.9rem 1rem;
            margin-top: 0.75rem;
        }}
        div[data-testid="stMetric"] {{
            background: #ffffff;
            border: 1px solid #e5e7eb;
            padding: 0.75rem 1rem;
            border-radius: 0.35rem;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)


def etiqueta_variable(nombre: str, color: str) -> None:
    """Muestra el nombre de la variable con un indicador de color."""
    st.markdown(
        f'<span class="etiqueta-color" style="background:{color};"></span>'
        f"<strong>{nombre}</strong>",
        unsafe_allow_html=True,
    )


def figura_indicador_cce(cce: int) -> go.Figure:
    """
    Indicador Plotly con el valor del CCE.

    Refuerza la lectura del resultado con una métrica visual clara.
    """
    # Color del número según el signo del ciclo
    if cce < 0:
        color_valor = "#2A9D8F"
    elif cce == 0:
        color_valor = "#6B7280"
    else:
        color_valor = "#E76F51"

    fig = go.Figure(
        go.Indicator(
            mode="number",
            value=cce,
            number={"suffix": " días", "font": {"size": 56, "color": color_valor}},
            title={
                "text": "Ciclo de Conversión de Efectivo (CCE)",
                "font": {"size": 18, "color": COLOR_CCE},
            },
            domain={"x": [0, 1], "y": [0, 1]},
        )
    )
    fig.update_layout(
        height=180,
        margin=dict(l=10, r=10, t=50, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


# ---------------------------------------------------------------------------
# Sidebar: contenido educativo (definición y fórmula)
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### Definición")
    st.write(
        "El **Ciclo de Conversión de Efectivo (CCE)** mide el tiempo, en días, "
        "que transcurre desde que la empresa desembolsa efectivo por la compra "
        "de inventario hasta que lo recupera mediante el cobro a clientes."
    )

    st.markdown("### Fórmula")
    st.latex(r"CCE = DI + D_{CxC} - D_{CxP}")

    st.markdown(
        f"""
**Variables**

- <span class="etiqueta-color" style="background:{COLOR_DI};"></span>
  **DI** — Días de inventario: tiempo promedio que el inventario permanece
  en stock antes de venderse.
- <span class="etiqueta-color" style="background:{COLOR_CXC};"></span>
  **D_CxC** — Días de Cuentas por Cobrar: tiempo promedio que tarda la
  empresa en cobrar a sus clientes.
- <span class="etiqueta-color" style="background:{COLOR_CXP};"></span>
  **D_CxP** — Días de Cuentas por Pagar: tiempo promedio que tarda la
  empresa en pagar a sus proveedores.
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Área principal: sliders + resultado + indicador
# ---------------------------------------------------------------------------
st.markdown("## Simulador del CCE")
st.write(
    "Ajusta las variables con los controles. El CCE se recalcula de forma automática."
)

st.markdown("### Variables del ciclo")

# Valores por defecto razonables para un ejemplo didáctico
etiqueta_variable("DI — Días de inventario", COLOR_DI)
di = st.slider(
    "DI",
    min_value=0,
    max_value=100,
    value=45,
    step=1,
    label_visibility="collapsed",
    help="Días promedio de inventario (0 a 100).",
    key="slider_di",
)

etiqueta_variable("D_CxC — Días de Cuentas por Cobrar", COLOR_CXC)
d_cxc = st.slider(
    "D_CxC",
    min_value=0,
    max_value=100,
    value=30,
    step=1,
    label_visibility="collapsed",
    help="Días promedio de cuentas por cobrar (0 a 100).",
    key="slider_cxc",
)

etiqueta_variable("D_CxP — Días de Cuentas por Pagar", COLOR_CXP)
d_cxp = st.slider(
    "D_CxP",
    min_value=0,
    max_value=100,
    value=25,
    step=1,
    label_visibility="collapsed",
    help="Días promedio de cuentas por pagar (0 a 100).",
    key="slider_cxp",
)

# Cálculo automático
cce = calcular_cce(di, d_cxc, d_cxp)
interpretacion = interpretar_cce(cce)

st.markdown("### Resultado")
st.caption(f"CCE = {di} + {d_cxc} − {d_cxp} = **{cce}** días")

# Tres métricas de componentes; el CCE se muestra en el indicador Plotly
m1, m2, m3 = st.columns(3)
m1.metric("DI", f"{di} días")
m2.metric("D_CxC", f"{d_cxc} días")
m3.metric("D_CxP", f"{d_cxp} días")

# Indicador Plotly del CCE
st.plotly_chart(
    figura_indicador_cce(cce),
    width="stretch",
    config={"displayModeBar": False},
)

# Nota de interpretación según el signo
st.markdown("### Interpretación del resultado")
st.markdown(
    f"""
<div class="nota-interpretacion">
<strong>{interpretacion["condicion"]}</strong> — {interpretacion["titulo"]}<br><br>
{interpretacion["detalle"]}
</div>
    """,
    unsafe_allow_html=True,
)

# Referencia rápida de las tres condiciones
with st.expander("Ver las tres condiciones del CCE"):
    st.markdown(
        """
| Condición | Significado breve |
|-----------|-------------------|
| **CCE < 0** | Favorable: se cobra antes de pagar a proveedores. |
| **CCE = 0** | Equilibrio entre ciclo operativo y plazo de proveedores. |
| **CCE > 0** | Se necesita financiar inventario y/o cobros. |
        """
    )
