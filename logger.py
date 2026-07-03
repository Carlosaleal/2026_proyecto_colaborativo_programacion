import logging

logging.basicConfig(
    filename="errores.log",
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)

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
    logging.error(f"{mensaje_usuario} | Detalle Técnico {type(excepcion).__name__}")
