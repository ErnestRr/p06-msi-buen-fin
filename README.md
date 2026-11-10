# P06. ¿Cuánto cuesta realmente ofrecer meses sin intereses (MSI) en el Buen Fin?

**[Ver el reporte interactivo](https://ernestrr.github.io/p06-msi-buen-fin/visualizaciones/msi_buen_fin.html)**

## Objetivo
Quiero que un dueño de comercio pueda poner su propio margen y ver cuánto le cuesta ofrecer MSI y si le conviene. El resultado es un solo archivo HTML, [`visualizaciones/msi_buen_fin.html`](visualizaciones/msi_buen_fin.html), que se abre en el navegador sin servidor.

## Pregunta
La terminal le deposita al comercio en horas, así que los MSI no los "paga" el banco: los paga el margen del comercio, a través de una comisión extra por plazo (la sobretasa). Es un descuento que no sale en la etiqueta. Lo que me interesa medir es cuánto más tendría que vender el negocio para ganar lo mismo que sin MSI.

## Datos y fuentes (consulta: 10 de noviembre de 2026)
| Dato | Valor | Fuente | Estatus |
|---|---|---|---|
| Comisión base de Clip | 3% + $1 + IVA (promoción de 2.6% + $1 para terminales compradas antes del 13-nov) | [Clip México, calculadora](https://www.clip.mx/como-funciona-clip/calculadora-clip) | Oficial |
| Depósito de Clip | "24 horas garantizadas" | misma página | Oficial |
| Comisión extra por MSI de Clip | 4.6% (3 meses), 7.6% (6), 12.8% (12), sin IVA | Una calculadora y un blog de terceros que citan a Clip. La tabla oficial no se pudo leer (carga con JavaScript) | Terceros, por confirmar |
| Comisión base y extra de Mercado Pago Point | 3.5% base; 4.7% (3), 7.7% (6), 12.9% (12), más IVA | [Mercado Pago México, terminales Point](https://www.mercadopago.com.mx/herramientas-para-vender/lectores-point) | Oficial |
| Comisión promedio de tarjeta de crédito, ventas al detalle | 2.9% (mínimo 1.5%, máximo 4.5%), julio de 2026 | [Banxico, tasas de descuento de crédito por giro](https://www.banxico.org.mx/servicios/tasas-de-descuento-para-tarjetas-de-credito-por-gi/tasas-descuento-por-giro-cred.html) | Oficial |
| Costo de mercancía, menudeo | $67.99 de cada $100 vendidos (67.994) | INEGI, Censos Económicos 2024 (ingresos menos producción bruta), tomado de [P05](https://github.com/ErnestRr/p05-presion-costos-comercio) | Oficial |
| Ventas estimadas del Buen Fin 2026 | $235 mil millones, +7.3% (13 al 17 de noviembre) | CONCANACO Servytur, vía [UnoTV](https://www.unotv.com/negocios/buen-fin-2026-concanaco-estima-ventas-235-mil-millones-de-pesos-menor-crecimiento/) y [Publimetro](https://www.publimetro.com.mx/noticias/2026/10/28/buen-fin-2026-ventas-235-mil-millones-tiendas-fisicas/); no encontré el comunicado de CONCANACO | Nota de prensa |

No uso el 3.6% de comisión base que circula en un blog (la página de Clip dice 3%) ni el dato de 77% de pagos con tarjeta en 2025, porque no encontré fuente primaria.

## Cómo calculo
Todo en porcentaje del precio de lista. `k` vale 1 si el comercio acredita el IVA de la comisión y 1.16 si no.

- Sin MSI y sin descuento: `margen0 = 100 − costo − base·k`.
- Con MSI y un descuento `d`: `margen1 = (100 − d)·(1 − (base + sobretasa)·k/100) − costo`.
- Unidades extra para ganar lo mismo: `margen0 / margen1 − 1`. Si `margen1` no es positivo, cada venta deja pérdida.
- Tasa anual implícita: la tasa mensual que iguala los pagos de `1/n` del cliente con lo que el comercio recibe hoy, `1 − sobretasa`, llevada a 12 meses.
- Semáforo: verde hasta 10% más unidades, azul hasta 25% y vino si es más o hay pérdida. Es un criterio mío. El 25% equivale a que la comisión extra se lleve una quinta parte del margen.

## Hallazgos (Clip, IVA acreditable, costo de $67.99)
1. A 12 meses la comisión extra es de 12.8% y hay que vender **78.6%** más para ganar lo mismo; a 6 meses, 35.3%; a 3, 18.7%.
2. Con 10% de descuento encima, a 12 meses hay que vender **270.8%** más. Con 20%, cada venta deja pérdida.
3. Esa comisión equivale a prestarle al cliente a **29.3%** anual (a 3 meses, 32.5%).
4. Con las tarifas oficiales de Mercado Pago sale parecido: 82.5% más a 12 meses y 19.7% a 3.
5. Si el IVA no se acredita, a 12 meses con Clip la comisión extra pesa 14.8% y hay que vender **107.9%** más.

## Implicación
Más que preguntar cuánto cobra la terminal, conviene preguntar cuánto de mi margen estoy regalando y cuánto tendría que vender para recuperarlo. La cuenta es `comisión extra ÷ (margen − comisión extra)`. Los plazos largos y los descuentos encima son los que rompen el margen.

## Sobre el reporte
Va de lo simple a lo detallado: primero una frase con el resultado, luego tres cifras (cuánto te queda sin MSI, cuánto con MSI, cuánto más tendrías que vender), una tabla por plazo, tres acciones y una gráfica. Las variaciones llevan triángulo y color según lo que significan para el negocio (vino si perjudican, verde si favorecen). Porcentajes con un decimal; pesos con dos.

## Límites
- No hay dato público de qué parte de las ventas del Buen Fin se paga a MSI, ni de cuánto vende de más un comercio por ofrecerlos. El reporte calcula el volumen necesario, no el que se va a lograr.
- Supongo que el precio de lista no cambia, y no incluyo costos fijos ni efecto en recompra.
- El costo de mercancía es un promedio nacional del menudeo e incluye otros costos de venta; cada negocio debe poner el suyo.
- La comisión extra cambia según terminal, banco y volumen; hay que confirmarla con el proveedor. Las de Clip vienen de terceros.
- El IVA de la comisión es acreditable para quien lo traslada en régimen general; en otros regímenes puede no serlo (el reporte tiene la opción).

## Reproducir
Solo necesita Python 3.
```
python src/calcular.py     # resultados/escenarios.csv y resumen.json
python src/graficar.py     # visualizaciones/msi_buen_fin.html
python src/verificar.py    # pruebas rápidas de las cuentas
```

## Contenido
- `src/`: cálculo, generación del HTML (`plantilla.html`, `fuentes/`) y pruebas.
- `resultados/`: escenarios por terminal, plazo, descuento e IVA, y un resumen.
- `visualizaciones/msi_buen_fin.html`: el reporte interactivo.
