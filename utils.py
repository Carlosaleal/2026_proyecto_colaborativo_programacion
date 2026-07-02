# Este archivo contendrá todos los datos no variables o constantes que tendrá el código.

from tkinter import font # Importación módulo específico de fuentes

# Configuración principal de la ventana
ANCHO_VENTANA = 700
ALTO_VENTANA = 400

# Función para centrar la ventana en la pantalla
def centrar_ventana(ventana, ANCHO_VENTANA, ALTO_VENTANA): 
    screen_width = ventana.winfo_screenwidth() 
    screen_height = ventana.winfo_screenheight()
    center_x = int(screen_width / 2 - ANCHO_VENTANA / 2)
    center_y = int(screen_height / 2 - ALTO_VENTANA / 2)
    ventana.geometry(f"{ANCHO_VENTANA}x{ALTO_VENTANA}+{center_x}+{center_y}")

# Colores


# Fuentes
FUENTE_TITULO_PRINCIPAL = ("Helvetica", 20, "bold")
FUENTE_SECUNDARIA = ("Helvetica", 16, "bold")
FUENTE_LABEL = ("Helvetica", 12, "bold")