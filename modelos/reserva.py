from modelos.cliente import Cliente
from modelos.servicio import Servicio
from excepciones import datosInvalidosError

class Reserva:

    """
    Esta es la clase para gestionar el ciclo de vida de una reserva de servicio por parte de un cliente.
    """

    def __init__(self, id_reserva:str, cliente:Cliente, servicio:Servicio, duracion:int):
        self.id_reserva = id_reserva
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self._estado = "Pendiente" # Los estados que se manejarán son: Pendiente, Confirmada y Cancelada.

    @property
    def id_reserva(self) -> str:
        return self._id_reserva
        
    @id_reserva.setter
    def id_reserva(self, valor: str):
        if valor is None or str(valor).strip() == "":
            raise datosInvalidosError("El ID de la reserva no puede estar vacío.")
        self._id_reserva = str(valor).strip()

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @cliente.setter
    def cliente(self,valor:Cliente):
        if not isinstance(valor,Cliente):
            raise datosInvalidosError("El cliente asignado a la reserva debe ser una instancia válida de la clase Cliente.")
        self._cliente = valor
        
    @property
    def servicio(self) -> Servicio:
        return self._servicio
        
    @servicio.setter
    def servicio(self, valor:Servicio):
        """Método para validar si el servicio es soportado por el sistema"""
        if not isinstance(valor, Servicio):
            raise datosInvalidosError("El servicio asignado debe ser una instancia derivada de la clase abstracta Servicio.")
        self._servicio = valor
        
    @property
    def duracion(self) -> int:
        return self._duracion
        
    @duracion.setter
    def duracion(self, valor: int):
        """Método para validar la duración de la reserva"""
        try:
            valor_int=int(valor)
        except (ValueError, TypeError):
            raise datosInvalidosError("La duración de la reserva debe ser un número entero.")
            
        if valor_int <= 0:
            raise datosInvalidosError("La duración de la reserva debe ser estrictamente mayor a cero.")
        self._duracion = valor_int
        
    @property
    def estado(self) -> str:
        """Método para hacer inaccesible el estado de la reserva desde afuera"""
        return self._estado
        
    # Ahora bien, estos son algunos métodos para gestionar el flujo de la reserva:

    def confirmar_reserva(self):
        if self._estado == "Cancelada":
            raise datosInvalidosError("No se puede confirmar una reserva")
        if self._estado == "Confirmada":
            raise datosInvalidosError("La reserva ya se encuentra en estado 'Confirmada'.")
        self._estado = "Confirmada"
    
    def cancelar_reserva(self):
        """Método para verificar y actualizar el estado de la reservación del cliente a cancelada"""
        if self._estado == "Cancelada":
            raise datosInvalidosError("La reserva ya ha sido cancelada con anterioridad.")
        self._estado = "Cancelada"

    def obtener_costo_reserva(self,**kwargs) -> float:
        """
        Calcula de forma dinámica el costo invocado el polimorfismo de la clase Servicio,
        transmitiendo de este modo los argumentos extras requeridos para la sobrecarga simulación.
        """
        try:
            return self.servicio.calcular_costo(self.duracion,**kwargs)
        except Exception as e:
            # Aquí encadeno las excepciones si el cálculo falla internamente
            raise RuntimeError("Error crítico al procesar el costo de la reserva") from e
        
    def __str__(self):
        """Método para todo los detalles de la reserva, información del cliente y detalles del servicio"""
        return(f"Reserva {self.id_reserva} [{self._estado}]\n"
               f" Cliente: {self.cliente.nombre} ({self.cliente.id_entidad})\n"
               f" Servicio: {self.servicio.nombre_servicio} | Duración: {self.duracion}\n"
               f" Detalles Servicio: {self.servicio.obtener_detalles()}")
    
