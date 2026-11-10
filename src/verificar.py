"""P06. Comprobaciones aritméticas independientes. Uso: python src/verificar.py"""
from calcular import COSTO_MERCANCIA_PCT as C, TERMINALES, escenario, tasa_anual

n_ok = 0


def ok(cond, msg):
    global n_ok
    assert cond, msg
    n_ok += 1


clip = TERMINALES["clip"]
# 1) Tasa anual de 12 MSI con sobretasa de 12.77%: 29.34%
ok(abs(tasa_anual(12.77, 12) - 29.34) < 0.005, "tasa anual 12.77%")
# 2) Equivalencia directa: sin descuento, el descuento equivalente es la sobretasa
e = escenario(C, 0, clip["base"], 12.77, True, 12)
ok(abs(e["descuento_equivalente_pct"] - 12.77) < 1e-9, "descuento equivalente")
# 3) Unidades extra: margen_total debe igualarse (margen0 * 1 = margen1 * (1 + extra))
for d in (0, 5, 10, 15):
    e = escenario(C, d, clip["base"], 12.77, True, 12)
    if e["unidades_extra_pct"] is not None:
        ok(abs(e["margen_msi"] * (1 + e["unidades_extra_pct"] / 100) - e["margen_base"]) < 1e-9, f"igualdad de margen d={d}")
# 4) Con 20% de descuento se pierde dinero a 12 MSI
ok(escenario(C, 20, clip["base"], 12.77, True, 12)["unidades_extra_pct"] is None, "20% pierde")
# 5) Monotonía: más plazo o más descuento exige más unidades
for d in (0, 5, 10):
    v = [escenario(C, d, clip["base"], clip["sobretasa"][n], True, n)["unidades_extra_pct"] for n in (3, 6, 12)]
    ok(v[0] < v[1] < v[2], f"monotonía en plazo d={d}")
# 6) IVA no acreditable cuesta más que acreditable
a = escenario(C, 0, clip["base"], 12.77, True, 12)["unidades_extra_pct"]
b = escenario(C, 0, clip["base"], 12.77, False, 12)["unidades_extra_pct"]
ok(b > a, "IVA no acreditable")
# 7) Identidad de costos: 100 - costo - base = margen base
ok(abs(escenario(C, 0, 2.99, 0, True, 12)["margen_base"] - (100 - C - 2.99)) < 1e-12, "margen base")
ok(abs(escenario(C, 0, 2.99, 0, True, 12)["unidades_extra_pct"]) < 1e-9, "sin sobretasa no hay unidades extra")
print(f"{n_ok} comprobaciones correctas")
