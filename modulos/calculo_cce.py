"""
Cálculo e interpretación del Ciclo de Conversión de Efectivo (CCE).

Fórmula:
    CCE = DI + D_CxC - D_CxP
"""

from __future__ import annotations


def calcular_cce(di: int, d_cxc: int, d_cxp: int) -> int:
    """
    Calcula el CCE a partir de sus tres componentes.

    Parámetros
    ----------
    di : int
        Días de inventario.
    d_cxc : int
        Días de cuentas por cobrar.
    d_cxp : int
        Días de cuentas por pagar.

    Retorna
    -------
    int
        Ciclo de conversión de efectivo en días.
    """
    return di + d_cxc - d_cxp


def interpretar_cce(cce: int) -> dict[str, str]:
    """
    Devuelve título y texto de interpretación según el signo del CCE.

    Retorna un diccionario con las claves:
    - condicion: etiqueta corta (< 0, = 0, > 0)
    - titulo: resumen para mostrar en pantalla
    - detalle: explicación pedagógica
    """
    if cce < 0:
        return {
            "condicion": "CCE < 0",
            "titulo": "Ciclo negativo: financiamiento con proveedores",
            "detalle": (
                "La empresa financia su operación con proveedores: recupera el "
                "efectivo de clientes antes de pagar a proveedores. Situación "
                "favorable desde el punto de vista de liquidez operativa."
            ),
        }
    if cce == 0:
        return {
            "condicion": "CCE = 0",
            "titulo": "Ciclo equilibrado",
            "detalle": (
                "El ciclo está equilibrado: el tiempo de inversión en inventario "
                "y cobros coincide con el plazo de pago a proveedores."
            ),
        }
    return {
        "condicion": "CCE > 0",
        "titulo": "Ciclo positivo: se requiere financiamiento",
        "detalle": (
            "La empresa necesita financiar el ciclo: el efectivo queda "
            "inmovilizado en inventario y cuentas por cobrar durante más días "
            "de los que obtiene de crédito de proveedores."
        ),
    }
