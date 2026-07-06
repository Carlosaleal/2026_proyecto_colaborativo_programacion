# Autor: Carlos Andres Leal
# Formulario de registro y edición de servicios en la aplicación de gestión de servicios.

# importaciones de módulos estándar
import os
import sys

directorio_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if directorio_raiz not in sys.path:
    sys.path.append(directorio_raiz)

import tkinter as tk
from tkinter import messagebox, ttk

import logger
from modelos.servicio import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from excepciones import datosInvalidosError
from utils import (
    FUENTE_LABEL,
    FUENTE_LABEL_2,
    FUENTE_BOTON,
    DATOS_EJEMPLO_SERVICIOS,
    COLORES,
)

# Clase FormularioServicio: Representa el formulario de registro y edición de servicios.
class FormularioServicio(tk.Frame):
    """Formulario para la gestión integral de servicios (CRUD) con soporte para tres tipos.
    
    Tipos de Servicios soportados:
    - Sala de Cómputo (ReservaSala): Gestiona capacidad en PCs
    - Alquiler de Equipos (AlquilerEquipo): Gestiona marca/modelo
    - Asesoría Especializada (AsesoriaEspecializada): Gestiona consultor
    
    Funcionalidades:
    - Registro de nuevos servicios con tipo dinámico
    - Visualización en catálogo con scroll
    - Edición de servicios existentes
    - Eliminación con confirmación
    
    Estructura UI:
    - Panel izquierdo: Formulario con combo dinámico de tipo de servicio
    - Panel derecho: Catálogo de servicios en tarjetas
    
    Alineación con requerimientos:
    - VALIDACIÓN: Manejo de datosInvalidosError para datos inválidos
    - EXCEPCIONES: Try-except con logging en logger
    - MODULARIZACIÓN: Integra modelos ReservaSala, AlquilerEquipo, AsesoriaEspecializada
    - NOMENCLATURA: Métodos y atributos con snake_case
    - CONSTANTES: FUENTE_LABEL, FUENTE_BOTON, COLORES (UPPERCASE de utils)
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        """Inicializa el formulario de servicios con paneles de entrada y catálogo.
        
        Parámetros:
            parent (tk.Widget): Widget padre (generalmente un ttk.Notebook)
        
        Alineación con requerimientos:
        - ESTRUCTURA: Crea panel izquierdo (input) y panel derecho (catálogo)
        - ALMACENAMIENTO: Inicializa servicios_dict para CRUD (snake_case)
        - UI: Configura canvas con scrollbar para múltiples servicios
        - DATOS DEMO: Carga datos desde DATOS_EJEMPLO_SERVICIOS (constante UPPERCASE)
        - MODULARIZACIÓN: Instancia modelos específicos (ReservaSala, AlquilerEquipo, AsesoriaEspecializada)
        """

        # ALMACENAMIENTO: diccionario de servicios y estado de edición (deben existir
        # ANTES de llamar a crear_formulario/cargar_datos_demostracion/actualizar_vista_tarjetas)
        self.servicios_dict = {}
        self.id_en_edicion = None

        self.panel_izq = tk.LabelFrame(self, text=" Registrar / Modificar Servicio ", font=FUENTE_LABEL, padx=10, pady=10)
        self.panel_izq.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.panel_der = tk.LabelFrame(self, text=" Catálogo de Servicios ", font=FUENTE_LABEL, padx=10, pady=10)
        self.panel_der.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        self.canvas = tk.Canvas(self.panel_der, borderwidth=0, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.panel_der, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=10)

        self.crear_formulario()
        self.cargar_datos_demostracion()
        self.actualizar_vista_tarjetas()

    # Funciones de la clase FormularioServicio
    def crear_formulario(self):
        """Construye los campos de entrada del formulario en el panel izquierdo.
        
        Campos creados:
        - Entrada de Código de Servicio
        - Combo de Tipo de Servicio (Sala, Alquiler, Asesoría) - DINÁMICO
        - Entrada de Nombre/Descripción
        - Entrada de Costo Base (con validación numérica)
        - Entrada Variable (cambia etiqueta según tipo: Capacidad, Marca, Consultor)
        - Botones Registrar/Actualizar y Cancelar
        
        Alineación con requerimientos:
        - NOMENCLATURA: Atributos snake_case (entrada_id, combo_tipo, entrada_variable, etc.)
        - VALIDACIÓN: entrada_costo con normalizar_costo_entry() para formato numérico
        - DINAMISMO: combo_tipo.bind() llama adaptar_campo_dinamico() para cambiar etiquetas
        - CONSTANTES: Utiliza FUENTE_LABEL_2, FUENTE_BOTON, COLORES (UPPERCASE)
        """
        tk.Label(self.panel_izq, text="Código Servicio:", font=FUENTE_LABEL_2).grid(row=0, column=0, sticky="e", pady=5)
        self.entrada_id = tk.Entry(self.panel_izq, width=25)
        self.entrada_id.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        tk.Label(self.panel_izq, text="Tipo de Servicio:", font=FUENTE_LABEL_2).grid(row=1, column=0, sticky="e", pady=5)
        # Combobox para seleccionar el tipo de servicio
        self.combo_tipo = ttk.Combobox(
            self.panel_izq,
            width=22,
            values=["Sala de Cómputo", "Alquiler de Equipos", "Asesoría Especializada"],
            state="readonly",
        )
        self.combo_tipo.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.combo_tipo.current(0)
        self.combo_tipo.bind("<<ComboboxSelected>>", lambda e: self.adaptar_campo_dinamico())

        tk.Label(self.panel_izq, text="Nombre/Descripción:", font=FUENTE_LABEL_2).grid(row=2, column=0, sticky="e", pady=5)
        self.entrada_nombre = tk.Entry(self.panel_izq, width=25)
        self.entrada_nombre.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.panel_izq, text="Costo Base ($):", font=FUENTE_LABEL_2).grid(row=3, column=0, sticky="e", pady=5)
        self.entrada_costo = tk.Entry(self.panel_izq, width=25)
        self.entrada_costo.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.entrada_costo.bind("<FocusOut>", self.normalizar_costo_entry)
        self.entrada_costo.bind("<Return>", self.normalizar_costo_entry)

        self.lbl_variable = tk.Label(self.panel_izq, text="Capacidad (PCs):", font=FUENTE_LABEL_2)
        self.lbl_variable.grid(row=4, column=0, sticky="e", pady=5)
        self.entrada_variable = tk.Entry(self.panel_izq, width=25)
        self.entrada_variable.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        self.btn_guardar = tk.Button(
            self.panel_izq,
            text="Registrar",
            font=FUENTE_BOTON,
            command=self.procesar_registro_servicio,
            bg=COLORES["boton_confirmar"],
            fg=COLORES["texto_blanco"],
        )
        self.btn_guardar.grid(row=5, column=1, pady=10, sticky="w")

        self.btn_cancelar_edicion = tk.Button(
            self.panel_izq,
            text="Cancelar",
            font=FUENTE_BOTON,
            command=self.salir_modo_edicion,
            bg=COLORES["boton_cancelar"],
            fg=COLORES["texto_blanco"],
        )
        self.btn_cancelar_edicion.grid(row=6, column=1, pady=5, sticky="w")
        self.btn_cancelar_edicion.grid_remove()

    # Función para adaptar el campo variable según el tipo de servicio seleccionado
    def adaptar_campo_dinamico(self):
        """Adapta dinámicamente la etiqueta del campo variable según tipo de servicio.
        
        Mapeos:
        - Sala de Cómputo → \"Capacidad (PCs):\"
        - Alquiler de Equipos → \"Marca / Modelo:\"
        - Asesoría Especializada → \"Consultor:\"
        
        Alineación con requerimientos:
        - DINAMISMO: UI reactiva según selección en combo_tipo
        - USABILIDAD: Guía al usuario sobre el campo a llenar
        - VINCULACIÓN: Vinculada mediante bind() del combo_tipo
        """
        tipo = self.combo_tipo.get()
        if tipo == "Sala de Cómputo":
            self.lbl_variable.config(text="Capacidad (PCs):")
        elif tipo == "Alquiler de Equipos":
            self.lbl_variable.config(text="Marca / Modelo:")
        elif tipo == "Asesoría Especializada":
            self.lbl_variable.config(text="Consultor:")

    # Función para normalizar el valor del costo ingresado en el formulario
    def normalizar_costo_entry(self, event=None):
        """Normaliza y formatea el valor de costo ingresado por el usuario.
        
        Proceso:
        1. Obtiene texto del campo entrada_costo
        2. Valida que sea número válido
        3. Formatea según decimales:
           - Enteros: muestra como \"100\"
           - Decimales: muestra como \"99.99\" (sin ceros al final)
        4. Actualiza el campo con valor formateado
        
        Eventos vinculados:
        - FocusOut: Cuando el usuario sale del campo
        - Return: Cuando el usuario presiona Enter
        
        Alineación con requerimientos:
        - VALIDACIÓN: Verifica que entrada sea número válido
        - UX: Presenta formato consistente de moneda (CONSTANTE formatear_moneda)
        - EXCEPCIONES: Captura ValueError silenciosamente si no es número
        """
        texto = self.entrada_costo.get().strip()
        if not texto:
            return

        try:
            numero = float(texto)
        except ValueError:
            return

        if numero.is_integer():
            texto_formateado = str(int(numero))
        else:
            texto_formateado = f"{numero:.2f}".rstrip("0").rstrip(".")

        self.entrada_costo.delete(0, tk.END)
        self.entrada_costo.insert(0, texto_formateado)

    # Función para cargar datos de demostración en el diccionario de servicios
    def cargar_datos_demostracion(self):
        """Carga datos de ejemplo en el diccionario de servicios para demostración.
        
        Fuente de datos:
        - Constante DATOS_EJEMPLO_SERVICIOS importada de utils (UPPERCASE)
        - Formato tupla: (id, tipo, nombre, costo, extra)
        
        Creación de modelos:
        - \"Sala de Cómputo\" → ReservaSala(id, nombre, costo, capacidad_pcs)
        - \"Alquiler de Equipos\" → AlquilerEquipo(id, nombre, costo, marca_modelo)
        - \"Asesoría Especializada\" → AsesoriaEspecializada(id, nombre, costo, consultor)
        
        Alineación con requerimientos:
        - MODULARIZACIÓN: Instancia modelos específicos del módulo modelos.servicio
        - CONSTANTES: Utiliza DATOS_EJEMPLO_SERVICIOS (UPPERCASE de utils)
        - VALIDACIÓN: Convierte costo a float con manejo de excepciones
        - ALMACENAMIENTO: Popula servicios_dict para visualización
        """
        for sid, tipo, nombre, costo, extra in DATOS_EJEMPLO_SERVICIOS:
            try:
                costo_f = float(costo)
                if tipo == "Sala de Cómputo":
                    self.servicios_dict[sid] = ReservaSala(sid, nombre, costo_f, int(extra))
                elif tipo == "Alquiler de Equipos":
                    self.servicios_dict[sid] = AlquilerEquipo(sid, nombre, costo_f, extra)
                elif tipo == "Asesoría Especializada":
                    self.servicios_dict[sid] = AsesoriaEspecializada(sid, nombre, costo_f, extra)
            except Exception as e:
                logger.registrar_error("Error inyectando datos de demostración en servicios", e)

    # Función para actualizar la vista de tarjetas de servicios en el panel derecho
    def actualizar_vista_tarjetas(self):
        """Refresca la visualización de servicios como tarjetas en el panel derecho.
        
        Proceso:
        1. Limpia widgets previos del scrollable_frame
        2. Si no hay servicios, muestra mensaje de vacío
        3. Itera servicios_dict y crea tarjeta para cada uno
        4. Llama obtener_detalles() de cada servicio para mostrar info formateada
        5. Agrega botones Editar y Eliminar con comandos asociados
        
        Alineación con requerimientos:
        - VALIDACIÓN: Verifica si servicios_dict está vacío
        - CONSTANTES: Aplica COLORES desde utils para consistencia visual
        - MODULARIZACIÓN: Utiliza método obtener_detalles() de modelos de servicio
        - INTERACTIVIDAD: Vincula botones a entrar_modo_edicion() y eliminar_servicio()
        """
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        # Si no hay servicios registrados, mostrar un mensaje informativo
        if not self.servicios_dict:
            tk.Label(self.scrollable_frame, text="No hay servicios registrados.", font=("Helvetica", 10, "italic"), fg="gray").pack(pady=20)
            return

        for id_serv, serv in self.servicios_dict.items():
            tarjeta = tk.Frame(self.scrollable_frame, bd=1, relief="ridge", bg=COLORES["fondo_primario"], padx=10, pady=8)
            tarjeta.pack(fill=tk.X, padx=5, pady=4, expand=True)
            tarjeta.grid_columnconfigure(0, weight=1)
            tarjeta.grid_columnconfigure(1, weight=0)

            detalles = serv.obtener_detalles()
            lbl_info = tk.Label(
                tarjeta,
                text=detalles,
                font=("Helvetica", 10),
                bg=COLORES["fondo_primario"],
                justify="left",
                anchor="w",
                wraplength=380,
            )
            lbl_info.grid(row=0, column=0, sticky="w", padx=(0, 10))

            frame_botones = tk.Frame(tarjeta, bg=COLORES["fondo_primario"])
            frame_botones.grid(row=0, column=1, sticky="e")

            tk.Button(
                frame_botones,
                text="Editar",
                font=("Helvetica", 9),
                bg=COLORES["estado_pendiente"],
                fg=COLORES["texto_blanco"],
                bd=0,
                padx=6,
                pady=3,
                cursor="hand2",
                command=lambda s_id=id_serv: self.entrar_modo_edicion(s_id),
            ).pack(side="left", padx=2)

            tk.Button(
                frame_botones,
                text="Eliminar",
                font=("Helvetica", 9),
                bg=COLORES["boton_cancelar"],
                fg=COLORES["texto_blanco"],
                bd=0,
                padx=6,
                pady=3,
                cursor="hand2",
                command=lambda s_id=id_serv: self.eliminar_servicio(s_id),
            ).pack(side="left", padx=2)

    # Función para procesar el registro o actualización de un servicio
    def procesar_registro_servicio(self):
        """Registra un nuevo servicio o actualiza uno existente con validación completa.
        
        Proceso:
        1. Obtiene valores de campos (ID, Nombre, Costo, Campo Variable)
        2. Determina tipo de servicio (Sala, Alquiler, Asesoría)
        3. VALIDACIÓN: Verifica campos obligatorios
        4. VALIDACIÓN: Comprueba duplicados en servicios_dict
        5. VALIDACIÓN: Convierte costo a float
        6. VALIDACIÓN: Para Sala, convierte capacidad a int
        7. Crea instancia de modelo específico (ReservaSala, AlquilerEquipo, AsesoriaEspecializada)
        8. Almacena en servicios_dict
        9. Actualiza vista y registra en logs
        
        Excepciones manejadas:
        - datosInvalidosError: Campos vacíos, duplicados, conversiones numéricas
        - Exception: Errores inesperados del sistema
        
        Alineación con requerimientos:
        - VALIDACIÓN: Múltiples niveles de validación con mensajes descriptivos
        - EXCEPCIONES: Try-except con logging en logger.registrar_error()
        - MODULARIZACIÓN: Instancia modelos específicos según tipo
        - LOGGING: Integra con actualizar_logs_visuales() del sistema
        - NOMENCLATURA: Usa snake_case en variables (id_serv, costo_raw, etc.)
        """
        # Obtener los datos del formulario
        if self.id_en_edicion:
            id_serv = self.id_en_edicion
        else:
            id_serv = self.entrada_id.get().strip()

        nombre = self.entrada_nombre.get().strip()
        costo_raw = self.entrada_costo.get().strip()
        extra = self.entrada_variable.get().strip()
        # Determinar el tipo de servicio basado en la edición o selección del combobox
        if self.id_en_edicion:
            servicio_existente = self.servicios_dict.get(self.id_en_edicion)
            if isinstance(servicio_existente, ReservaSala):
                tipo = "Sala de Cómputo"
            elif isinstance(servicio_existente, AlquilerEquipo):
                tipo = "Alquiler de Equipos"
            elif isinstance(servicio_existente, AsesoriaEspecializada):
                tipo = "Asesoría Especializada"
            else:
                tipo = self.combo_tipo.get()
        else:
            tipo = self.combo_tipo.get()

        self.normalizar_costo_entry()
        # Validación de datos y creación del servicio
        try:
            if not id_serv or not nombre or not costo_raw or not extra:
                raise datosInvalidosError("Todos los campos del servicio son obligatorios.")

            if not self.id_en_edicion and id_serv in self.servicios_dict:
                raise datosInvalidosError(f"El identificador de servicio '{id_serv}' ya se encuentra registrado.")

            try:
                costo_f = float(costo_raw)
            except ValueError:
                raise datosInvalidosError("El costo base debe ser un número válido.")

            if tipo == "Sala de Cómputo":
                try:
                    capacidad = int(extra)
                except ValueError:
                    raise datosInvalidosError("La capacidad de computadores debe ser un número entero.")
                nuevo_servicio = ReservaSala(id_serv, nombre, costo_f, capacidad)
            elif tipo == "Alquiler de Equipos":
                nuevo_servicio = AlquilerEquipo(id_serv, nombre, costo_f, extra)
            elif tipo == "Asesoría Especializada":
                nuevo_servicio = AsesoriaEspecializada(id_serv, nombre, costo_f, extra)
            else:
                raise datosInvalidosError("Tipo de servicio no reconocido.")

            self.servicios_dict[id_serv] = nuevo_servicio

            if self.id_en_edicion:
                messagebox.showinfo("Éxito", "El servicio ha sido actualizado correctamente.")
                if hasattr(self.master, "master") and hasattr(self.master.master, "actualizar_logs_visuales"):
                    self.master.master.actualizar_logs_visuales(f"ACTUALIZADO: Servicio [{id_serv}] modificado.")
                self.salir_modo_edicion()
            else:
                messagebox.showinfo("Éxito", "El servicio ha sido registrado correctamente.")
                if hasattr(self.master, "master") and hasattr(self.master.master, "actualizar_logs_visuales"):
                    self.master.master.actualizar_logs_visuales(f"REGISTRADO: Servicio [{id_serv}] guardado.")
                self.limpiar_campos()

            self.actualizar_vista_tarjetas()

        except datosInvalidosError as err:
            messagebox.showerror("Datos Inválidos", str(err))
            if hasattr(self.master, "master") and hasattr(self.master.master, "actualizar_logs_visuales"):
                self.master.master.actualizar_logs_visuales(f"VALIDACIÓN: {str(err)}")
            logger.registrar_error("Fallo de validación en formulario servicio", err)

    # Función para entrar en modo edición de un servicio existente
    def entrar_modo_edicion(self, id_servicio):
        """Carga los datos de un servicio en el formulario para edición.
        
        Parámetros:
            id_servicio: Identificación del servicio a editar
        
        Acciones:
        1. Obtiene objeto servicio del diccionario
        2. Carga datos en campos de entrada (ID deshabilitado, otros editables)
        3. Detecta tipo de servicio (isinstance) y ajusta etiqueta del campo variable
        4. Deshabilita combo_tipo para evitar cambios de tipo en edición
        5. Llama adaptar_campo_dinamico() para actualizar etiquetas
        
        Alineación con requerimientos:
        - MANEJO DE ESTADO: Utiliza id_en_edicion para rastrear servicio en edición
        - VALIDACIÓN: Retorna silenciosamente si servicio no existe
        - MODULARIZACIÓN: Utiliza isinstance() para identificar tipo de modelo
        - NOMENCLATURA: Usa snake_case (id_en_edicion, id_servicio, etc.)
        """
        serv = self.servicios_dict.get(id_servicio)
        if not serv:
            return

        self.id_en_edicion = id_servicio
        self.entrada_id.delete(0, tk.END)
        self.entrada_nombre.delete(0, tk.END)
        self.entrada_costo.delete(0, tk.END)
        self.entrada_variable.delete(0, tk.END)

        self.entrada_id.insert(0, serv.id_entidad)
        self.entrada_id.config(state="disabled")
        self.entrada_nombre.insert(0, serv.nombre_servicio)
        self.entrada_costo.insert(0, serv.formatear_valor_numero(serv.costo_base))

        # Adaptar el campo variable según el tipo de servicio
        if isinstance(serv, ReservaSala):
            self.combo_tipo.set("Sala de Cómputo")
            self.lbl_variable.config(text="Capacidad (PCs):")
            self.entrada_variable.insert(0, str(getattr(serv, "capacidad", "")))
        elif isinstance(serv, AlquilerEquipo):
            self.combo_tipo.set("Alquiler de Equipos")
            self.lbl_variable.config(text="Marca / Modelo:")
            self.entrada_variable.insert(0, str(getattr(serv, "marca_modelo", "")))
        elif isinstance(serv, AsesoriaEspecializada):
            self.combo_tipo.set("Asesoría Especializada")
            self.lbl_variable.config(text="Consultor:")
            self.entrada_variable.insert(0, str(getattr(serv, "consultor", "")))

        self.adaptar_campo_dinamico()
        self.combo_tipo.config(state="disabled")
        self.btn_guardar.config(text="Actualizar", bg=COLORES["boton_accion"], activebackground=COLORES["boton_accion"])
        self.btn_cancelar_edicion.grid()

    # Función para salir del modo edición y restaurar el formulario a su estado inicial
    def salir_modo_edicion(self):
        """Cancela el modo edición y restaura el formulario a su estado inicial.
        
        Acciones:
        1. Limpia id_en_edicion (establece en None)
        2. Habilita campo ID y combo_tipo para nuevos registros
        3. Limpia todos los campos de entrada
        4. Restaura botón Registrar con configuración inicial
        5. Oculta botón Cancelar
        
        Alineación con requerimientos:
        - VALIDACIÓN: Retorna formulario a estado seguro para nuevo registro
        - NOMENCLATURA: Usa snake_case en variables
        - CONSTANTES: Restaura colores originales desde COLORES
        """
        self.id_en_edicion = None
        self.entrada_id.config(state="normal")
        self.combo_tipo.config(state="readonly")
        self.limpiar_campos()
        self.btn_guardar.config(text="Registrar", bg=COLORES["boton_confirmar"], activebackground=COLORES["boton_confirmar"])
        self.btn_cancelar_edicion.grid_remove()

    # Función para eliminar un servicio del diccionario y actualizar la vista
    def eliminar_servicio(self, id_servicio):
        """Elimina un servicio del diccionario con confirmación del usuario.
        
        Parámetros:
            id_servicio: Identificación del servicio a eliminar
        
        Proceso:
        1. Valida que el servicio exista en diccionario
        2. Muestra diálogo de confirmación al usuario
        3. Si se confirma:
           - Cancela edición si servicio estaba siendo editado
           - Elimina del diccionario
           - Actualiza vista visual
           - Registra en logs del sistema
        
        Alineación con requerimientos:
        - VALIDACIÓN: Confirmación del usuario antes de acción destructiva
        - LOGGING: Registra eliminación en actualizar_logs_visuales()
        - NOMENCLATURA: Usa snake_case (id_servicio, id_en_edicion, etc.)
        """
        serv = self.servicios_dict.get(id_servicio)
        if not serv:
            return

        if messagebox.askyesno("Confirmar Eliminación", f"¿Seguro que desea eliminar el servicio:\n👉 {serv.nombre_servicio}?"):
            if self.id_en_edicion == id_servicio:
                self.salir_modo_edicion()
            del self.servicios_dict[id_servicio]
            self.actualizar_vista_tarjetas()
            if hasattr(self.master, "master") and hasattr(self.master.master, "actualizar_logs_visuales"):
                self.master.master.actualizar_logs_visuales(f"ELIMINADO: Servicio [{id_servicio}] removido.")

    # función para limpiar los campos del formulario y restaurar el estado inicial
    def limpiar_campos(self):
        """Limpia todos los campos de entrada del formulario.
        
        Campos afectados:
        - entrada_id
        - entrada_nombre
        - entrada_costo
        - entrada_variable
        
        Alineación con requerimientos:
        - NOMENCLATURA: Utiliza snake_case en nombres de atributos
        - UTILIDAD: Invocada tras registros exitosos y al cancelar edición
        """
        self.entrada_id.delete(0, tk.END)
        self.entrada_nombre.delete(0, tk.END)
        self.entrada_costo.delete(0, tk.END)
        self.entrada_variable.delete(0, tk.END)
        self.combo_tipo.current(0)
        self.adaptar_campo_dinamico()
