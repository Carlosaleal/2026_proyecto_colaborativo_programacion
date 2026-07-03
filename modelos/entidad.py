from abc import ABC, abstractmethod
from excepciones import datosInvalidosError

class Entidad(ABC):  
    """
    Clase abstracta que representa una entidad general dentro del sistema Software FJ.
    """
    def __init__(self, id_entidad: str):
        self.id_entidad = id_entidad

    @property
    def id_entidad(self) -> str:
        return self._id_entidad

    @id_entidad.setter
    def id_entidad(self, valor: str):
        if valor is None or str(valor).strip() == "":
            raise datosInvalidosError("El identificador / ID de la entidad no puede estar vacío.")
        self._id_entidad = str(valor).strip()

    @abstractmethod
    def obtener_detalles(self) -> str:
        """
        Método abstracto obligatorio para que las clases derivadas describan sus atributos.
        """
        pass