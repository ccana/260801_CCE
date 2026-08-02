"""
Visualización gráfica del CCE (Funcionalidad 2).

Barras horizontales con posicionamiento temporal:
- Inventario (DI): inicia en 0
- CxC: inicia al terminar el inventario
- CxP: inicia en 0
- CCE > 0: inicia al terminar CxP
- CCE < 0: inicia al terminar CxC
- CCE = 0: sin tramo visible
"""

from __future__ import annotations

from typing import Any

import plotly.graph_objects as go

from modulos.calculo_cce import calcular_cce
from modulos.colores import COLOR_CCE, COLOR_CXC, COLOR_CXP, COLOR_DI


def tramos_temporales(
    di: int,
    d_cxc: int,
    d_cxp: int,
) -> list[dict[str, Any]]:
    """
    Calcula inicio (base) y longitud de cada barra del gráfico.

    Retorna una lista de diccionarios con:
    etiqueta, base, longitud, color y texto auxiliar.
    """
    cce = calcular_cce(di, d_cxc, d_cxp)

    tramos: list[dict[str, Any]] = [
        {
            "etiqueta": "Inventario (DI)",
            "base": 0,
            "longitud": di,
            "color": COLOR_DI,
            "detalle": f"De 0 a {di} días",
        },
        {
            "etiqueta": "Cuentas por cobrar (D_CxC)",
            "base": di,
            "longitud": d_cxc,
            "color": COLOR_CXC,
            "detalle": f"De {di} a {di + d_cxc} días",
        },
        {
            "etiqueta": "Cuentas por pagar (D_CxP)",
            "base": 0,
            "longitud": d_cxp,
            "color": COLOR_CXP,
            "detalle": f"De 0 a {d_cxp} días",
        },
    ]

    # Posición del CCE según el signo
    if cce > 0:
        tramos.append(
            {
                "etiqueta": "CCE",
                "base": d_cxp,
                "longitud": cce,
                "color": COLOR_CCE,
                "detalle": f"De {d_cxp} a {d_cxp + cce} días (financiamiento)",
            }
        )
    elif cce < 0:
        inicio_cce = di + d_cxc
        tramos.append(
            {
                "etiqueta": "CCE",
                "base": inicio_cce,
                "longitud": abs(cce),
                "color": COLOR_CCE,
                "detalle": (
                    f"De {inicio_cce} a {inicio_cce + abs(cce)} días "
                    "(holgura a favor de la empresa)"
                ),
            }
        )
    else:
        # CCE = 0: barra con longitud cero (no se percibe tramo)
        tramos.append(
            {
                "etiqueta": "CCE",
                "base": d_cxp,
                "longitud": 0,
                "color": COLOR_CCE,
                "detalle": "Longitud cero: ciclo equilibrado",
            }
        )

    return tramos


def figura_barras_cce(di: int, d_cxc: int, d_cxp: int) -> go.Figure:
    """
    Construye el gráfico de barras horizontales del CCE.

    Cada barra usa `base` (inicio en el eje temporal) y `x` (duración en días).
    """
    tramos = tramos_temporales(di, d_cxc, d_cxp)
    cce = calcular_cce(di, d_cxc, d_cxp)

    # Invertir el orden para que Inventario quede arriba en el eje Y
    tramos_plot = list(reversed(tramos))

    etiquetas = [t["etiqueta"] for t in tramos_plot]
    bases = [t["base"] for t in tramos_plot]
    longitudes = [t["longitud"] for t in tramos_plot]
    colores = [t["color"] for t in tramos_plot]
    detalles = [t["detalle"] for t in tramos_plot]

    fig = go.Figure(
        go.Bar(
            y=etiquetas,
            x=longitudes,
            base=bases,
            orientation="h",
            marker=dict(color=colores, line=dict(width=0)),
            text=[f"{lon} d" if lon > 0 else "" for lon in longitudes],
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(color="white", size=12),
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Inicio: %{base} días<br>"
                "Duración: %{x} días<br>"
                "%{customdata}<extra></extra>"
            ),
            customdata=detalles,
        )
    )

    # Escala del eje X: cubrir el máximo entre ciclo operativo y CxP
    max_eje = max(di + d_cxc, d_cxp, di + d_cxc + max(cce, 0), 1)

    fig.update_layout(
        title=dict(
            text="Secuencia temporal del Ciclo de Conversión de Efectivo",
            font=dict(size=16, color=COLOR_CCE),
        ),
        xaxis=dict(
            title="Días",
            range=[0, max_eje * 1.05],
            showgrid=True,
            gridcolor="#e5e7eb",
            zeroline=True,
            zerolinecolor="#9ca3af",
        ),
        yaxis=dict(
            title="",
            categoryorder="array",
            categoryarray=etiquetas,
        ),
        height=360,
        margin=dict(l=20, r=20, t=60, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(248,250,252,0.6)",
        showlegend=False,
        bargap=0.35,
    )

    return fig


def explicacion_grafico(di: int, d_cxc: int, d_cxp: int) -> str:
    """
    Texto pedagógico que explica cómo leer el gráfico,
    adaptado al signo actual del CCE.
    """
    cce = calcular_cce(di, d_cxc, d_cxp)
    fin_cxc = di + d_cxc

    if cce > 0:
        lectura_cce = (
            f"Como **CCE = {cce} > 0**, la barra del CCE comienza cuando termina "
            f"CxP (día {d_cxp}) y se extiende {cce} días hasta el final del ciclo "
            f"operativo (día {fin_cxc}). Ese tramo es el financiamiento que la "
            "empresa debe cubrir."
        )
    elif cce < 0:
        lectura_cce = (
            f"Como **CCE = {cce} < 0**, la barra del CCE comienza cuando termina "
            f"CxC (día {fin_cxc}) y cubre {abs(cce)} días hasta el final de CxP "
            f"(día {d_cxp}). Ese tramo es la holgura a favor de la empresa."
        )
    else:
        lectura_cce = (
            "Como **CCE = 0**, no hay tramo visible del ciclo: el final de CxP "
            f"coincide con el final de CxC (día {fin_cxc})."
        )

    return f"""
**Cómo leer el gráfico**

- Cada barra horizontal representa un componente del ciclo en el eje de **días**.
- **Inventario (DI)** siempre inicia en el día 0 y dura {di} días.
- **Cuentas por cobrar (D_CxC)** se encadenan al inventario: empiezan el día {di}
  (cuando termina DI) y duran {d_cxc} días, hasta el día {fin_cxc}.
- **Cuentas por pagar (D_CxP)** también parten del día 0 (son independientes del
  inventario) y duran {d_cxp} días. Así se puede comparar el crédito de
  proveedores con el ciclo operativo (DI + D_CxC).
- {lectura_cce}
"""
