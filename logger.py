import logging
import sys

# Configuración básica del logging nativo
logging.basicConfig(
    filename="errores.log",
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)

# Funciones personalizadas para log de errores y eventos
def registrar_evento(mensaje: str):
    """
    Registra acciones normales del sistema
    """
    logging.info(mensaje)

def registrar_error(mensaje_usuario: str, excepcion: Exception):
    """
    Registrar los errores graves junto con 
    el detalle técnico de la excepción
    """
    logging.error(f"{mensaje_usuario} | Detalle Técnico: {type(excepcion).__name__} - {str(excepcion)}")



# Heredar métodos nativos de 'logging'
# Tomamos el módulo actual en tiempo de ejecución
modulo_actual = sys.modules[__name__]

# Lista de métodos nativos de la librería 'logging' que queremos exponer directamente
metodos_logging_nativos = [
    'debug', 'info', 'warning', 'error', 'critical', 'log',
    'exception', 'getLogger', 'disable', 'shutdown'
]

# Inyectamos dinámicamente los métodos para que puedan usarse como metodos heredados
for metodo in metodos_logging_nativos:
    if hasattr(logging, metodo):
        setattr(modulo_actual, metodo, getattr(logging, metodo))