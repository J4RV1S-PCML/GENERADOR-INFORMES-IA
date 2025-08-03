import csv

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