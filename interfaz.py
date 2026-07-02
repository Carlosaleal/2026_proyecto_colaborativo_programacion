import tkinter as tk
import utils
from tkinter import messagebox
from tkinter import ttk

from utils import (
    ANCHO_VENTANA,
    ALTO_VENTANA,
    centrar_ventana,
    FUENTE_TITULO_PRINCIPAL,
    FUENTE_SECUNDARIA,
    FUENTE_LABEL
)

class VistaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Software FJ - Sistema Integral de Gestión")

        centrar_ventana(self, ANCHO_VENTANA, ALTO_VENTANA)

        self.iniciar_componentes()

    def iniciar_componentes(self):

        titulo_label = tk.Label(
            self,
            text="Software FJ - Gestión de Servicios",
            font=FUENTE_TITULO_PRINCIPAL
        )
        titulo_label.pack(pady=10)

        self.cuaderno = ttk.Notebook(self)
        self.cuaderno.pack(fill="both", expand=True, padx=10, pady=5)

        self.pestaña_clientes = FormularioCliente(self.cuaderno)
        self.pestaña_servicios = FormularioServicio(self.cuaderno)
        self.pestaña_reservas = FormularioReserva(self.cuaderno)

        self.cuaderno.add(self.pestaña_clientes, text="Gestión de Clientes")
        self.cuaderno.add(self.pestaña_servicios, text="Gestión de Servicios")
        self.cuaderno.add(self.pestaña_reservas, text="Gestión de Reservas")

        panel_logs = tk.LabelFrame(self, text="Consola de Eventos / Logs", font=FUENTE_LABEL, fg="darkred")
        panel_logs.pack(fill="x", side="bottom", padx=10, pady=10)

        self.texto_logs = tk.Text(panel_logs, height=4, bg="#F4F4F4", state="disabled")
        self.texto_logs.pack(fill="x", padx=5, pady=5)
        
        self.actualizar_logs_visuales("Sistema FJ iniciado correctamente con geometrias de utils.py")

    def actualizar_logs_visuales(self, mensaje: str):
        
        self.texto_logs.config(state="normal")
        self.texto_logs.insert(tk.END, f">> {mensaje}\n")
        self.texto_logs.see(tk.END)
        self.texto_logs.config(state="disabled")

class FormularioCliente(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.config(padx=15, pady=15)
        self.crear_formulario()

    def crear_formulario(self):

        tk.Label(
            self,
            text="Registrar Nuevo Cliente",
            font=FUENTE_SECUNDARIA
        ).grid(row=0, column=0, columnspan=2, sticky="e", pady=5)
        
        tk.Label(
            self,
            text="ID / Identificación:",
            font=FUENTE_LABEL
        ).grid(row=1, column=0, sticky="e", pady=5)

        self.entrada_nombre = tk.Entry(self, width=25)
        self.entrada_nombre.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        boton_guardar = tk.Button(self, text="Registrar", command=self.procesar_registro_cliente, bg="#4CAF50", fg="white")
        boton_guardar.grid(row=3, column=1, pady=10, sticky="w")

    def procesar_registro_cliente(self):

        id_cliente = self.entrada_id.get().strip()
        nombre_cliente = self.entrada_nombre.get().strip()

        try:
            if not id_cliente or not nombre_cliente:
                raise Exception("datosInvalidosError: Campos obligatorios vacíos.")
            
            messagebox.showinfo("Éxito", f"Cliente {nombre_cliente} procesado.")
            self.master.master.actualizar_logs_visuales(f"ÉXITO: Cliente [{id_cliente}] mapeado en el sistema.")
            self.limpiar_campos()
        
        except Exception as error_detectado:
            messagebox.showerror("Error", str(error_detectado))
            self.master.master.actualizar_logs_visuales(f"EXCEPCIÓN ATRAPADA: {str(error_detectado)}")

    def limpiar_campos(self):
        self.entrada_id.delete(0, tk.END)
        self.entrada_nombre.delete(0, tk.END)

class FormularioServicio(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Tipos de Servicio (Salas, Equipos, Asesorías)", font=FUENTE_SECUNDARIA).pack(pady=10)

class FormularioReserva(tk.Frame):
    
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Control y Procesamiento de Reservas", font=FUENTE_SECUNDARIA).pack(pady=10)


if __name__ == "__main__":
    app = VistaPrincipal()
    app.mainloop()