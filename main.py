"""Punto de entrada principal (entry point) del Sistema Integral de Gestión - Software FJ.

Responsabilidades:
- Ser el único archivo que el usuario final ejecuta para iniciar la aplicación (python main.py)
- Importar la clase VistaPrincipal desde el paquete 'interfaz', que a su vez centraliza
  las clases de la interfaz de usuario (ui)
- Instanciar la ventana principal y arrancar el bucle de eventos de Tkinter

Alineación con requerimientos:
- MODULARIZACIÓN: Delega toda la lógica de construcción de la interfaz al módulo
  interfaz (y este a su vez al paquete ui), manteniendo main.py simple y desacoplado
- ESTRUCTURA: Actúa como capa superior del proyecto; no contiene lógica de negocio
  ni de interfaz, solo orquesta el arranque de la aplicación
- EJECUCIÓN: Utiliza el bloque estándar `if __name__ == "__main__"` para evitar que
  la aplicación se inicie automáticamente si este archivo llegara a ser importado

  Participantes del grupo:
  - Juan Albrin Meza Guzmán (Administrador y encargado de modelos)
  - Carlos Andrés Leal Ramírez (Encargado de IU)
  - Kenier Pérez Solona (Encargado de Test Automatizado)
"""

# se importa la clase VistaPrincipal desde el módulo interfaz
from interfaz import VistaPrincipal

# se crea una instancia de la clase VistaPrincipal y se inicia el bucle principal de la aplicación
# Alineación con requerimientos:
# - EJECUCIÓN: Bloque `if __name__ == "__main__"` que garantiza que la app solo se
#   inicie cuando este archivo se ejecuta directamente (no al ser importado)
# - ESTRUCTURA: app = VistaPrincipal() crea la ventana principal (Tkinter Tk());
#   app.mainloop() inicia el bucle de eventos que mantiene la interfaz gráfica activa
#   y receptiva a las acciones del usuario hasta que la ventana se cierre
if __name__ == "__main__":
    app = VistaPrincipal()
    app.mainloop()