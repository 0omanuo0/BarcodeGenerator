from barcode import Code128
from barcode.writer import ImageWriter
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader

from barcode import Code128
from barcode.writer import ImageWriter
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.colors import red, green, blue, magenta, black
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader

def generate_barcode_pdf_multiple_pages(
    base_code,
    start_number,
    total_codes,
    rows,
    cols,
    margins_mm,
    gap_mm,
    page_size=A4,
    draw_lines=False
):
    """
    Genera un PDF con múltiples páginas si el número de códigos excede la capacidad de una sola página,
    respetando el aspect ratio de los códigos de barras.
    
    Parámetros:
        base_code (str): Prefijo base para los códigos.
        start_number (int): Número inicial para los códigos.
        total_codes (int): Número total de códigos a generar.
        rows (int): Número de filas por página.
        cols (int): Número de columnas por página.
        margins_mm (tuple): Márgenes en milímetros.
        gap_mm (tuple): Espaciado entre códigos en milímetros (horizontal y vertical).
        page_size (tuple): Tamaño de la página (default: A4).
        draw_lines (bool): Si es True, dibuja líneas de referencia para las celdas y márgenes.
    """
    # Crear el canvas
    c = canvas.Canvas("temp.pdf", pagesize=page_size)
    page_width, page_height = page_size

    # Calcular márgenes, dimensiones de las celdas y gaps
    margin_x = margins_mm[0] * mm
    margin_y = margins_mm[1] * mm
    gap_x = gap_mm[0] * mm
    gap_y = gap_mm[1] * mm
    cell_width = (page_width - 2 * margin_x) / cols
    cell_height = (page_height - 2 * margin_y) / rows

    # Generar todas las páginas
    codes_per_page = rows * cols
    for page in range((total_codes + codes_per_page - 1) // codes_per_page):  # Total de páginas necesarias
        current_y = page_height - margin_y
        
        if draw_lines:
            # Guardar el estado gráfico
            c.saveState()
            
            # 1. Márgenes
            c.setStrokeColor(red)
            # Línea vertical izquierda
            c.line(margin_x, 0, margin_x, page_height)
            # Línea vertical derecha
            c.line(page_width - margin_x, 0, page_width - margin_x, page_height)
            # Línea horizontal superior
            c.line(0, page_height - margin_y, page_width, page_height - margin_y)
            # Línea horizontal inferior
            c.line(0, margin_y, page_width, margin_y)


            # 2. Dibujar las celdas (opcional, aquí se marcan las cajas de cada celda)
            c.setStrokeColor(blue)
            for row in range(rows):
                for col in range(cols):
                    x_cell = margin_x + col * cell_width
                    y_cell = page_height - margin_y - (row + 1) * cell_height
                    c.rect(x_cell, y_cell, cell_width, cell_height, stroke=1, fill=0)

            # Restaurar estado gráfico
            c.restoreState()

        for row in range(rows):
            current_x = margin_x
            for col in range(cols):
                # Calcular índice del código actual
                code_index = page * codes_per_page + row * cols + col
                if code_index >= total_codes:  # Terminar si no quedan más códigos
                    break

                # Generar código único
                code_number = start_number + code_index
                barcode_data = f"{base_code}{code_number}"
                
                # Generar la imagen del código de barras
                barcode = Code128(barcode_data, writer=ImageWriter())
                barcode_bytes = BytesIO()
                barcode.write(barcode_bytes, options={"module_width": 0.4, "module_height": 15, "font_size": 10, "text_distance": 6, "dpi": 300})
                barcode_bytes.seek(0)
                
                # Convertir a ImageReader para usar en drawImage
                barcode_image = ImageReader(barcode_bytes)
                
                # Escalar proporcionalmente para que quepa en la celda considerando los gaps
                aspect_ratio = 3/2  # Relación de aspecto aproximada para Code128
                max_width = cell_width - gap_x
                max_height = cell_height - gap_y
                if max_width / max_height > aspect_ratio:  # Espacio más ancho que el código
                    scaled_height = max_height
                    scaled_width = max_height * aspect_ratio
                else:  # Espacio más alto que el código
                    scaled_width = max_width
                    scaled_height = max_width / aspect_ratio
                
                # Centrar la imagen en la celda
                x_offset = (cell_width - scaled_width) / 2
                y_offset = (cell_height - scaled_height) / 2
                
                # Dibujar la imagen en el PDF
                c.setStrokeColorRGB(255, 0, 255)  # Magenta para los códigos
                c.drawImage(
                    barcode_image, 
                    current_x + x_offset, 
                    current_y - cell_height + y_offset, 
                    width=scaled_width, 
                    height=scaled_height,
                    showBoundary=draw_lines
                )
                
                # Mover al siguiente espacio horizontal
                current_x += cell_width
            
            current_y -= cell_height
        
        # Agregar nueva página si no es la última
        if (page + 1) * codes_per_page < total_codes:
            c.showPage()

    return c



if __name__ == "__main__":

    # get args from the shell
    import sys

    # print args to the console in raw, if is string, it will be printed with quotes
    for arg in sys.argv:
        print(arg if not isinstance(arg, str) else f'"{arg}"')
    base_code = sys.argv[1][0:2]
    start_number = int(sys.argv[1][2:])
    total_codes = int(sys.argv[2])
    rows = int(sys.argv[3])
    cols = int(sys.argv[4])
    margins_mm = float(sys.argv[5])
    gap_x_mm = float(sys.argv[6])
    gap_y_mm = float(sys.argv[7])

    # Llamar a la función
    canvas_object = generate_barcode_pdf_multiple_pages(base_code, start_number, total_codes, rows, cols, margins_mm, gap_x_mm, gap_y_mm)

    # Guardar el PDF
    canvas_object.save()




    # 
