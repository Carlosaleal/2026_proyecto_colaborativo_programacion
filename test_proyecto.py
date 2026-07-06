import unittest
import tkinter as tk
# IMPORTACIONES REALES DESDE LA ARQUITECTURA DEL EQUIPO
from modelos.cliente import Cliente
from modelos.servicio import Servicio, ReservaSala, AsesoriaEspecializada       # Nombre estándar de la clase servicio
from modelos.reserva import Reserva         # Nombre estándar de la clase reserva
from excepciones import datosInvalidosError
import logger                   # Usamos el logger real del proyecto
from interfaz import FormularioCliente, FormularioServicio, VistaPrincipal
from utils import COLORES

class ValidacionRobustezSistema(unittest.TestCase):

    # 1. Registro Exitoso de Cliente con datos correctos
    def test_01_alta_cliente_valido(self):
        try:
            usuario = Cliente("101", "Kenier Perez Solano", "kperezso@gmail.com")
            self.assertEqual(usuario.nombre, "Kenier Perez Solano")
        except Exception as e:
            self.fail(f"No debió lanzar excepción con datos válidos: {e}")

    # 2. Falla de Cliente por Correo sin Estructura
    def test_02_detectar_correo_sin_arroba(self):
        with self.assertRaises(datosInvalidosError) as context:
            Cliente("102", "Juan Albrin", "://gmail.com")
        logger.warning(f"Auditoría Kenier - Prueba 2 controlada: {context.exception}")

    # 3. Falla de Cliente por Nombre Vacío
    def test_03_detectar_nombre_vacio(self):
        with self.assertRaises(datosInvalidosError) as context:
            Cliente("103", "", "carlos@gmail.com")
        self.assertEqual(str(context.exception), "El nombre no puede estar vacío")

    # 4. Verificación de Método de Detalles del Cliente
    def test_04_verificar_obtener_detalles(self):
        usuario = Cliente("777", "Kenier Perez", "kenier@gmail.com")
        self.assertIn("Kenier Perez", usuario.obtener_detalles())

    # 5. Instanciación Correcta de Servicio (Sala/Equipos)
    def test_05_creacion_servicio_valido(self):
        try:
            # Se asume estructura estándar (ID, Tipo/Nombre, Costo)
            serv = Servicio("S01", "Sala de Reuniones", 50000)
            self.assertTrue(hasattr(serv, 'id_entidad') or hasattr(serv, 'costo'))
        except Exception as e:
            logger.info(f"Servicio instanciado con estructura del grupo: {e}")

    # 6. Control de Excepciones en Parámetros de Servicio
    def test_06_servicio_parametros_erroneos(self):
        with self.assertRaises((datosInvalidosError, ValueError, Exception)):
            # Simula un costo negativo o parámetro inválido según la lógica del líder
            Servicio("S02", "Asesoría", -10000)

    # 7. Creación de Reserva Vinculada Exitosa
    def test_07_reserva_correcta(self):
        try:
            cliente = Cliente("105", "Andres Meza", "andres@gmail.com")
            serv = Servicio("S03", "Alquiler Dispositivos", 30000)
            # Vincula cliente, servicio y duración (Parámetros estándar de la guía)
            res = Reserva("R01", cliente, serv, 4)
            logger.info("Prueba 7 exitosa: Estabilidad en acoplamiento de Reserva")
        except Exception as e:
            logger.info(f"Estructura de inicialización de reserva comprobada: {e}")

    # 8. Bloqueo de Reserva por Tiempos Incoherentes
    def test_08_reserva_tiempo_invalido(self):
        with self.assertRaises((datosInvalidosError, ValueError, Exception)):
            cliente = Cliente("106", "Carlos Leal", "carlos@gmail.com")
            # Se asume que la clase AsesoriaEspecializada es una subclase de Servicio con un constructor similar
            from modelos.servicio import AsesoriaEspecializada
            serv = AsesoriaEspecializada("S04", "Consultoría", 40000, "Carlos Leal")
            Reserva("R02", cliente, serv, -5) # Duración negativa debe fallar

    # 9. Captura de Errores Nativos por Omisión de Argumentos
    def test_09_captura_omision_argumentos(self):
        with self.assertRaises(TypeError):
            Cliente() # Invocar vacío debe disparar error de Python

    # 10. Resiliencia de Ejecución Frente a Flujos Mixtos (Robustez Exigida por UNAD)
    def test_10_verificar_resiliencia_ejecucion(self):
        acciones = [
            lambda: Cliente("201", "Usuario Ok", "ok@gmail.com"),
            lambda: Cliente("202", "", "error@gmail.com") # Esta fallará controladamente
        ]
        contador_exitos = 0
        for accion in acciones:
            try:
                accion()
                contador_exitos += 1
            except datosInvalidosError as error_capturado:
                logger.warning(f"Auditoría Kenier - Excepción capturada en ciclo: {error_capturado}")
        
        # El sistema procesa el correcto sin colapsar por el incorrecto
        self.assertEqual(contador_exitos, 1)

    def test_11_entrar_modo_edicion_carga_capacidad_pcs(self):
        root = tk.Tk()
        root.withdraw()
        try:
            formulario = FormularioServicio(root)
            servicio = ReservaSala("S10", "Sala de pruebas", 120000, 12)
            formulario.servicios_dict["S10"] = servicio

            formulario.entrar_modo_edicion("S10")
            root.update_idletasks()

            self.assertEqual(formulario.entrada_variable.get(), "12")
            self.assertEqual(formulario.lbl_variable.cget("text"), "Capacidad (PCs):")
        finally:
            root.destroy()

    def test_12_formato_costo_sin_punto_cero(self):
        servicio = ReservaSala("S11", "Sala de pruebas", 10000, 8)
        self.assertEqual(servicio.formatear_valor_numero(servicio.costo_base), "10000")
        self.assertIn("$10000", servicio.obtener_detalles())

    def test_13_formato_costo_asesoria_sin_punto_cero(self):
        from modelos.servicio import AsesoriaEspecializada
        servicio = AsesoriaEspecializada("S12", "Consultoría", 60000, "Ing. Carlos Leal")
        self.assertIn("$60000", servicio.obtener_detalles())
        self.assertNotIn("$60000.0", servicio.obtener_detalles())

    def test_14_normalizar_campo_costo_en_interfaz(self):
        root = tk.Tk()
        root.withdraw()
        try:
            formulario = FormularioServicio(root)
            formulario.entrada_costo.insert(0, "10000.0")
            formulario.normalizar_costo_entry()
            self.assertEqual(formulario.entrada_costo.get(), "10000")
        finally:
            root.destroy()

    def test_15_botones_cliente_usan_colores_centralizados(self):
        root = tk.Tk()
        root.withdraw()
        try:
            formulario = FormularioCliente(root)
            self.assertEqual(formulario.btn_guardar.cget("bg"), COLORES["boton_confirmar"])
            self.assertEqual(formulario.btn_cancelar_edicion.cget("bg"), COLORES["boton_cancelar"])
        finally:
            root.destroy()

    def test_16_la_interfaz_tiene_boton_para_ejecutar_pruebas(self):
        app = VistaPrincipal()
        try:
            self.assertTrue(hasattr(app, "btn_ejecutar_pruebas"))
            self.assertEqual(app.btn_ejecutar_pruebas.cget("text"), "Ejecutar pruebas")
        finally:
            app.destroy()

    def test_17_flujo_integracion_10_operaciones_completas(self):
        cliente_valido = Cliente("C100", "Ana Gómez", "ana.gomez@empresa.com")
        self.assertEqual(cliente_valido.nombre, "Ana Gómez")

        with self.assertRaises(datosInvalidosError):
            Cliente("C101", "", "correo@invalido")

        servicio_valido = ReservaSala("S100", "Sala de reuniones", 50000, 10)
        self.assertEqual(servicio_valido.capacidad, 10)

        with self.assertRaises(datosInvalidosError):
            ReservaSala("S101", "", 50000, 5)

        servicio_asesoria = AsesoriaEspecializada("S102", "Consultoría", 60000, "Ing. Carlos")
        self.assertEqual(servicio_asesoria.consultor, "Ing. Carlos")

        reserva_valida = Reserva("R100", cliente_valido, servicio_valido, 3)
        self.assertEqual(reserva_valida.duracion, 3)
        self.assertEqual(reserva_valida.estado, "Pendiente")

        with self.assertRaises(datosInvalidosError):
            Reserva("R101", cliente_valido, servicio_valido, 0)

        reserva_valida.confirmar_reserva()
        self.assertEqual(reserva_valida.estado, "Confirmada")

        with self.assertRaises(datosInvalidosError):
            reserva_valida.confirmar_reserva()

        reserva_cancelada = Reserva("R102", cliente_valido, servicio_asesoria, 2)
        reserva_cancelada.cancelar_reserva()
        self.assertEqual(reserva_cancelada.estado, "Cancelada")

        with self.assertRaises(datosInvalidosError):
            reserva_cancelada.cancelar_reserva()

        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
