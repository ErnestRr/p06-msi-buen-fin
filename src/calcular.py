"""Costo de ofrecer meses sin intereses (MSI): escenarios por terminal, plazo y descuento."""
import csv
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
RES = RAIZ / "resultados"

IVA = 0.16
PLAZOS = (3, 6, 12)
DESCUENTOS = (0, 5, 10, 15, 20)

# De Clip tomo la base de su página; la comisión extra por plazo sale de terceros,
# porque su tabla no se pudo leer. Mercado Pago publica todo en su sitio.
TERMINALES = {
    "clip": {
        "nombre": "Clip (referencia de terceros)",
        "base": 2.99,
        "sobretasa": {3: 4.57, 6: 7.57, 12: 12.77},
    },
    "mp": {
        "nombre": "Mercado Pago Point (oficial)",
        "base": 3.50,
        "sobretasa": {3: 4.69, 6: 7.69, 12: 12.89},
    },
}
COSTO_MERCANCIA_PCT = 67.99  # INEGI, Censos Económicos 2024, menudeo (67.994)
COMISION_PROMEDIO_BANXICO = 2.94  # Banxico, crédito, ventas al detalle, julio 2026


def factor_iva(acreditable):
    return 1.0 if acreditable else 1.0 + IVA


def escenario(costo_pct, descuento_pct, base_pct, sobretasa_pct, acreditable=True, n=12):
    """Todo en % del precio de lista. Se compara contra vender con tarjeta, sin MSI ni descuento."""
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
    """Tasa anual que implica la comisión: recibo (1 - s) hoy y el cliente paga 1/n cada mes."""
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
    with open(RES / "escenarios.csv", "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0].keys()))
        w.writeheader()
        for f in filas:
            w.writerow({k: ("" if v is None else (f"{v:.4f}" if isinstance(v, float) else v)) for k, v in f.items()})

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
    for d, x in ref["clip_iva_acreditable"]["12"].items():
        print(f"Clip, 12 meses, descuento {d}%: unidades extra {x['unidades_extra_pct']}, tasa anual {x['tasa_anual_pct']:.2f}%")


if __name__ == "__main__":
    main()
