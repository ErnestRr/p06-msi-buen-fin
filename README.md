# P06. ¿Cuánto cuesta realmente ofrecer meses sin intereses (MSI) en el Buen Fin?

**[Ver el reporte interactivo](https://ernestrr.github.io/p06-msi-buen-fin/visualizaciones/msi_buen_fin.html)**

## Objetivo
Que un dueño de comercio calcule, con su propio margen, cuánto le cuesta ofrecer MSI y si le conviene. El reporte interactivo es [`visualizaciones/msi_buen_fin.html`](visualizaciones/msi_buen_fin.html): un solo archivo que se abre en el navegador, sin servidor.

## Pregunta
Si el comercio cobra la venta en horas, ¿qué cuesta ofrecer MSI? La respuesta que sostengo: la **comisión extra por MSI** (sobretasa) que cobra la terminal. Es un descuento que no aparece en la etiqueta, y se mide en cuánto más hay que vender para ganar lo mismo.

## Datos y fuentes (consulta: 10 de noviembre de 2026, salvo indicación)
| Dato | Valor | Fuente | Estatus |
|---|---|---|---|
| Comisión base de Clip | 3% + $1 + IVA (promoción 2.6% + $1 para terminales compradas antes del 13-nov) | [Clip México, calculadora](https://www.clip.mx/como-funciona-clip/calculadora-clip) | Oficial |
| Depósito de Clip | "24 horas garantizadas" | misma página | Oficial |
| Comisión extra por MSI de Clip (sobretasa) | 4.6% (3 meses), 7.6% (6), 12.8% (12), sin IVA | Calculadora y blog de terceros que citan a Clip; la tabla oficial de Clip no se pudo leer (carga con JavaScript y no está en los términos publicados) | Terceros, por confirmar |
| Comisión base y extra por MSI de Mercado Pago Point | 3.5% base; 4.7% (3), 7.7% (6), 12.9% (12), más IVA | [Mercado Pago México, terminales Point](https://www.mercadopago.com.mx/herramientas-para-vender/lectores-point) | Oficial |
| Comisión promedio de tarjeta de crédito, ventas al detalle | 2.9% (mínimo 1.5%, máximo 4.5%), julio de 2026 | [Banxico, tasas de descuento de crédito por giro](https://www.banxico.org.mx/servicios/tasas-de-descuento-para-tarjetas-de-credito-por-gi/tasas-descuento-por-giro-cred.html) | Oficial |
| Costo de mercancía, menudeo | $67.99 por cada $100 vendidos (67.994) | INEGI, Censos Económicos 2024 (ingresos menos producción bruta, menudeo), de [P05](https://github.com/ErnestRr/p05-presion-costos-comercio) | Oficial |
| Ventas estimadas del Buen Fin 2026 | $235 mil millones, +7.3% (estimación, 13 al 17 de noviembre) | CONCANACO Servytur, presentación del 28-oct-2026, vía [UnoTV](https://www.unotv.com/negocios/buen-fin-2026-concanaco-estima-ventas-235-mil-millones-de-pesos-menor-crecimiento/) y [Publimetro](https://www.publimetro.com.mx/noticias/2026/10/28/buen-fin-2026-ventas-235-mil-millones-tiendas-fisicas/); no se pudo leer el comunicado de CONCANACO | Nota de prensa |

Lo que **no** se usa: el 3.6% de comisión base de Clip (viene de un blog; la página oficial dice 3%) y el 77% de pagos con tarjeta en 2025 (no encontré fuente primaria).

## Cómo se calculan las cifras
Todo en % del precio de lista, con `k = 1` si el IVA de la comisión es acreditable (costo sin IVA) y `k = 1.16` si no.

- Línea base (venta con tarjeta, sin MSI ni descuento): `margen0 = 100 − costo − base·k`.
- Con MSI y un descuento adicional `d`: `margen1 = (100 − d)·(1 − (base + sobretasa)·k/100) − costo`.
- **Unidades extra** = `margen0 / margen1 − 1`. Si `margen1 ≤ 0`, se pierde dinero en cada unidad.
- **Descuento equivalente** = `1 − (1 − d)(1 − sobretasa·k)`. Sin descuento adicional es la propia sobretasa.
- **Tasa anual implícita**: la tasa mensual `r` que iguala los pagos de `1/n` del cliente cada mes con `(1 − sobretasa)` recibido hoy, capitalizada a 12 meses.
- Semáforo (umbral propio, no es un dato oficial): verde si exige hasta 10% más unidades; azul hasta 25%; vino si exige más o hay pérdida. El 25% equivale a que la comisión extra se lleve una quinta parte del margen (comisión ÷ margen = 20%).

## Hallazgos (Clip, IVA acreditable, costo de mercancía de $67.99)
1. Vender a 12 MSI cuesta 12.8% del precio y exige **78.6%** más unidades para ganar lo mismo; a 6 meses, 35.3%; a 3 meses, 18.7%.
2. Con 10% de descuento adicional, 12 MSI exige **270.8%** más unidades; con 20%, cada venta deja pérdida.
3. La comisión extra de 12 meses equivale a prestarle al cliente a **29.3%** anual (sin IVA); a 3 meses, 32.5%.
4. Con Mercado Pago Point (datos oficiales) el resultado es parecido: 12 MSI exige 82.5% más unidades; 3 MSI, 19.7%.
5. Si el IVA de la comisión no es acreditable, la comisión extra de 12 MSI en Clip cuesta 14.8% del precio y exige **107.9%** más unidades (tasa anual implícita 35.4%).

## Implicación
La pregunta correcta no es "¿cuánto me cobra la terminal?", sino "¿cuánto de mi margen regalo y qué volumen necesito para recuperarlo?". Regla: comisión extra ÷ (margen por unidad después de pagarla) = cuánto más hay que vender. Los plazos largos y el descuento acumulado son los que rompen el margen.

## Criterios visuales del reporte (aplicar en los siguientes análisis)
- **Ejecutivo, escaneable y en lenguaje de dueño de negocio:** relato en tres pasos ("Pon tus números", "Esto es lo que pasa", "Esto es lo que hay que hacer"). El resultado va primero en una frase (semáforo), luego tres cifras que se leen en secuencia (cuánto te queda sin MSI, cuánto con MSI, cuánto más tendrías que vender), una acción concreta y una sola gráfica. Entradas mínimas (margen, descuento, plazo); lo demás va en "Más opciones". Fórmulas en "Cómo se calculó". Sin jerga (sobretasa, tasa implícita, descuento equivalente); cifras principales grandes (54 px) y textos de apoyo de 14 px o más.
- **Deltas** (guía de estilo del autor): triángulo antes del número y del mismo color (`▲ +78.6%`, `▼ −12.89`); signo real, con `−` tipográfico; peso Inter 500 en deltas pequeños y Instrument Serif en cifras grandes.
- **Color por consecuencia para el negocio, no por signo:** verde pino `#2B6A52` favorece, vino `#8F2B3E` perjudica, azul acero `#4A6785` sin cambio o no significativo (sin triángulo). Aquí subir las unidades por vender es malo, por eso `▲` va en vino. Terracota es marca, nunca un signo negativo.
- **Sin chips ni fondos tintados:** el semáforo es un punto y un título de color sobre tarjeta marfil claro; el estado también se dice con palabras (Te conviene / Depende de cuánto vendas de más / No te conviene).
- **Leyenda mínima** al pie de la gráfica: `▲ sube, ▼ baja`, la convención de color y si hay prueba de significancia (aquí no: es aritmética).
- Porcentajes con un decimal y sin ".0" (12.9%, 30%); pesos con dos decimales; paleta, tipografías, sello, fuente y aviso legal de la guía de estilo del autor.

## Supuestos y límites
- No hay dato público del porcentaje del Buen Fin que se paga a MSI, ni de cuánto vende de más un comercio por ofrecerlo (elasticidad); el reporte calcula el volumen **necesario**, no el que se obtendrá.
- El precio de lista no cambia; sin costos fijos ni efectos en la recompra.
- El costo de mercancía del INEGI es un promedio nacional del menudeo e incluye otros costos de venta; cada negocio debe poner el suyo.
- La comisión extra varía por banco emisor, volumen y terminal; hay que confirmar la vigente con el proveedor. La base de Clip puede ser menor con promociones o niveles de volumen.
- Las comisiones extra de Clip provienen de terceros. Las de Mercado Pago son oficiales y sirven de contraste.
- El IVA de la comisión es acreditable para quien lo traslada en el régimen general; en otros regímenes puede no serlo (opción en el reporte).
- Porcentajes con un decimal (sin decimal si es .0); pesos con dos. Los cálculos usan la precisión completa.

## Reproducir
Requiere Python 3 (solo biblioteca estándar).
```
python src/calcular.py     # resultados/escenarios.csv y resumen.json
python src/graficar.py     # visualizaciones/msi_buen_fin.html (fuentes incrustadas)
python src/verificar.py    # 13 comprobaciones aritméticas
```

## Contenido
- `src/`: cálculo, generación del HTML (`plantilla.html`, `fuentes/`) y verificación.
- `resultados/`: escenarios por terminal, plazo, descuento e IVA; resumen.
- `visualizaciones/msi_buen_fin.html`: reporte interactivo.
