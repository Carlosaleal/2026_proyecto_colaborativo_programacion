# Autor: Carlos Andres Leal
# Ventana principal de la aplicación

# Importación de módulos necesarios
import io
import os
import sys
import threading
import traceback
import unittest

directorio_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if directorio_raiz not in sys.path:
    sys.path.append(directorio_raiz)

import tkinter as tk
from tkinter import ttk

import logger
from .formulario_cliente import FormularioCliente
from .formulario_servicio import FormularioServicio
from .formulario_reserva import FormularioReserva
from utils import (
    ANCHO_VENTANA,
    ALTO_VENTANA,
    centrar_ventana,
    FUENTE_TITULO_PRINCIPAL,
    FUENTE_SECUNDARIA,
    FUENTE_LABEL,
    COLORES,
)

class VistaPrincipal(tk.Tk):
    """Ventana principal de la aplicación - Interfaz gráfica del sistema integral de gestión.
    
    Responsabilidades:
    - Crear la interfaz gráfica principal de la aplicación
    - Integrar los tres formularios principales (clientes, servicios, reservas)
    - Gestionar la consola de eventos/logs visual
    - Ejecutar pruebas automatizadas en hilos separados (threading)
    - Aplicar estilos y temas consistentes (COLORES del módulo utils)
    
    Alineación con requerimientos:
    - MODULARIZACIÓN: Integra módulos de formularios (formulario_cliente, formulario_servicio, formulario_reserva)
    - ESTILO: Utiliza constantes importadas de utils (snake_case, CONSTANTS) según lineamientos
    - THREADING: Ejecuta pruebas en hilos separados para no bloquear la interfaz
    - MANEJO DE EXCEPCIONES: Captura errores durante ejecución de pruebas
    """
    
    def __init__(self):
        super().__init__()
        self.title("Software FJ - Sistema Integral de Gestión")
        centrar_ventana(self, ANCHO_VENTANA, ALTO_VENTANA)
        self.iniciar_componentes()

    def iniciar_componentes(self):
        """Inicializa los componentes visuales de la interfaz principal.
        
        Crea:
        - Título principal de la aplicación
        - Cuaderno de pestañas (ttk.Notebook) con tres formularios
        - Panel de logs/eventos visual para registrar acciones del sistema
        - Botón para ejecutar pruebas automatizadas
        
        Alineación con requerimientos:
        - MODULARIZACIÓN: Instancia e integra cada formulario como pestaña
        - CONSTANTES: Utiliza COLORES y FUENTES del módulo utils (UPPERCASE para constantes)
        - VALIDACIÓN: Inicializa el panel de logs para registrar eventos del sistema
        """
        estilo = ttk.Style()
        estilo.configure("TNotebook.Tab", font=FUENTE_SECUNDARIA, padding=[10, 5])

        titulo_label = tk.Label(
            self,
            text="Software FJ - Gestión de Servicios",
            font=FUENTE_TITULO_PRINCIPAL,
        )
        titulo_label.pack(pady=10)
        # Creación del cuaderno de pestañas para la gestión de clientes, servicios y reservas
        self.cuaderno = ttk.Notebook(self)
        self.cuaderno.pack(fill="both", expand=True, padx=10, pady=5)

        self.pestaña_clientes = FormularioCliente(self.cuaderno)
        self.pestaña_servicios = FormularioServicio(self.cuaderno)
        self.pestaña_reservas = FormularioReserva(self.cuaderno)

        self.cuaderno.add(self.pestaña_clientes, text="Gestión de Clientes")
        self.cuaderno.add(self.pestaña_servicios, text="Gestión de Servicios")
        self.cuaderno.add(self.pestaña_reservas, text="Gestión de Reservas")

        panel_logs = tk.LabelFrame(self, text="Consola de Eventos / Logs", font=FUENTE_LABEL, fg=COLORES["boton_cancelar"])
        panel_logs.pack(fill="x", side="bottom", padx=10, pady=10)

        frame_logs = tk.Frame(panel_logs)
        frame_logs.pack(fill="x", padx=5, pady=5)

        self.texto_logs = tk.Text(frame_logs, height=4, bg=COLORES["fondo_primario"], state="disabled")
        self.texto_logs.pack(side="left", fill="x", expand=True)

        self.btn_ejecutar_pruebas = tk.Button(
            frame_logs,
            text="Ejecutar pruebas",
            font=("Helvetica", 10, "bold"),
            bg=COLORES["boton_accion"],
            fg=COLORES["texto_blanco"],
            command=self.ejecutar_pruebas_automatizadas,
        )
        self.btn_ejecutar_pruebas.pack(side="right", padx=(8, 0))

        self.actualizar_logs_visuales("Sistema FJ iniciado correctamente")

    def actualizar_logs_visuales(self, mensaje: str):
        """Actualiza el panel visual de logs con eventos del sistema.
        
        Parámetros:
            mensaje (str): Mensaje a registrar en los logs visuales
        
        Alineación con requerimientos:
        - MANEJO DE EVENTOS: Registra acciones del usuario (REGISTRO, ACTUALIZACIÓN, ELIMINACIÓN, VALIDACIÓN, ERROR)
        - DOCUMENTACIÓN: Proporciona trazabilidad visual de las operaciones realizadas
        """
        self.texto_logs.config(state="normal")
        self.texto_logs.insert(tk.END, f">> {mensaje}\n")
        self.texto_logs.see(tk.END)
        self.texto_logs.config(state="disabled")

    def ejecutar_pruebas_automatizadas(self):
        """Inicia la ejecución de pruebas automatizadas en un hilo separado.
        
        Alineación con requerimientos:
        - THREADING: Ejecuta unittest en hilo daemon para no bloquear la interfaz
        - LOGGING: Registra el inicio de la ejecución en el sistema de logs
        - UX: Deshabilita el botón durante la ejecución para evitar múltiples inicios
        """
        self.btn_ejecutar_pruebas.config(state="disabled", text="Ejecutando...")
        self.actualizar_logs_visuales("Iniciando pruebas automatizadas...")
        logger.registrar_evento("Inicio de ejecución de pruebas automatizadas desde la interfaz")

        hilo = threading.Thread(target=self._ejecutar_pruebas_en_hilo, daemon=True)
        hilo.start()

    def _ejecutar_pruebas_en_hilo(self):
        """Ejecuta las pruebas automatizadas (unittest) capturando la salida.
        
        Alineación con requerimientos:
        - MANEJO DE EXCEPCIONES: Captura errores durante la ejecución de pruebas
        - THREADING: Se ejecuta en hilo separado (daemon=True) para no bloquear UI
        - LOGGING: Registra errores en el sistema de logs usando logger.registrar_error()
        
        Nota: Este método es llamado desde ejecutar_pruebas_automatizadas() en un Thread.
        """
        try:
            flujo_salida = io.StringIO()
            suite = unittest.defaultTestLoader.discover(".", pattern="test_proyecto.py")
            resultado = unittest.TextTestRunner(stream=flujo_salida, verbosity=2)
            resultado.run(suite)

            salida = flujo_salida.getvalue().strip()
            if not salida:
                salida = "No se produjo salida de unittest."

            self.after(0, lambda: self._mostrar_resultados_pruebas(salida))
        except Exception as error:
            logger.registrar_error("Error al ejecutar pruebas automatizadas", error)
            self.after(0, lambda: self._mostrar_resultados_pruebas(f"Error durante la ejecución: {error}\n{traceback.format_exc()}"))

    def _mostrar_resultados_pruebas(self, salida: str):
        """Muestra los resultados de las pruebas en la interfaz y abre ventana emergente.
        
        Parámetros:
            salida (str): Salida capturada de unittest.TextTestRunner
        
        Alineación con requerimientos:
        - LOGGING: Registra el término de las pruebas en el sistema de logs
        - UX: Habilita el botón de pruebas y muestra resultados en ventana emergente
        """
        self.actualizar_logs_visuales("Resultados de pruebas automatizadas:")
        for linea in salida.splitlines():
            self.actualizar_logs_visuales(linea)

        self.actualizar_logs_visuales("Fin de ejecución de pruebas automatizadas")
        logger.registrar_evento("Fin de ejecución de pruebas automatizadas desde la interfaz")
        self.btn_ejecutar_pruebas.config(state="normal", text="Ejecutar pruebas")
        self.mostrar_resultado_en_ventana_emergente(salida)

    def mostrar_resultado_en_ventana_emergente(self, salida: str):
        """Crea una ventana emergente (Toplevel) para mostrar los resultados de pruebas.
        
        Parámetros:
            salida (str): Salida de unittest a mostrar
        
        Características:
        - Interfaz visual que indica PASÓ/FALLÓ con colores del sistema (COLORES dict)
        - Área de texto con scroll para visualizar detalles de pruebas
        - Utiliza constantes de colores importadas de utils (COLORES["estado_confirmado"])
        
        Alineación con requerimientos:
        - ESTILOS: Aplicación consistente de colores y fuentes del módulo utils
        - UX: Interfaz clara con información visual del estado de las pruebas
        """
        ventana = tk.Toplevel(self)
        ventana.title("Resultado de pruebas")
        ventana.geometry("700x450")
        centrar_ventana(ventana, 700, 450)

        paso = "OK" in salida.upper() and "FAILED" not in salida.upper()
        color_fondo = COLORES["estado_confirmado"] if paso else COLORES["estado_cancelado"]
        color_texto = COLORES["texto_blanco"]

        frame = tk.Frame(ventana, padx=10, pady=10)
        frame.pack(fill="both", expand=True)

        encabezado = tk.Frame(frame, bg=color_fondo, padx=10, pady=10)
        encabezado.pack(fill="x")

        tk.Label(
            encabezado,
            text="Ejecución de pruebas automatizadas",
            font=("Helvetica", 12, "bold"),
            bg=color_fondo,
            fg=color_texto,
        ).pack(anchor="w")

        estado_texto = "PASÓ" if paso else "FALLÓ"
        tk.Label(
            encabezado,
            text=f"Estado: {estado_texto}",
            font=("Helvetica", 11, "bold"),
            bg=color_fondo,
            fg=color_texto,
        ).pack(anchor="w", pady=(4, 0))

        texto = tk.Text(frame, wrap="word", bg=COLORES["fondo_primario"], height=20)
        texto.pack(fill="both", expand=True, pady=(8, 0))
        texto.insert(tk.END, salida)
        texto.config(state="disabled")

        barra = ttk.Scrollbar(frame, orient="vertical", command=texto.yview)
        barra.pack(side="right", fill="y")
        texto.configure(yscrollcommand=barra.set)

        tk.Button(
            frame,
            text="Cerrar",
            bg=COLORES["boton_neutral"],
            fg=COLORES["texto_blanco"],
            command=ventana.destroy,
        ).pack(pady=(10, 0), anchor="e")
