import os
import sys

directorio_raiz = os.path.dirname(os.path.abspath(__file__))
if directorio_raiz not in sys.path:
    sys.path.append(directorio_raiz)

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import logger
import modelos.cliente

from excepciones import datosInvalidosError

from utils import (
    ANCHO_VENTANA,
    ALTO_VENTANA,
    centrar_ventana,
    FUENTE_TITULO_PRINCIPAL,
    FUENTE_SECUNDARIA,
    FUENTE_LABEL
)

# se crea la clase principal de la interfaz gráfica
class VistaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Software FJ - Sistema Integral de Gestión")
        centrar_ventana(self, ANCHO_VENTANA, ALTO_VENTANA)
        self.iniciar_componentes()

    #se define el método para iniciar los componentes de la interfaz
    def iniciar_componentes(self):
        # se crea un label para el título principal
        titulo_label = tk.Label(
            self,
            text="Software FJ - Gestión de Servicios",
            font=FUENTE_TITULO_PRINCIPAL
        )
        titulo_label.pack(pady=10)
        # se crea un cuaderno (notebook) para organizar las pestañas de la interfaz
        self.cuaderno = ttk.Notebook(self)
        self.cuaderno.pack(fill="both", expand=True, padx=10, pady=5)
        # se crean las pestañas para cada formulario
        self.pestaña_clientes = FormularioCliente(self.cuaderno)
        self.pestaña_servicios = FormularioServicio(self.cuaderno)
        self.pestaña_reservas = FormularioReserva(self.cuaderno)
        # se agregan las pestañas al cuaderno con sus respectivos títulos
        self.cuaderno.add(self.pestaña_clientes, text="Gestión de Clientes")
        self.cuaderno.add(self.pestaña_servicios, text="Gestión de Servicios")
        self.cuaderno.add(self.pestaña_reservas, text="Gestión de Reservas")
        # se crea un panel de logs para mostrar mensajes de eventos y errores
        panel_logs = tk.LabelFrame(self, text="Consola de Eventos / Logs", font=FUENTE_LABEL, fg="darkred")
        panel_logs.pack(fill="x", side="bottom", padx=10, pady=10)
        # 
        self.texto_logs = tk.Text(panel_logs, height=4, bg="#F4F4F4", state="disabled")
        self.texto_logs.pack(fill="x", padx=5, pady=5)
        # se muestra un mensaje inicial en el panel de logs indicando que el sistema ha iniciado correctamente
        self.actualizar_logs_visuales("Sistema FJ iniciado correctamente")

    # se define el método para actualizar los logs visuales en la interfaz
    def actualizar_logs_visuales(self, mensaje: str):
        self.texto_logs.config(state="normal")
        self.texto_logs.insert(tk.END, f">> {mensaje}\n")
        self.texto_logs.see(tk.END)
        self.texto_logs.config(state="disabled")

