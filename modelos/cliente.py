from modelos.entidad import Entidad
from excepciones import datosInvalidosError

class Cliente(Entidad):
    def __init__(self, id_entidad: str, nombre: str, email: str):
        """
        Clase para guardar los campos de los clientes
        """
        super().__init__(id_entidad)
        self.nombre = nombre
        self.email = email

    # A continuación defino con @property los atributos de la clase Cliente para que solo puedan ser leidos desde afuera.
    @property
    def nombre(self):
        return self._nombre
    @property
    def email(self):
        return self._email
    
    # Aquí defino los setters para nombre y cliente (atributos) con el fin de evaluar si estos tienen problemas y de este modo lanzar las clases con sus respectivas excepciones
    @nombre.setter
    def nombre(self, nombre: str):
        if nombre is None or str(nombre).strip() == "":
            raise datosInvalidosError("El nombre no puede estar vacío")
        self._nombre = str(nombre).strip()
    
    @email.setter
    def email(self, email: str):
        if email is None:
            raise datosInvalidosError("El correo no puede estar vacío")
        email_str = str(email).strip()
        if "@" not in email_str or "." not in email_str:
            raise datosInvalidosError("El correo debe contener '.' y '@'")
        self._email = email_str
    
    
    def obtener_detalles(self) -> str:
        """Esta es la función que defini como necesaria y obligatoria para las clases hijas,
        con esta clase se busca mostrar una pequeña descripción de los clientes"""
        
        return f"ID: {self.id_entidad}, Nombre: {self.nombre}, Email: {self.email}"