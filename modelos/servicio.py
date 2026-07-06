from abc import abstractmethod
from modelos.entidad import Entidad
from excepciones import datosInvalidosError

class Servicio(Entidad):
    """
    Esta clase representará todos lo relacionado con servicios generales de Software
    """

    def __init__(self, id_entidad:str, nombre_servicio:str, costo_base:float):
        super().__init__(id_entidad)
        self.nombre_servicio = nombre_servicio
        self.costo_base = costo_base

    @staticmethod
    def formatear_valor_numero(valor: float) -> str:
        """Devuelve un número como texto sin mostrar .0 cuando es entero."""
        try:
            numero = float(valor)
        except (TypeError, ValueError):
            return str(valor)

        if numero.is_integer():
            return str(int(numero))

        texto = f"{numero:.2f}".rstrip("0").rstrip(".")
        return texto if texto else "0"

    @property
    def nombre_servicio(self) -> str:
        """Método por el cual se define el atributo nombre_servicio como no accesible desde afuera"""
        return self._nombre_servicio

    @nombre_servicio.setter
    def nombre_servicio(self, valor:str):
        """Metodo por el cual se validan los datos de entrada como el valor del costo_base"""
        if valor is None or str(valor).strip()=="":
            raise datosInvalidosError("El nombre del servicio no puede estar vacío.") # Manejo de los errores con el archivo para los log y novedades
        self._nombre_servicio = str(valor).strip()
        
    @property
    def costo_base(self) -> float:
        """Método por el cual se define el atributo costo_base como no accesible desde afuera"""
        return self._costo_base
    
    @costo_base.setter
    def costo_base(self, valor: float):
        """Metodo por el cual se validan los datos de entrada como el valor del costo_base"""
        try:
            valor_float = float(valor)
        except (ValueError, TypeError):
            raise datosInvalidosError("El costo base debe ser un valor númerico válido.")
           
        if valor_float < 0:
            raise datosInvalidosError("El costo base no puede ser negativo.")
        self._costo_base = valor_float

    @abstractmethod
    def calcular_costo(self, duracion:int, **kwargs) -> float:
        """
        Este metodo es para calcular el costo en función de la duración (horas o días) y 
        entre otros parámetros opcionales (simulando sobrecarga)
        """
        pass

class ReservaSala(Servicio):
    """
    Servicio para salas físicas o virtuales.
    """

    def __init__(self, id_entidad:str, nombre_servicio: str, costo_base:float, capacidad:int):
        super().__init__(id_entidad, nombre_servicio, costo_base)
        self.capacidad = capacidad

    def calcular_costo(self, duracion:int, descuento: float = 0.0, impuesto:float=0.0) -> float:
        """ Método para validar que el y calcular el costo de la reserva"""
        if duracion <= 0:
            raise datosInvalidosError("La duración de la reserva de la sala debe ser mayor a 0 horas.")
            
        costo_total = self.costo_base * duracion
        if descuento > 0:
            costo_total -= costo_total * (descuento/100)
        if impuesto > 0:
            costo_total += costo_total * (impuesto/100)
            
        return round(costo_total, 2)
        
    def obtener_detalles(self)->str:
            """Método universal y polimorfico por el cual se obtienen los datos de la reserva"""
            return f"[Sala] ID: {self.id_entidad} | {self.nombre_servicio} | Capacidad: {self.capacidad} pers. | Costo/Hora: ${self.formatear_valor_numero(self.costo_base)}"
    
class AlquilerEquipo(Servicio):
    """Servicio especializado en alquiler de hardware o infraestructurasss"""

    def __init__(self, id_entidad: str, nombre_servicio: str, costo_base: float, marca_modelo:str):
        super().__init__(id_entidad, nombre_servicio, costo_base)
        self.marca_modelo = marca_modelo

    def calcular_costo(self, duracion: int, seguro_opcional: bool = False) -> float:
        """Método para calcular el costo del alquiler del equipo hardware o la infraestructurada alquilada"""
        if duracion <= 0:
            raise datosInvalidosError("La duración del alquiler del equipo debe ser de al menos 1 día.") # Se valida que el valor sea de 1 o más
        
        costo_total = self.costo_base * duracion # Se calcula el costo
        if seguro_opcional:
            costo_total +=15000.0 # Valor fijo para el seguro, el cual es opcional, es decir, si el cliente desea o no activarlo
        return round(costo_total, 2)
    
    def obtener_detalles(self):
        return f"[Equipo] ID: {self.id_entidad} | {self.nombre_servicio} ({self.marca_modelo}) | Costo/Día: ${self.formatear_valor_numero(self.costo_base)}"
    
class AsesoriaEspecializada(Servicio):
    """
    Servicio especializado en consultoría de Software
    """

    def __init__(self, id_entidad: str, nombre_servicio: str, costo_base:float, consultor: str):
        super().__init__(id_entidad, nombre_servicio, costo_base)
        self.consultor = consultor

    def calcular_costo(self, duracion: int, tarifa_urgencia:float=0.0)->float:
        """ Método para validar y realizar el calculo del costo de la asesoría especializada"""
        if duracion <= 0:
            raise datosInvalidosError("La duración de la asesoría debe ser de al menos 1 hora")
    
        costo_total = self.costo_base * duracion + tarifa_urgencia # aqui se calcula el costo_total, teniendo en cuenta el costo_base, la duración de la asesoría y la tarifa de emergencia (la cual es puesta por el administrativo)
        return round(costo_total, 2)
    
    def obtener_detalles(self) -> str:
        return f"[Asesoría] ID: {self.id_entidad} | {self.nombre_servicio} | Consultor: {self.consultor} | Costo/Hora: ${self.formatear_valor_numero(self.costo_base)}"