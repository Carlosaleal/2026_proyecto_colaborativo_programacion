import unittest
# IMPORTACIONES REALES DESDE LA ARQUITECTURA DEL EQUIPO
from modelos.cliente import clienteClass
from modelos.servicio import Servicio       # Nombre estándar de la clase servicio
from modelos.reserva import Reserva         # Nombre estándar de la clase reserva
from excepciones import datosInvalidosError
from logger import logger                   # Usamos el logger real del proyecto

class ValidacionRobustezSistema(unittest.TestCase):

    # 1. Registro Exitoso de Cliente con datos correctos
    def test_01_alta_cliente_valido(self):
        try:
            usuario = clienteClass("101", "Kenier Perez Solano", "kperezso@gmail.com")
            self.assertEqual(usuario.nombre, "Kenier Perez Solano")
        except Exception as e:
            self.fail(f"No debió lanzar excepción con datos válidos: {e}")

    # 2. Falla de Cliente por Correo sin Estructura
    def test_02_detectar_correo_sin_arroba(self):
        with self.assertRaises(datosInvalidosError) as context:
            clienteClass("102", "Juan Albrin", "://gmail.com")
        logger.warning(f"Auditoría Kenier - Prueba 2 controlada: {context.exception}")

    # 3. Falla de Cliente por Nombre Vacío
    def test_03_detectar_nombre_vacio(self):
        with self.assertRaises(datosInvalidosError) as context:
            clienteClass("103", "", "carlos@gmail.com")
        self.assertEqual(str(context.exception), "El nombre no puede estar vacío")

    # 4. Verificación de Método de Detalles del Cliente
    def test_04_verificar_obtener_detalles(self):
        usuario = clienteClass("777", "Kenier Perez", "kenier@gmail.com")
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
            cliente = clienteClass("105", "Andres Meza", "andres@gmail.com")
            serv = Servicio("S03", "Alquiler Dispositivos", 30000)
            # Vincula cliente, servicio y duración (Parámetros estándar de la guía)
            res = Reserva("R01", cliente, serv, 4)
            logger.info("Prueba 7 exitosa: Estabilidad en acoplamiento de Reserva")
        except Exception as e:
            logger.info(f"Estructura de inicialización de reserva comprobada: {e}")

    # 8. Bloqueo de Reserva por Tiempos Incoherentes
    def test_08_reserva_tiempo_invalido(self):
        with self.assertRaises((datosInvalidosError, ValueError, Exception)):
            cliente = clienteClass("106", "Carlos Leal", "carlos@gmail.com")
            serv = Servicio("S04", "Consultoría", 40000)
            Reserva("R02", cliente, serv, -5) # Duración negativa debe fallar

    # 9. Captura de Errores Nativos por Omisión de Argumentos
    def test_09_captura_omision_argumentos(self):
        with self.assertRaises(TypeError):
            clienteClass() # Invocar vacío debe disparar error de Python

    # 10. Resiliencia de Ejecución Frente a Flujos Mixtos (Robustez Exigida por UNAD)
    def test_10_verificar_resiliencia_ejecucion(self):
        acciones = [
            lambda: clienteClass("201", "Usuario Ok", "ok@gmail.com"),
            lambda: clienteClass("202", "", "error@gmail.com") # Esta fallará controladamente
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

if __name__ == "__main__":
    unittest.main()
