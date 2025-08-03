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