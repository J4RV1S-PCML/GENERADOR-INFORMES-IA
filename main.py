# --- Función de análisis de ventas ---
def analisis_ventas(datos):
    """
    Analiza tendencias de productos vendidos, detecta si algún producto ha bajado en ventas respecto a la semana anterior y sugiere estrategias para aumentar ventas.

    Args:
        datos (list of dict): Lista de diccionarios con las ventas. Cada diccionario debe tener las claves 'fecha', 'producto', 'cantidad', 'precio'.

    Returns:
        str: Informe de análisis con tendencias, productos en descenso y sugerencias.
    """
    import datetime
    from collections import defaultdict

    # Agrupar ventas por semana y producto
    ventas_por_semana = defaultdict(lambda: defaultdict(int))
    for fila in datos:
        fecha = datetime.datetime.strptime(fila['fecha'], '%Y-%m-%d')
        semana = fecha.isocalendar()[1]
        producto = fila['producto']
        cantidad = int(fila['cantidad'])
        ventas_por_semana[semana][producto] += cantidad

    semanas = sorted(ventas_por_semana.keys())
    analisis = "\n## Análisis de Tendencias\n"
    if len(semanas) < 2:
        analisis += "No hay suficientes datos para comparar semanas.\n"
        return analisis

    semana_actual = semanas[-1]
    semana_anterior = semanas[-2]
    productos_actual = ventas_por_semana[semana_actual]
    productos_anterior = ventas_por_semana[semana_anterior]

    productos_descenso = []
    for producto in productos_actual:
        ventas_act = productos_actual[producto]
        ventas_ant = productos_anterior.get(producto, 0)
        if ventas_act < ventas_ant:
            productos_descenso.append((producto, ventas_ant, ventas_act))

    if productos_descenso:
        analisis += "Productos con descenso en ventas respecto a la semana anterior:\n"
        for prod, ant, act in productos_descenso:
            analisis += f"- {prod}: Semana anterior {ant}, Semana actual {act}\n"
        analisis += "\nSugerencias para aumentar ventas:\n"
        for prod, _, _ in productos_descenso:
            analisis += f"- Promocionar {prod} con descuentos o combos.\n  - Mejorar la visibilidad en tienda y redes sociales.\n"
    else:
        analisis += "No se detectaron productos con descenso en ventas esta semana. ¡Buen trabajo!\n"
    return analisis
import csv
import os
from fpdf import FPDF

# 1. Leer datos del archivo CSV
with open('ventas.csv', 'r') as archivo:
    lector = csv.DictReader(archivo)
    datos = [fila for fila in lector]

# 2. Calcular total y promedio de ventas
total_ventas = 0
cantidad_total = 0
for fila in datos:
    total_ventas += float(fila['precio']) * int(fila['cantidad'])
    cantidad_total += int(fila['cantidad'])
promedio_ventas = total_ventas / cantidad_total if cantidad_total > 0 else 0
# 3. Encontrar el producto más vendido
productos = {}
for fila in datos:
    producto = fila['producto']
    cantidad = int(fila['cantidad'])
    if producto in productos:
        productos[producto] += cantidad
    else:
        productos[producto] = cantidad
producto_mas_vendido = max(productos, key=productos.get)
# 4. (Luego) Generar informe Markdown
informe = f"""
# Informe de Ventas

## Resumen
- Total Ventas: ${total_ventas:.2f}
- Promedio Ventas: ${promedio_ventas:.2f}
- Producto Más Vendido: {producto_mas_vendido} (Cantidad: {productos[producto_mas_vendido]})

## Detalle de Ventas
| Fecha       | Producto  | Cantidad | Precio Unitario | Total   |
|-------------|-----------|----------|------------------|---------|
"""
for fila in datos:
    total_fila = float(fila['precio']) * int(fila['cantidad'])
    informe += f"| {fila['fecha']} | {fila['producto']} | {fila['cantidad']} | ${fila['precio']} | ${total_fila:.2f} |\n"


# Llamar a la función de análisis y agregar resultado al informe
analisis = analisis_ventas(datos)
informe += analisis

# Mostrar el informe en tiempo real en la consola
print(informe)


# 5. Generar PDF y guardarlo en la carpeta "reportes" con nombre único por fecha y secuencia
import datetime
os.makedirs("reportes", exist_ok=True)
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(0, 10, "Informe de Ventas", ln=True, align="C")
pdf.ln(10)
pdf.set_font("Arial", size=10)

pdf.multi_cell(0, 8, f"Total Ventas: ${total_ventas:.2f}\nPromedio Ventas: ${promedio_ventas:.2f}\nProducto Más Vendido: {producto_mas_vendido} (Cantidad: {productos[producto_mas_vendido]})")
pdf.ln(8)
pdf.cell(0, 8, "Detalle de Ventas:", ln=True)
pdf.set_font("Arial", size=9)
pdf.cell(35, 8, "Fecha", 1)
pdf.cell(35, 8, "Producto", 1)
pdf.cell(20, 8, "Cantidad", 1)
pdf.cell(35, 8, "Precio Unitario", 1)
pdf.cell(30, 8, "Total", 1)
pdf.ln()
for fila in datos:
    total_fila = float(fila['precio']) * int(fila['cantidad'])
    pdf.cell(35, 8, fila['fecha'], 1)
    pdf.cell(35, 8, fila['producto'], 1)
    pdf.cell(20, 8, str(fila['cantidad']), 1)
    pdf.cell(35, 8, f"${fila['precio']}", 1)
    pdf.cell(30, 8, f"${total_fila:.2f}", 1)
    pdf.ln()

# Agregar análisis al PDF
pdf.ln(8)
pdf.set_font("Arial", size=10)
pdf.multi_cell(0, 8, analisis)

# Generar nombre de archivo con fecha y secuencia
fecha_actual = datetime.datetime.now().strftime('%Y-%m-%d')
base_filename = f"informe_ventas_{fecha_actual}.pdf"
filepath = os.path.join("reportes", base_filename)
secuencia = 1
while os.path.exists(filepath):
    base_filename = f"informe_ventas_{fecha_actual}_{secuencia}.pdf"
    filepath = os.path.join("reportes", base_filename)
    secuencia += 1
pdf.output(filepath)
print(f"PDF generado: {filepath}")