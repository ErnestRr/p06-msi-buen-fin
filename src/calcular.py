"""P06. Costo real de ofrecer meses sin intereses (MSI). Cálculo y tablas.
Uso: python src/calcular.py   (escribe resultados/*.csv y resultados/resumen.json)
"""
import csv
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
RES = RAIZ / "resultados"

IVA = 0.16
PLAZOS = (3, 6, 12)
DESCUENTOS = (0, 5, 10, 15, 20)  # puntos de descuento adicional sobre el precio de lista

# Fuentes de cada parámetro (se reutilizan en el HTML y en el README)
TERMINALES = {
    "clip": {
        "nombre": "Clip (referencia de terceros)",
        "base": 2.99,  # clip.mx, calculadora, consultada 2026-11-10 (oficial)
        "sobretasa": {3: 4.57, 6: 7.57, 12: 12.77},  # blog/calculadora de terceros; sin tabla oficial legible
    },
    "mp": {
        "nombre": "Mercado Pago Point (oficial)",
        "base": 3.50,  # mercadopago.com.mx, consultada 2026-11-10
        "sobretasa": {3: 4.69, 6: 7.69, 12: 12.89},
    },
}
COSTO_MERCANCIA_PCT = 67.99  # INEGI, Censos Económicos 2024, menudeo: 67.994 (resultados de P05), a dos decimales
COMISION_PROMEDIO_BANXICO = 2.94  # Banxico, tasa de descuento crédito, Ventas al detalle, promedio, jul 2026


def factor_iva(acreditable):
    """1.00 si el IVA de la comisión es acreditable (costo = tasa sin IVA); 1.16 si no."""
    return 1.0 if acreditable else 1.0 + IVA


def escenario(costo_pct, descuento_pct, base_pct, sobretasa_pct, acreditable=True, n=12):
    """Todas las cifras en % del precio de lista. Devuelve dict con el resultado del escenario.

    Línea base: venta con tarjeta, sin MSI y sin descuento.   margen0 = 100 - costo - base*k
    Con MSI y descuento d:  margen1 = (100 - d) * (1 - (base + sobretasa)*k/100) - costo
    Unidades extra (%)   = margen0 / margen1 - 1   (None si margen1 <= 0: se pierde dinero)
    """
    k = factor_iva(acreditable)
    fee_base = base_pct * k
    fee_sob = sobretasa_pct * k
    margen0 = 100.0 - costo_pct - fee_base
    precio = 100.0 - descuento_pct
    margen1 = precio * (1.0 - (fee_base + fee_sob) / 100.0) - costo_pct
    extra = None if margen1 <= 0 else (margen0 / margen1 - 1.0) * 100.0
    desc_equiv = (1.0 - (1.0 - descuento_pct / 100.0) * (1.0 - fee_sob / 100.0)) * 100.0
    return {
        "fee_base": fee_base, "fee_sobretasa": fee_sob, "fee_total": fee_base + fee_sob,
        "margen_base": margen0, "margen_msi": margen1,
        "unidades_extra_pct": extra, "descuento_equivalente_pct": desc_equiv,
        "tasa_anual_pct": tasa_anual(fee_sob, n),
    }


def tasa_anual(sobretasa_pct, n=12):
    """Tasa efectiva anual implícita: el comercio recibe (1 - s) hoy y el cliente paga 1/n al final de cada mes."""
    s = sobretasa_pct / 100.0

    def f(r):
        return sum((1.0 / n) / (1.0 + r) ** t for t in range(1, n + 1)) - (1.0 - s)

    lo, hi = 1e-9, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if f(mid) > 0:
            lo = mid
        else:
            hi = mid
    r = (lo + hi) / 2
    return ((1.0 + r) ** 12 - 1.0) * 100.0


def main():
    RES.mkdir(exist_ok=True)
    filas = []
    for tkey, t in TERMINALES.items():
        for acred in (True, False):
            for n in PLAZOS:
                for d in DESCUENTOS:
                    e = escenario(COSTO_MERCANCIA_PCT, d, t["base"], t["sobretasa"][n], acred, n)
                    filas.append({"terminal": tkey, "iva_acreditable": acred, "plazo": n, "descuento_pct": d, **e})
    campos = list(filas[0].keys())
    with open(RES / "escenarios.csv", "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=campos)
        w.writeheader()
        for f in filas:
            w.writerow({k: ("" if v is None else (f"{v:.4f}" if isinstance(v, float) else v)) for k, v in f.items()})

    # Resumen con la referencia de la tesis (Clip, 12 MSI, margen del menudeo)
    ref = {}
    for tkey, t in TERMINALES.items():
        for acred in (True, False):
            clave = f"{tkey}_{'iva_acreditable' if acred else 'iva_no_acreditable'}"
            ref[clave] = {}
            for n in PLAZOS:
                ref[clave][str(n)] = {
                    str(d): escenario(COSTO_MERCANCIA_PCT, d, t["base"], t["sobretasa"][n], acred, n)
                    for d in (0, 10, 20)
                }
    resumen = {
        "costo_mercancia_pct": COSTO_MERCANCIA_PCT,
        "comision_promedio_banxico_pct": COMISION_PROMEDIO_BANXICO,
        "terminales": {k: {"nombre": v["nombre"], "base": v["base"], "sobretasa": {str(n): s for n, s in v["sobretasa"].items()}}
                       for k, v in TERMINALES.items()},
        "referencia": ref,
    }
    (RES / "resumen.json").write_text(json.dumps(resumen, ensure_ascii=False, indent=1), encoding="utf-8")
    e = ref["clip_iva_acreditable"]["12"]
    print("Clip, 12 MSI, IVA acreditable, margen del menudeo")
    for d in ("0", "10", "20"):
        x = e[d]
        print(f"  descuento {d}%: unidades extra {x['unidades_extra_pct']}, equivalente {x['descuento_equivalente_pct']:.2f}%, tasa anual {x['tasa_anual_pct']:.2f}%")


if __name__ == "__main__":
    main()