# se crean las clases para los formularios de clientes, servicios y reservas
class FormularioCliente(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.config(padx=15, pady=15)
        self.crear_formulario()

    # se define el método para crear el formulario de registro de clientes
    def crear_formulario(self):
        # se crea un label para el título del formulario
        tk.Label(
            self,
            text="Registrar Nuevo Cliente",
            font=FUENTE_SECUNDARIA
        ).grid(row=0, column=0, columnspan=2, sticky="e", pady=5)
        # se crean los labels y campos de entrada para el ID, nombre y email del cliente
        tk.Label(
            self,
            text="ID / Identificación:",
            font=FUENTE_LABEL
        ).grid(row=1, column=0, sticky="e", pady=5)
        self.entrada_id = tk.Entry(self, width=25)
        self.entrada_id.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        tk.Label(
            self,
            text="Nombre del Cliente:",
            font=FUENTE_LABEL
        ).grid(row=2, column=0, sticky="e", pady=5)
        self.entrada_nombre = tk.Entry(self, width=25)
        self.entrada_nombre.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        tk.Label(
            self,
            text="E-mail:",
            font=FUENTE_LABEL
        ).grid(row=3, column=0, sticky="e", pady=5)
        self.entrada_email = tk.Entry(self, width=25)
        self.entrada_email.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        # se crea un botón para registrar el cliente, que llama al método procesar_registro_cliente al hacer clic
        boton_guardar = tk.Button(self, text="Registrar", command=self.procesar_registro_cliente, bg="#4CAF50", fg="white")
        boton_guardar.grid(row=4, column=1, pady=10, sticky="w")

    # se define el método para procesar el registro del cliente, validando los campos y mostrando mensajes de éxito o error
    def procesar_registro_cliente(self):
        # Capturar y limpiar los datos de los campos de texto
        id_cliente = self.entrada_id.get().strip()
        nombre_cliente = self.entrada_nombre.get().strip()
        email_cliente = self.entrada_email.get().strip() if hasattr(self, 'entrada_email') else "correo@ejemplo.com"

        try:
            #Validación visual previa antes de instanciar el modelo
            if not id_cliente or not nombre_cliente:
                from excepciones import datosInvalidosError
                raise datosInvalidosError("Campos obligatorios vacíos. Por favor diligencie la Identificación y el Nombre.")
            
            #Intentar crear la instancia del modelo (aquí se disparan los setters de clienteClass)
            from modelos.cliente import clienteClass
            nuevo_cliente = modelos.cliente.clienteClass(id_cliente, nombre_cliente, email_cliente)
            
            #FLUJO EXITOSO: Si no se lanza ninguna excepción
            mensaje_exito = f"Cliente [{id_cliente}] - {nombre_cliente} registrado con éxito."
            
            # Muestra ventana emergente
            messagebox.showinfo("Éxito", f"El cliente {nombre_cliente} ha sido procesado correctamente.")
            
            # Registra el éxito en la consola visual de la interfaz (abajo)
            self.master.master.actualizar_logs_visuales(f"ÉXITO: {mensaje_exito}")
            
            # Limpia los campos del formulario para un nuevo ingreso
            self.limpiar_campos()

        except datosInvalidosError as error_validacion:
            # CAPTURA CONTROLADA: Errores de validación (campos vacíos, correo mal estructurado, etc.)
            # Muestra un mensaje de error al usuario
            messagebox.showerror("Datos Inválidos", str(error_validacion))
            
            # Mantiene el reporte visible en la consola inferior de la pantalla principal
            self.master.master.actualizar_logs_visuales(f"VALIDACIÓN ENCONTRADA: {str(error_validacion)}")
            
            # Guarda de forma persistente el error en tu archivo errores.log técnico
            logger.registrar_error("Fallo de validación en formulario cliente", error_validacion)

        except Exception as error_inesperado:
            # CAPTURA GENÉRICA: Cualquier otra falla imprevista del sistema (p. ej. error de atributos o tipos)
            mensaje_critico = f"Error inesperado: {type(error_inesperado).__name__} - {str(error_inesperado)}"
            messagebox.showerror("Error del Sistema", "Ocurrió una anomalía interna en el sistema. Contacte al administrador.")
            
            # Refleja la falla grave en la consola visual
            self.master.master.actualizar_logs_visuales(f"ERROR CRÍTICO: {mensaje_critico}")
            
            # Guarda el rastro técnico completo en el log físico para el tutor
            logger.registrar_error("Excepción no controlada en el registro de cliente", error_inesperado)

    # se define el método para limpiar los campos de entrada del formulario después de un registro exitoso
    def limpiar_campos(self):
        self.entrada_id.delete(0, tk.END)
        self.entrada_nombre.delete(0, tk.END)
        self.entrada_email.delete(0, tk.END)

# se crea la clase para el formulario de servicios
class FormularioServicio(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Tipos de Servicio (Salas, Equipos, Asesorías)", font=FUENTE_SECUNDARIA).pack(pady=10)

# se crea la clase para el formulario de reservas
class FormularioReserva(tk.Frame):
    
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Control y Procesamiento de Reservas", font=FUENTE_SECUNDARIA).pack(pady=10)

# se define el bloque principal para ejecutar la aplicación
if __name__ == "__main__":
    app = VistaPrincipal()
    app.mainloop()