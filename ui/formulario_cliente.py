# Autor: Carlos Andres Leal
# Formulario para gestionar clientes

# Importación de módulos y configuración del path para importar desde el directorio raíz
import os
import sys

directorio_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if directorio_raiz not in sys.path:
    sys.path.append(directorio_raiz)

import tkinter as tk
from tkinter import messagebox, ttk

import logger
# Importación de clases y funciones desde otros módulos del proyecto
from modelos.cliente import Cliente
from excepciones import datosInvalidosError
from utils import (
    FUENTE_LABEL,
    FUENTE_LABEL_2,
    FUENTE_BOTON,
    DATOS_EJEMPLO_CLIENTES,
    COLORES,
)

# Clase FormularioCliente: Representa el formulario para registrar, editar y eliminar clientes
class FormularioCliente(tk.Frame):
    """Formulario para la gestión completa de clientes (CRUD).
    
    Funcionalidades:
    - Registrar nuevos clientes (Create)
    - Visualizar clientes en tarjetas con scroll (Read)
    - Editar datos de clientes existentes (Update)
    - Eliminar clientes con confirmación (Delete)
    
    Estructura UI:
    - Panel izquierdo: Formulario para registrar/editar clientes (ID, Nombre, Email)
    - Panel derecho: Lista visual de clientes como tarjetas con botones de acción
    
    Alineación con requerimientos:
    - VALIDACIÓN: Manejo de datosInvalidosError para campos obligatorios y duplicados
    - EXCEPCIONES: Try-except con logging de errores en sistema de logs
    - CONSTANTES: Utiliza COLORES y FUENTES importadas de utils (UPPERCASE)
    - NOMENCLATURA: Métodos con snake_case, atributos con snake_case
    - MODULARIZACIÓN: Integración con modelo Cliente y logger del proyecto
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        """Inicializa el formulario de clientes configurando la interfaz y datos iniciales.
        
        Parámetros:
            parent (tk.Widget): Widget padre (generalmente un ttk.Notebook)
        
        Alineación con requerimientos:
        - ESTRUCTURA: Crea dos paneles (izquierdo para input, derecho para visualización)
        - ALMACENAMIENTO: Inicializa diccionario clientes_dict para CRUD (snake_case)
        - UI: Configura canvas con scrollbar para gestionar múltiples registros
        - DATOS DEMO: Carga datos de demostración desde DATOS_EJEMPLO_CLIENTES (constante UPPERCASE)
        """
        
        self.clientes_dict = {}     # Diccionario para almacenar los clientes registrados, con la identificación como clave y el objeto Cliente como valor
        self.id_en_edicion = None   # Variable para almacenar la identificación del cliente que se está editando actualmente (si aplica)

        # Configuración de los paneles izquierdo y derecho del formulario
        self.panel_izq = tk.LabelFrame(
            self,
            text=" Registrar Nuevo Cliente ",
            font=FUENTE_LABEL,
            padx=10,
            pady=10
        )
        self.panel_izq.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.panel_der = tk.LabelFrame(
            self,
            text=" Clientes Registrados ",
            font=FUENTE_LABEL,
            padx=10,
            pady=10
        )
        # Configuración del canvas y scrollbar para el panel derecho, permitiendo desplazamiento vertical si hay muchos clientes
        self.canvas = tk.Canvas(self.panel_der, borderwidth=0, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.panel_der, orient="vertical", command=self.canvas.yview)

        self.scrollable_frame = tk.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.canvas.find_withtag("all")[0], width=e.width),
        )
        self.panel_der.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.crear_formulario()
        self.clientes_registrados()
        self.cargar_datos_demostracion()
        self.actualizar_vista_tarjetas()

    # Función para crear el formulario de registro/edición de clientes
    def crear_formulario(self):
        """Construye los campos de entrada y botones del panel izquierdo del formulario.
        
        Campos creados:
        - Entrada de ID/Identificación del cliente
        - Entrada de Nombre del cliente
        - Entrada de Email del cliente
        - Botón Registrar/Actualizar (dinámico según contexto)
        - Botón Cancelar (oculto hasta modo edición)
        
        Alineación con requerimientos:
        - NOMENCLATURA: Atributos con snake_case (entrada_id, entrada_nombre, etc.)
        - VALIDACIÓN: Campos vinculados a procesar_registro_cliente() con try-except
        - CONSTANTES: Utiliza FUENTE_LABEL_2, FUENTE_BOTON, COLORES (UPPERCASE de utils)
        """
        tk.Label(
            self.panel_izq,
            text="ID / Identificación:",
            font=FUENTE_LABEL_2,
        ).grid(row=0, column=0, sticky="e", pady=5)
        self.entrada_id = tk.Entry(self.panel_izq, width=25)
        self.entrada_id.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(
            self.panel_izq,
            text="Nombre del Cliente:",
            font=FUENTE_LABEL_2,
        ).grid(row=1, column=0, sticky="e", pady=5)
        self.entrada_nombre = tk.Entry(self.panel_izq, width=25)
        self.entrada_nombre.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(
            self.panel_izq,
            text="E-mail:",
            font=FUENTE_LABEL_2,
        ).grid(row=2, column=0, sticky="e", pady=5)
        self.entrada_email = tk.Entry(self.panel_izq, width=25)
        self.entrada_email.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        self.btn_guardar = tk.Button(
            self.panel_izq,
            text="Registrar",
            font=FUENTE_BOTON,
            command=self.procesar_registro_cliente,
            bg=COLORES["boton_confirmar"],
            fg=COLORES["texto_blanco"],
        )
        self.btn_guardar.grid(row=3, column=1, pady=10, sticky="w")

        self.btn_cancelar_edicion = tk.Button(
            self.panel_izq,
            text="Cancelar",
            font=FUENTE_BOTON,
            command=self.salir_modo_edicion,
            bg=COLORES["boton_cancelar"],
            fg=COLORES["texto_blanco"],
        )
        self.btn_cancelar_edicion.grid(row=4, column=1, pady=10, sticky="w")
        self.btn_cancelar_edicion.grid_remove() # Oculta el botón de cancelar edición al iniciar el formulario, ya que no hay un cliente en modo edición al cargar la interfaz por primera vez.

    # Función para inicializar el diccionario de clientes registrados
    def clientes_registrados(self):
        """Inicializa el diccionario de clientes registrados (actualmente sin operaciones).
        
        Nota: Este método es un placeholder que permite la estructura de carga de datos
        sin bloquear la ejecución. Los datos se cargan posteriormente en cargar_datos_demostracion().
        """

    # Función para actualizar la vista de tarjetas de clientes en el panel derecho
    def actualizar_vista_tarjetas(self):
        """Refresca la visualización de clientes como tarjetas en el panel derecho.
        
        Proceso:
        1. Limpia widgets previos del scrollable_frame
        2. Si no hay clientes, muestra mensaje de vacío
        3. Itera clientes_dict y crea tarjeta para cada uno con info y botones
        4. Cada tarjeta incluye botones de Editar y Eliminar con comandos asociados
        
        Alineación con requerimientos:
        - VALIDACIÓN: Verifica si clientes_dict está vacío
        - CONSTANTES: Aplica COLORES desde utils para consistencia visual
        - INTERACTIVIDAD: Vincula botones a entrar_modo_edicion() y eliminar_cliente()
        - NOMENCLATURA: Utiliza snake_case en variables (cliente_obj, id_cliente, etc.)
        """
        # Limpia el contenido actual del frame scrollable_frame antes de agregar las tarjetas de clientes
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        # Si no hay clientes registrados, muestra un mensaje indicando que no hay clientes en el sistema
        if not self.clientes_dict:
            lbl_vacio = tk.Label(
                self.scrollable_frame,
                text="No hay clientes registrados en el sistema.",
                font=("Helvetica", 10, "italic"),
                fg="gray",
            )
            lbl_vacio.pack(pady=20)
            return
        # Itera sobre los clientes registrados en el diccionario clientes_dict y crea una tarjeta para cada cliente, mostrando su información y botones de acción (Editar y Eliminar)
        for id_cliente, cliente_obj in self.clientes_dict.items():
            tarjeta = tk.Frame(
                self.scrollable_frame,
                bd=1,
                relief="ridge",
                bg=COLORES["fondo_primario"],
                padx=8,
                pady=6,
            )
            tarjeta.pack(fill=tk.X, padx=5, pady=4, expand=True)

            info_texto = f"ID: {cliente_obj.id_entidad}  |  {cliente_obj.nombre}\n✉ {cliente_obj.email}"
            lbl_info = tk.Label(
                tarjeta,
                text=info_texto,
                font=("Helvetica", 10),
                bg=COLORES["fondo_primario"],
                justify="left",
                anchor="w",
            )
            lbl_info.pack(side="left", fill=tk.X, expand=True)

            frame_botones = tk.Frame(tarjeta, bg=COLORES["fondo_primario"])
            frame_botones.pack(side="right")
            # Botón para editar cliente
            btn_editar = tk.Button(
                frame_botones,
                text="Editar",
                font=("Helvetica", 9),
                bg=COLORES["estado_pendiente"],
                fg=COLORES["texto_blanco"],
                bd=0,
                padx=8,
                pady=4,
                cursor="hand2",
                command=lambda c_id=id_cliente: self.entrar_modo_edicion(c_id),
            )
            btn_editar.pack(side="left", padx=2)
            # Botón para eliminar cliente
            btn_eliminar = tk.Button(
                frame_botones,
                text="Eliminar",
                font=("Helvetica", 9),
                bg=COLORES["boton_cancelar"],
                fg=COLORES["texto_blanco"],
                bd=0,
                padx=8,
                pady=4,
                cursor="hand2",
                command=lambda c_id=id_cliente: self.eliminar_cliente(c_id),
            )
            btn_eliminar.pack(side="left", padx=2)

    # Función para entrar en modo edición de un cliente específico, cargando sus datos en el formulario y ajustando la interfaz para reflejar que se está editando
    def entrar_modo_edicion(self, id_cliente):
        """Carga los datos de un cliente en el formulario para edición.
        
        Parámetros:
            id_cliente: Identificación del cliente a editar
        
        Acciones:
        1. Obtiene el objeto Cliente del diccionario
        2. Carga datos en campos de entrada (ID deshabilitado, Nombre y Email editables)
        3. Cambia botón Registrar a Actualizar
        4. Muestra botón Cancelar
        5. Registra acción en logs visuales del sistema
        
        Alineación con requerimientos:
        - MANEJO DE ESTADO: Utiliza id_en_edicion para rastrear cliente en edición
        - VALIDACIÓN: Retorna silenciosamente si cliente no existe
        - LOGGING: Integra con sistema de logs visuales del proyecto (actualizar_logs_visuales)
        - CONSTANTES: Aplicacolores y fuentes desde COLORES y FUENTE_BOTON (UPPERCASE)
        """
        cliente = self.clientes_dict.get(id_cliente)
        # Si el cliente no existe en el diccionario, simplemente retorna sin hacer nada
        if not cliente:
            return

        self.id_en_edicion = id_cliente
        self.limpiar_campos()
        self.entrada_id.insert(0, cliente.id_entidad)
        self.entrada_nombre.insert(0, cliente.nombre)
        self.entrada_email.insert(0, cliente.email)

        self.entrada_id.config(state="disabled")
        self.btn_guardar.config(
            text="Actualizar",
            bg=COLORES["boton_accion"],
            activebackground=COLORES["boton_accion"],
        )
        self.btn_cancelar_edicion.grid()
        # Si el formulario está contenido dentro de otro frame que tiene un método para actualizar logs visuales, se llama a ese método para registrar la acción de edición del cliente. Esto permite mantener un registro visual de las acciones realizadas en la interfaz.
        if hasattr(self.master, "master") and hasattr(self.master.master, "actualizar_logs_visuales"):
            self.master.master.actualizar_logs_visuales(f"EDICIÓN: Editando datos del cliente ID {id_cliente}")

    # Función para salir del modo edición, restaurando el formulario a su estado inicial y permitiendo registrar un nuevo cliente
    def salir_modo_edicion(self):
        """Cancela el modo edición y restaura el formulario a su estado inicial.
        
        Acciones:
        1. Limpia id_en_edicion (establece en None)
        2. Habilita campo ID para nuevos registros
        3. Limpia todos los campos de entrada
        4. Restaura botón Registrar con configuración inicial
        5. Oculta botón Cancelar
        
        Alineación con requerimientos:
        - VALIDACIÓN: Retorna formulario a estado seguro para nuevo registro
        - NOMENCLATURA: Usa snake_case en variables (id_en_edicion, entrada_id, etc.)
        - CONSTANTES: Restaura colores y textos originales desde COLORES y FUENTE_BOTON
        """
        self.id_en_edicion = None
        self.entrada_id.config(state="normal")
        self.limpiar_campos()
        self.btn_guardar.config(
            text="Registrar",
            font=FUENTE_BOTON,
            command=self.procesar_registro_cliente,
            bg=COLORES["boton_confirmar"],
            fg=COLORES["texto_blanco"],
        )
        self.btn_cancelar_edicion.grid_remove()

    # Función para cargar datos de demostración en el diccionario de clientes, útil para pruebas y demostraciones del sistema
    def cargar_datos_demostracion(self):
        """Carga datos de ejemplo en el diccionario de clientes para demostración.
        
        Fuente de datos:
        - Utiliza constante DATOS_EJEMPLO_CLIENTES importada de utils (UPPERCASE)
        - Tuplas de formato: (id, nombre, email)
        
        Alineación con requerimientos:
        - CONSTANTES: Obtiene datos de DATOS_EJEMPLO_CLIENTES (UPPERCASE de utils)
        - MODULARIZACIÓN: Utiliza modelo Cliente del módulo modelos.cliente
        - ALMACENAMIENTO: Popula clientes_dict con objetos Cliente para visualización
        """
        from modelos.cliente import Cliente

        for cid, nom, mail in DATOS_EJEMPLO_CLIENTES:
            self.clientes_dict[cid] = Cliente(cid, nom, mail)

    # Función para procesar el registro o actualización de un cliente, validando los datos ingresados y gestionando el diccionario de clientes
    def procesar_registro_cliente(self):
        """Registra un nuevo cliente o actualiza uno existente con validación completa.
        
        Proceso:
        1. Obtiene valores de campos de entrada con .strip()
        2. VALIDACIÓN: Verifica campos obligatorios (ID, Nombre requeridos)
        3. VALIDACIÓN: Comprueba duplicados en clientes_dict
        4. Crea objeto Cliente y lo almacena en diccionario
        5. Maneja tanto registro nuevo como actualización con mensajes diferentes
        6. Actualiza vista visual y registra en logs del sistema
        
        Excepciones manejadas:
        - datosInvalidosError: Campos vacíos, ID duplicado (CUSTOM exception)
        - Exception: Errores inesperados del sistema
        
        Alineación con requerimientos:
        - VALIDACIÓN: Lanza datosInvalidosError con mensajes descriptivos
        - EXCEPCIONES: Try-except con logging en logger.registrar_error()
        - LOGGING: Integra con actualizar_logs_visuales() del sistema
        - MODULARIZACIÓN: Utiliza modelo Cliente y excepciones personalizadas
        - CONSTANTES: Usa COLORES para botones (UPPERCASE de utils)
        """
        # Obtiene los valores ingresados en los campos del formulario, considerando si se está editando un cliente existente o registrando uno nuevo
        id_cliente = self.id_en_edicion if self.id_en_edicion else self.entrada_id.get().strip()
        nombre = self.entrada_nombre.get().strip()
        email = self.entrada_email.get().strip()
        # Validación de datos y manejo de excepciones para registrar o actualizar un cliente
        try:
            if not id_cliente or not nombre:
                raise datosInvalidosError("Campos obligatorios vacíos. Por favor diligencie la Identificación y el Nombre.")

            if not self.id_en_edicion and id_cliente in self.clientes_dict:
                raise datosInvalidosError(f"La identificación / ID '{id_cliente}' ya se encuentra registrada en el sistema.")

            nuevo_cliente = Cliente(id_cliente, nombre, email)
            self.clientes_dict[id_cliente] = nuevo_cliente

            if self.id_en_edicion:
                messagebox.showinfo("Éxito", "Los datos del cliente han sido actualizados correctamente.")
                if hasattr(self.master, "master") and hasattr(self.master.master, "actualizar_logs_visuales"):
                    self.master.master.actualizar_logs_visuales(f"ACTUALIZADO: Cliente [{id_cliente}] modificado.")
                self.salir_modo_edicion()
            else:
                messagebox.showinfo("Éxito", "El cliente ha sido registrado correctamente.")
                if hasattr(self.master, "master") and hasattr(self.master.master, "actualizar_logs_visuales"):
                    self.master.master.actualizar_logs_visuales(f"REGISTRADO: Cliente [{id_cliente}] guardado.")
                self.limpiar_campos()

            self.actualizar_vista_tarjetas()
        # Manejo de excepciones específicas para errores de validación y errores inesperados, mostrando mensajes de error al usuario y registrando los errores en el sistema de logs
        except datosInvalidosError as error_validacion:
            messagebox.showerror("Datos Inválidos", str(error_validacion))
            if hasattr(self.master, "master") and hasattr(self.master.master, "actualizar_logs_visuales"):
                self.master.master.actualizar_logs_visuales(f"VALIDACIÓN: {str(error_validacion)}")
            logger.registrar_error("Fallo de validación en formulario cliente", error_validacion)
        # Manejo de excepciones generales para capturar cualquier error inesperado durante el proceso de registro o actualización del cliente
        except Exception as error_inesperado:
            messagebox.showerror("Error del Sistema", "Ocurrió una anomalía interna.")
            logger.registrar_error("Excepción no controlada en clientes", error_inesperado)

    # Función para eliminar un cliente del diccionario de clientes, mostrando un mensaje de confirmación antes de proceder con la eliminación
    def eliminar_cliente(self, id_cliente):
        """Elimina un cliente del diccionario con confirmación del usuario.
        
        Parámetros:
            id_cliente: Identificación del cliente a eliminar
        
        Proceso:
        1. Valida que el cliente exista en diccionario
        2. Muestra diálogo de confirmación al usuario
        3. Si se confirma:
           - Cancela edición si cliente estaba siendo editado
           - Elimina del diccionario
           - Actualiza vista visual
           - Registra en logs del sistema
        4. Captura excepciones inesperadas
        
        Alineación con requerimientos:
        - VALIDACIÓN: Confirmación del usuario antes de acción destructiva
        - EXCEPCIONES: Try-except con manejo de errores y logging
        - LOGGING: Registra eliminación en actualizar_logs_visuales()
        - NOMENCLATURA: Usa snake_case (id_cliente, mensaje_log, etc.)
        """
        cliente = self.clientes_dict.get(id_cliente)
        if not cliente:
            return

        confirmacion = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de que desea eliminar al cliente:\n\n👉 {cliente.nombre} (ID: {id_cliente})?\n\nEsta acción no se puede deshacer.",
        )

        if confirmacion:
            try:
                if self.id_en_edicion == id_cliente:
                    self.salir_modo_edicion()

                del self.clientes_dict[id_cliente]
                self.actualizar_vista_tarjetas()

                mensaje_log = f"Cliente [{id_cliente}] - {cliente.nombre} eliminado correctamente."
                if hasattr(self.master, "master") and hasattr(self.master.master, "actualizar_logs_visuales"):
                    self.master.master.actualizar_logs_visuales(f"ELIMINADO: {mensaje_log}")

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el cliente: {str(e)}")
                if hasattr(self.master, "master") and hasattr(self.master.master, "actualizar_logs_visuales"):
                    self.master.master.actualizar_logs_visuales(f"ERROR: Fallo al intentar eliminar ID {id_cliente}")

    # Función para limpiar los campos del formulario, eliminando cualquier texto ingresado en los campos de identificación, nombre y correo electrónico
    def limpiar_campos(self):
        """Limpia todos los campos de entrada del formulario.
        
        Campos afectados:
        - entrada_id
        - entrada_nombre
        - entrada_email
        
        Alineación con requerimientos:
        - NOMENCLATURA: Utiliza snake_case en nombres de atributos (entrada_id, etc.)
        - UTILIDAD: Invocada tras registros exitosos y al cancelar edición
        """
        self.entrada_id.delete(0, tk.END)
        self.entrada_nombre.delete(0, tk.END)
        self.entrada_email.delete(0, tk.END)
