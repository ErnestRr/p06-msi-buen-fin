"""Pruebas rápidas de las cuentas. Uso: python src/verificar.py"""
from calcular import COSTO_MERCANCIA_PCT as C, TERMINALES, escenario, tasa_anual

clip = TERMINALES["clip"]
base = clip["base"]

assert abs(tasa_anual(12.77, 12) - 29.34) < 0.005

e = escenario(C, 0, base, 12.77, True, 12)
assert abs(e["descuento_equivalente_pct"] - 12.77) < 1e-9

# con las unidades extra, el margen total vuelve a ser el de vender sin MSI
for d in (0, 5, 10, 15):
    e = escenario(C, d, base, 12.77, True, 12)
    if e["unidades_extra_pct"] is not None:
        assert abs(e["margen_msi"] * (1 + e["unidades_extra_pct"] / 100) - e["margen_base"]) < 1e-9

assert escenario(C, 20, base, 12.77, True, 12)["unidades_extra_pct"] is None

for d in (0, 5, 10):
    v = [escenario(C, d, base, clip["sobretasa"][n], True, n)["unidades_extra_pct"] for n in (3, 6, 12)]
    assert v[0] < v[1] < v[2]

acreditable = escenario(C, 0, base, 12.77, True, 12)["unidades_extra_pct"]
no_acreditable = escenario(C, 0, base, 12.77, False, 12)["unidades_extra_pct"]
assert no_acreditable > acreditable

sin_msi = escenario(C, 0, base, 0, True, 12)
assert abs(sin_msi["margen_base"] - (100 - C - base)) < 1e-12
assert abs(sin_msi["unidades_extra_pct"]) < 1e-9

print("todo bien")
