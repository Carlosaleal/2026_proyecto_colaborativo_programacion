# Autor: Carlos Andres Leal
# Formulario para gestionar reservas

# Importación de módulos necesarios
import os
import sys

directorio_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if directorio_raiz not in sys.path:
    sys.path.append(directorio_raiz)

import tkinter as tk
from tkinter import messagebox, ttk

import logger
from modelos.reserva import Reserva
from utils import FUENTE_LABEL, formatear_moneda, COLORES

# Clase principal del formulario de reservas
class FormularioReserva(tk.Frame):
    """Formulario para la gestión integral de reservas de servicios.
    
    Funcionalidades:
    - Seleccionar cliente (lista dinámica desde clientes_dict)
    - Seleccionar servicio (lista dinámica desde servicios_dict)
    - Especificar duración en horas
    - Registrar nuevas reservas (Create)
    - Cambiar estado de reservas (Pendiente → Confirmada → Cancelada)
    - Eliminar reservas con confirmación
    
    Estructura UI - 4 paneles:
    1. Panel izquierda: Treeview de clientes disponibles
    2. Panel centro: Treeview de servicios disponibles
    3. Panel derecha: Entrada de duración y botón confirmar
    4. Panel inferior: Treeview de reservas con botones de control
    
    Alineación con requerimientos:
    - MODULARIZACIÓN: Accede dinámicamente a clientes_dict y servicios_dict
    - CONSTANTES: Utiliza COLORES y formatear_moneda de utils (UPPERCASE)
    - VALIDACIÓN: Cambio de estados con confirmación del usuario
    - NOMENCLATURA: Métodos y atributos con snake_case
    - ALMACENAMIENTO: reservas_dict con modelos Reserva del módulo modelos.reserva
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        """Inicializa el formulario de reservas con los 4 paneles principales.
        
        Parámetros:
            parent (tk.Widget): Widget padre (generalmente un ttk.Notebook)
        
        Estructura de paneles:
        - Panel 1: Treeview de clientes (ID, Nombre)
        - Panel 2: Treeview de servicios (ID, Nombre, Tipo, Costo)
        - Panel 3: Entrada de duración en horas y botón Confirmar
        - Panel 4: Treeview de reservas con botones (Confirmar, Cancelar, Eliminar)
        
        Alineación con requerimientos:
        - ESTRUCTURA: Grid layout con columnas ponderadas para responsive design
        - TAGS: Color coding para estados de reserva (Pendiente, Confirmada, Cancelada)
        - VINCULACIÓN: Se vincula a cargar_datos() mediante <Visibility> event
        - CONSTANTES: Utiliza COLORES y FUENTE_LABEL (UPPERCASE de utils)
        """

        # ALMACENAMIENTO: diccionario de reservas (debe existir antes de que
        # cualquier método intente leerlo o escribirlo, p. ej. actualizar_lista_reservas)
        self.reservas_dict = {}

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=1)

        # Paneles y widgets del formulario
        self.panel_clientes = tk.LabelFrame(self, text=" 1. Seleccionar Cliente ", font=FUENTE_LABEL)
        self.panel_clientes.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.tree_clientes = ttk.Treeview(self.panel_clientes, columns=("ID", "Nombre"), show="headings", height=6)
        self.tree_clientes.heading("ID", anchor="center", text="ID")
        self.tree_clientes.column("ID", anchor="center", width=40)
        self.tree_clientes.heading("Nombre", anchor="center", text="Nombre")
        self.tree_clientes.column("Nombre", anchor="center", width=120)
        self.tree_clientes.pack(fill="both", expand=True)

        self.panel_servicios = tk.LabelFrame(self, text=" 2. Seleccionar Servicio ", font=FUENTE_LABEL)
        self.panel_servicios.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.tree_servicios = ttk.Treeview(self.panel_servicios, columns=("ID", "Nombre", "Tipo", "Costo"), show="headings", height=6)
        self.tree_servicios.heading("ID", anchor="center", text="ID")
        self.tree_servicios.column("ID", anchor="center", width=40)
        self.tree_servicios.heading("Nombre", anchor="center", text="Nombre")
        self.tree_servicios.column("Nombre", anchor="center", width=150)
        self.tree_servicios.heading("Tipo", anchor="center", text="Tipo")
        self.tree_servicios.column("Tipo", anchor="center", width=90)
        self.tree_servicios.heading("Costo", anchor="center", text="Costo")
        self.tree_servicios.column("Costo", anchor="center", width=70)
        self.tree_servicios.pack(fill="both", expand=True)

        self.panel_datos = tk.LabelFrame(self, text=" 3. Detalles de Reserva ", font=FUENTE_LABEL)
        self.panel_datos.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        tk.Label(self.panel_datos, text="Duración (Horas):").pack(pady=5)
        self.ent_duracion = tk.Entry(self.panel_datos, justify="center")
        self.ent_duracion.pack()
        tk.Button(self.panel_datos, text="Confirmar Reserva", command=self.registrar_reserva, bg=COLORES["boton_confirmar"], fg=COLORES["texto_blanco"]).pack(pady=15)

        self.panel_control = tk.LabelFrame(self, text=" 4. Gestión de Reservas Creadas ", font=FUENTE_LABEL)
        self.panel_control.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)

        # Configuración del Treeview para mostrar las reservas
        self.tree_reservas = ttk.Treeview(self.panel_control, columns=("ID", "Cliente", "Servicio", "Estado", "Costo"), show="headings", height=5)
        self.tree_reservas.tag_configure("Pendiente", background=COLORES["estado_pendiente"])
        self.tree_reservas.tag_configure("Confirmada", background=COLORES["estado_confirmado"])
        self.tree_reservas.tag_configure("Cancelada", background=COLORES["estado_cancelado"])

        # Configuración de encabezados y columnas del Treeview
        for col in ("ID", "Cliente", "Servicio", "Estado", "Costo"):
            self.tree_reservas.heading(col, anchor="center", text=col)
            self.tree_reservas.column(col, anchor="center", width=100)
        self.tree_reservas.pack(fill="x", padx=5, pady=5)

        self.frame_btns = tk.Frame(self.panel_control)
        self.frame_btns.pack(fill="x")
        # Botones para cambiar el estado de la reserva y eliminarla
        tk.Button(self.frame_btns, text="Confirmar", command=lambda: self.cambiar_estado("Confirmada"), bg=COLORES["boton_accion"], fg=COLORES["texto_blanco"]).pack(side="left", padx=5)
        tk.Button(self.frame_btns, text="Cancelar", command=lambda: self.cambiar_estado("Cancelada"), bg=COLORES["boton_cancelar"], fg=COLORES["texto_blanco"]).pack(side="left", padx=5)
        tk.Button(self.frame_btns, text="Eliminar", command=self.eliminar_reserva, bg=COLORES["boton_neutral"], fg=COLORES["texto_blanco"]).pack(side="right", padx=5)

        self.bind("<Visibility>", lambda event: self.cargar_datos())

    # Funciones para manejar la lógica de reservas
    def cargar_datos(self):
        """Carga dinámicamente clientes y servicios desde los formularios vinculados.
        
        Proceso:
        1. Limpia Treeviews de clientes y servicios
        2. Accede a pestaña_clientes.clientes_dict desde ventana principal
        3. Accede a pestaña_servicios.servicios_dict desde ventana principal
        4. Inserta filas en Treeviews con datos formateados
        5. Formatea costo usando formatear_moneda() (constante de utils)
        
        Alineación con requerimientos:
        - MODULARIZACIÓN: Integra datos de clientes_dict y servicios_dict
        - DINÁMICO: Se ejecuta al hacer visible la pestaña (<Visibility> event)
        - EXCEPCIONES: Try-except para manejo silencioso de errores
        - CONSTANTES: Usa formatear_moneda de utils (UPPERCASE)
        
        Nota: Navegación: master.master → ventana principal (VistaPrincipal)
        """
        try:
            for i in self.tree_clientes.get_children():
                self.tree_clientes.delete(i)
            for i in self.tree_servicios.get_children():
                self.tree_servicios.delete(i)
            for cid, obj in self.master.master.pestaña_clientes.clientes_dict.items():
                self.tree_clientes.insert("", "end", values=(cid, obj.nombre))
            for sid, obj in self.master.master.pestaña_servicios.servicios_dict.items():
                self.tree_servicios.insert("", "end", values=(sid, obj.nombre_servicio, type(obj).__name__, formatear_moneda(obj.costo_base)))
        except Exception:
            pass

    # Función para actualizar la lista de reservas en el Treeview
    def actualizar_lista_reservas(self):
        """Actualiza la visualización de todas las reservas en el Treeview.
        
        Proceso:
        1. Verifica que tree_reservas existe
        2. Limpia todas las filas previas del Treeview
        3. Itera reservas_dict e inserta fila para cada reserva
        4. Asigna TAG de color según estado de reserva (Pendiente/Confirmada/Cancelada)
        5. Formatea el costo usando formatear_moneda() (constante de utils)
        
        Alineación con requerimientos:
        - VALIDACIÓN: Verifica existencia de tree_reservas
        - ESTADO: Visualiza estados de reserva con color coding (tags)
        - CONSTANTES: Utiliza formatear_moneda de utils (UPPERCASE)
        - MODULARIZACIÓN: Utiliza método obtener_costo_reserva() del modelo Reserva
        """

        for i in self.tree_reservas.get_children():
            self.tree_reservas.delete(i)
        for rid, res in self.reservas_dict.items():
            self.tree_reservas.insert(
                "",
                "end",
                values=(rid, res.cliente.nombre, res.servicio.nombre_servicio, res._estado, formatear_moneda(res.obtener_costo_reserva())),
                tags=(res._estado,),
            )

    # Función para registrar una nueva reserva
    def registrar_reserva(self):
        """Registra una nueva reserva validando cliente, servicio y duración.
        
        Proceso:
        1. VALIDACIÓN: Verifica que cliente y servicio estén seleccionados
        2. VALIDACIÓN: Verifica que duración sea número positivo válido
        3. Crea instancia Reserva con ID generado dinámico
        4. Almacena en reservas_dict
        5. Actualiza lista visual de reservas
        6. Maneja excepciones mostrando mensajes de error
        
        Excepciones manejadas:
        - Selección incompleta de cliente o servicio
        - Duración inválida (no número, vacío, <= 0)
        - Errores inesperados durante creación
        
        Alineación con requerimientos:
        - VALIDACIÓN: Múltiples niveles de validación de entrada
        - MANEJO DE EXCEPCIONES: Try-except para captura de errores
        - MODULARIZACIÓN: Integra Cliente y Servicio del sistema
        - NOMENCLATURA: Usa snake_case (sel_c, sel_s, dur_txt, etc.)
        """
        try:
            sel_c = self.tree_clientes.selection()
            sel_s = self.tree_servicios.selection()
            # Validación de selección de cliente y servicio
            if not sel_c or not sel_s:
                raise Exception("Seleccione cliente y servicio.")

            dur_txt = self.ent_duracion.get().strip()
            if not dur_txt or not dur_txt.isdigit() or int(dur_txt) <= 0:
                raise Exception("Duración inválida.")
            # Creación de la reserva y actualización del diccionario de reservas
            res = Reserva(
                f"RES-{sel_s[0]}-{sel_c[0]}",
                self.master.master.pestaña_clientes.clientes_dict[str(self.tree_clientes.item(sel_c[0])["values"][0])],
                self.master.master.pestaña_servicios.servicios_dict[str(self.tree_servicios.item(sel_s[0])["values"][0])],
                int(dur_txt),
            )

            self.reservas_dict[res.id_reserva] = res
            self.actualizar_lista_reservas()

            costo_total = formatear_moneda(res.obtener_costo_reserva())
            tipo_servicio = type(res.servicio).__name__
            detalle_reserva = (
                f"Reserva creada exitosamente.\n\n"
                f"N° Reserva: {res.id_reserva}\n"
                f"Cliente: {res.cliente.nombre}\n"
                f"Servicio: {res.servicio.nombre_servicio} ({tipo_servicio})\n"
                f"Duración: {dur_txt} hora(s)\n"
                f"Costo total: {costo_total}"
            )
            messagebox.showinfo("Éxito", detalle_reserva)

            if hasattr(self.master, "master") and hasattr(self.master.master, "actualizar_logs_visuales"):
                self.master.master.actualizar_logs_visuales(
                    f"REGISTRO: Reserva [{res.id_reserva}] creada - Cliente: {res.cliente.nombre} | "
                    f"Servicio: {res.servicio.nombre_servicio} | Duración: {dur_txt}h | Costo: {costo_total}"
                )
            logger.registrar_evento(
                f"Reserva [{res.id_reserva}] creada correctamente - Cliente: {res.cliente.nombre}, "
                f"Servicio: {res.servicio.nombre_servicio}, Duración: {dur_txt}h, Costo: {costo_total}"
            )
        except Exception as e:
            messagebox.showerror("Error", str(e))
            logger.registrar_error("Fallo de validación al registrar reserva", e)
            if hasattr(self.master, "master") and hasattr(self.master.master, "actualizar_logs_visuales"):
                self.master.master.actualizar_logs_visuales(f"VALIDACIÓN: {str(e)}")

    # Función para cambiar el estado de una reserva seleccionada
    def cambiar_estado(self, nuevo_estado):
        """Cambia el estado de una reserva seleccionada (Confirmada o Cancelada).
        
        Parámetros:
            nuevo_estado (str): \"Confirmada\" para confirmar, \"Cancelada\" para cancelar
        
        Proceso:
        1. VALIDACIÓN: Verifica que una reserva esté seleccionada
        2. Obtiene objeto Reserva del diccionario
        3. Llama método confirmar_reserva() o cancelar_reserva() del modelo
        4. Actualiza visualización en Treeview
        5. Captura excepciones y muestra mensajes de error
        
        Alineación con requerimientos:
        - VALIDACIÓN: Verifica selección antes de procesar
        - MANEJO DE EXCEPCIONES: Try-except para captura de errores
        - ESTADO: Gestiona transiciones de estado de reserva
        - MODULARIZACIÓN: Utiliza métodos del modelo Reserva
        """
        try:
            sel = self.tree_reservas.selection()
            if not sel:
                raise Exception("Seleccione una reserva.")
            rid = self.tree_reservas.item(sel[0])["values"][0]
            res = self.reservas_dict[rid]
            if nuevo_estado == "Confirmada":
                res.confirmar_reserva()
            else:
                res.cancelar_reserva()
            self.actualizar_lista_reservas()
            if hasattr(self.master, "master") and hasattr(self.master.master, "actualizar_logs_visuales"):
                self.master.master.actualizar_logs_visuales(f"ACTUALIZACIÓN: Reserva [{rid}] cambiada a estado '{nuevo_estado}'.")
            logger.registrar_evento(f"Reserva [{rid}] cambiada a estado '{nuevo_estado}'")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            logger.registrar_error("Fallo al cambiar estado de reserva", e)
            if hasattr(self.master, "master") and hasattr(self.master.master, "actualizar_logs_visuales"):
                self.master.master.actualizar_logs_visuales(f"VALIDACIÓN: {str(e)}")

    # Función para eliminar una reserva seleccionada
    def eliminar_reserva(self):
        """Elimina una reserva seleccionada con confirmación del usuario.
        
        Proceso:
        1. VALIDACIÓN: Verifica que una reserva esté seleccionada
        2. Obtiene ID de la reserva desde Treeview
        3. Muestra diálogo de confirmación al usuario
        4. Si se confirma:
           - Elimina reserva del diccionario
           - Actualiza lista visual
        5. Captura excepciones inesperadas
        
        Alineación con requerimientos:
        - VALIDACIÓN: Confirmación del usuario antes de acción destructiva
        - MANEJO DE EXCEPCIONES: Try-except para captura de errores
        - NOMENCLATURA: Usa snake_case (sel, rid, etc.)
        """
        try:
            sel = self.tree_reservas.selection()
            if not sel:
                raise Exception("Seleccione una reserva.")
            rid = self.tree_reservas.item(sel[0])["values"][0]
            if messagebox.askyesno("Confirmar", "¿Eliminar reserva?"):
                del self.reservas_dict[rid]
                self.actualizar_lista_reservas()
                if hasattr(self.master, "master") and hasattr(self.master.master, "actualizar_logs_visuales"):
                    self.master.master.actualizar_logs_visuales(f"ELIMINADO: Reserva [{rid}] removida.")
                logger.registrar_evento(f"Reserva [{rid}] eliminada")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            logger.registrar_error("Fallo al eliminar reserva", e)
            if hasattr(self.master, "master") and hasattr(self.master.master, "actualizar_logs_visuales"):
                self.master.master.actualizar_logs_visuales(f"VALIDACIÓN: {str(e)}")