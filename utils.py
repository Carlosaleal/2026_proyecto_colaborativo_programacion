# Este archivo contendrá todos los datos no variables o constantes que tendrá el código.

from tkinter import font # Importación módulo específico de fuentes

# Configuración principal de la ventana
ANCHO_VENTANA = 1000
ALTO_VENTANA = 700

# Función para centrar la ventana en la pantalla
def centrar_ventana(ventana, ANCHO_VENTANA, ALTO_VENTANA): 
    screen_width = ventana.winfo_screenwidth() 
    screen_height = ventana.winfo_screenheight()
    center_x = int(screen_width / 2 - ANCHO_VENTANA / 2)
    center_y = int(screen_height / 2 - ALTO_VENTANA / 2)
    ventana.geometry(f"{ANCHO_VENTANA}x{ALTO_VENTANA}+{center_x}+{center_y}")

# Función para formatear un valor numérico como moneda
def formatear_moneda(valor: float) -> str:
    
    try:
        numero = float(valor)
        if numero.is_integer():
            return f"$ {int(numero)}"
        else:
            return f"$ {numero:.2f}"
    except (ValueError, TypeError):
        return "$ 0"
    
# Colores
COLORES = {
    "fondo_primario": "#f0f0f0",
    "boton_confirmar": "#27ae60",
    "boton_cancelar": "#e74c3c",
    "boton_accion": "#3498db",
    "boton_neutral": "#95a5a6",
    "texto_blanco": "#ffffff",
    "estado_pendiente": "#f39c12",
    "estado_confirmado": "#27ae60",
    "estado_cancelado": "#e74c3c"
}

# Fuentes
FUENTE_TITULO_PRINCIPAL = ("Helvetica", 20, "bold")
FUENTE_SECUNDARIA = ("Helvetica", 16, "bold")
FUENTE_LABEL = ("Helvetica", 12, "bold")
FUENTE_LABEL_2 = ("Helvetica", 12, "italic")
FUENTE_BOTON = ("Helvetica", 14, "bold")

# Datos de ejemplo para pruebas
DATOS_EJEMPLO_CLIENTES = [
    ("1010", "Carlos Andrés Leal", "calealr@unadvirtual.edu.co"),
    ("2020", "Kenier Perez", "kenier@outlook.com"),
    ("3030", "Juan Albrin Meza", "juan@softwarefj.com")
]

# Datos de ejemplo para servicios
DATOS_EJEMPLO_SERVICIOS = [
    ("S01", "Sala de Cómputo", "Sala de Desarrollo Avanzado", "45000", "25"),
    ("S02", "Alquiler de Equipos", "Video Beam 4K Pro", "15000", "Epson X41"),
    ("S03", "Asesoría Especializada", "Consultoría Arquitectura Cloud", "60000", "Ing. Carlos Leal")
]