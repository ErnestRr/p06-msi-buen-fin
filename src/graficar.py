"""P06. Genera el reporte interactivo (un solo HTML autocontenido, sin servidor).
Uso: python src/graficar.py   (escribe visualizaciones/msi_buen_fin.html)
"""
import base64
import json
from pathlib import Path

from calcular import COMISION_PROMEDIO_BANXICO, COSTO_MERCANCIA_PCT, DESCUENTOS, IVA, PLAZOS, TERMINALES

RAIZ = Path(__file__).resolve().parents[1]
FUENTES = RAIZ / "src" / "fuentes"
SALIDA = RAIZ / "visualizaciones" / "msi_buen_fin.html"

SELLO = ('<svg viewBox="0 0 100 100" width="46" height="46"><path d="M0 0 H84 L100 16 V100 H0 Z" fill="#F6F1E7"/>'
         '<g fill="none" stroke="#12213A" stroke-width="6.5" stroke-linecap="square" stroke-linejoin="miter">'
         '<path d="M28 32 H14 V68 H28"/><path d="M38 68 V32 H48 A9 9 0 0 1 48 50 H38 M48 50 L57 68"/>'
         '<path d="M68 68 V32 H78 A9 9 0 0 1 78 50 H68 M78 50 L87 68"/></g>'
         '<line x1="14" y1="50" x2="25" y2="50" stroke="#C4533A" stroke-width="6.5" stroke-linecap="square"/></svg>')

# (dato, valor, fuente, fecha de consulta, estatus)
FUENTES_TABLA = [
    ("Comisión base Clip", "3% + $1 + IVA (ventas regulares)", "Clip México, calculadora de comisiones (clip.mx/como-funciona-clip/calculadora-clip)", "10-nov-2026", "Oficial"),
    ("Depósito de Clip", "24 horas garantizadas", "Clip México, calculadora de comisiones (clip.mx/como-funciona-clip/calculadora-clip)", "10-nov-2026", "Oficial"),
    ("Comisión extra por MSI, Clip", "4.6% (3), 7.6% (6), 12.8% (12), sin IVA", "Calculadora y blog de terceros que citan a Clip; la tabla oficial de Clip no se pudo leer", "10-nov-2026", "Terceros, por confirmar"),
    ("Comisión base y extra por MSI, Mercado Pago Point", "3.5% base; 4.7% (3), 7.7% (6), 12.9% (12), + IVA", "Mercado Pago México, terminales Point (mercadopago.com.mx/herramientas-para-vender/lectores-point)", "10-nov-2026", "Oficial"),
    ("Comisión promedio de crédito, ventas al detalle", f"{COMISION_PROMEDIO_BANXICO:.1f}% (referencia)", "Banxico, tasas de descuento de tarjetas de crédito por giro, julio 2026", "10-nov-2026", "Oficial"),
    ("Costo de mercancía, menudeo", f"${COSTO_MERCANCIA_PCT:.2f} por cada $100 vendidos", "INEGI, Censos Económicos 2024 (ingresos menos producción bruta, menudeo)", "6-nov-2026", "Oficial"),
    ("Ventas estimadas del Buen Fin 2026", "$235 mil millones, +7.3% (estimación)", "CONCANACO Servytur, presentación oficial del 28-oct-2026, vía UnoTV y Publimetro", "10-nov-2026", "Nota de prensa"),
]


def b64(nombre):
    return base64.b64encode((FUENTES / nombre).read_bytes()).decode()


def construir():
    plantilla = (Path(__file__).with_name("plantilla.html")).read_text(encoding="utf-8")
    datos = {
        "terminales": {k: {"nombre": v["nombre"], "base": v["base"], "sobretasa": {str(n): s for n, s in v["sobretasa"].items()}} for k, v in TERMINALES.items()},
        "iva": IVA, "plazos": list(PLAZOS), "descuentos": list(DESCUENTOS), "costo_defecto": COSTO_MERCANCIA_PCT,
    }
    filas = "".join(
        f"<tr><td>{d}</td><td>{v}</td><td>{f}</td><td>{fe}</td><td>{e}</td></tr>" for d, v, f, fe, e in FUENTES_TABLA
    )
    html = (plantilla
            .replace("%%FONT_SERIF%%", b64("instrument-serif-latin-400-normal.woff2"))
            .replace("%%FONT_SERIF_IT%%", b64("instrument-serif-latin-400-italic.woff2"))
            .replace("%%FONT_INTER%%", b64("inter-latin-400-normal.woff2"))
            .replace("%%FONT_INTER_500%%", b64("inter-latin-500-normal.woff2"))
            .replace("%%DATOS%%", json.dumps(datos, ensure_ascii=False))
            .replace("%%SELLO%%", SELLO)
            .replace("%%FILAS_FUENTES%%", filas))
    SALIDA.parent.mkdir(exist_ok=True)
    SALIDA.write_text(html, encoding="utf-8")
    print(f"{SALIDA} ({SALIDA.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    construir()
