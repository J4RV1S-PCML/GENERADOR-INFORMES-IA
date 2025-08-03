# Generador de Informes de Ventas con IA

Este proyecto permite analizar y generar informes automáticos de ventas a partir de un archivo CSV. El informe se muestra en consola y se guarda en PDF, incluyendo análisis de tendencias y sugerencias para mejorar las ventas.

## Requisitos
- Python 3.11 o superior
- Paquete `fpdf` (instalación: `pip install fpdf`)
- Archivo `ventas.csv` con las columnas: `fecha`, `producto`, `cantidad`, `precio`

## Uso
1. Coloca tu archivo `ventas.csv` en la raíz del proyecto.
2. Ejecuta el script principal:
   ```powershell
   python main.py
   ```
   (En Windows PowerShell, usa la ruta completa si es necesario)
3. El informe se mostrará en la consola y se guardará en la carpeta `reportes` con nombre único por fecha y secuencia.

## Ejemplo de salida en consola
```
# Informe de Ventas

## Resumen
- Total Ventas: $290.00
- Promedio Ventas: $26.36
- Producto Más Vendido: camisa (Cantidad: 6)

## Detalle de Ventas
| Fecha       | Producto  | Cantidad | Precio Unitario | Total   |
|-------------|-----------|----------|------------------|---------|
| 2024-08-01 | camisa | 2 | $25 | $50.00 |
| 2024-08-01 | pantalon | 1 | $40 | $40.00 |
| 2024-08-02 | camisa | 3 | $25 | $75.00 |
| 2024-08-02 | corbata | 2 | $10 | $20.00 |
| 2024-08-03 | pantalon | 2 | $40 | $80.00 |
| 2024-08-03 | camisa | 1 | $25 | $25.00 |

## Análisis de Tendencias
No hay suficientes datos para comparar semanas.
```

## Notas
- Los archivos PDF generados se ignoran en el repositorio (ver `.gitignore`).
- El análisis de tendencias requiere al menos dos semanas de datos para comparar.
