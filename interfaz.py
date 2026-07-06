"""Carlos Andres Leal

Punto de entrada del paquete 'ui' - Interfaz de usuario del Sistema Integral de Gestión.

Responsabilidades:
- Centralizar la importación de todas las clases de la interfaz gráfica (ui)
- Exponer dichas clases mediante __all__ para su uso externo (from ui import ...)
- Actuar como punto de entrada (entry point) de la aplicación al ejecutarse directamente

Alineación con requerimientos:
- MODULARIZACIÓN: Agrupa e integra los módulos de formularios (formulario_cliente,
  formulario_servicio, formulario_reserva) junto con la ventana principal (ventana_principal)
- ESTRUCTURA: Simplifica las importaciones en otros módulos, evitando rutas largas
  (ej. permite `from ui import FormularioCliente` en lugar de `from ui.formulario_cliente import FormularioCliente`)
- EJECUCIÓN: Define el bloque __main__ como único punto de arranque de la aplicación
"""

# Importación de las clases de la interfaz de usuario
from ui.ventana_principal import VistaPrincipal
from ui.formulario_cliente import FormularioCliente
from ui.formulario_servicio import FormularioServicio
from ui.formulario_reserva import FormularioReserva

# Definición de las clases que se exportarán al importar este módulo
# Alineación con requerimientos:
# - MODULARIZACIÓN: Controla explícitamente qué clases son públicas al hacer `from ui import *`
# - NOMENCLATURA: Utiliza UPPERCASE para la constante __all__ (dunder reservado de Python)
__all__ = [
    "VistaPrincipal",
    "FormularioCliente",
    "FormularioServicio",
    "FormularioReserva",
]

# Se crea una instancia de la clase VistaPrincipal y se inicia el bucle principal de la aplicación
# Alineación con requerimientos:
# - EJECUCIÓN: Bloque estándar de Python (`if __name__ == "__main__"`) que evita que el código
#   se ejecute automáticamente si este archivo es importado desde otro módulo
# - ESTRUCTURA: Instancia VistaPrincipal (ventana principal) e inicia app.mainloop(),
#   el bucle de eventos de Tkinter que mantiene la interfaz gráfica activa
if __name__ == "__main__":
    app = VistaPrincipal()
    app.mainloop()