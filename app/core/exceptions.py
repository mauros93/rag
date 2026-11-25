"""Excepciones de negocio compartidas por la capa de servicios.

Estas excepciones no dependen de FastAPI ni de HTTP: los servicios las lanzan
cuando se incumple una regla de negocio y la capa HTTP las traduce a
respuestas concretas mediante los manejadores registrados en ``app.main``.
"""


class DomainError(Exception):
    """Clase base para los errores de negocio.

    Los servicios lanzan sus subclases cuando una regla de negocio falla.
    La capa HTTP las captura mediante ``app.add_exception_handler`` y las
    convierte en respuestas con el código adecuado.
    """


class UserNotFoundError(DomainError):
    """Se lanza cuando el usuario solicitado no existe.

    La lanza la capa de servicios después de que el repositorio devuelva
    ``None``. El manejador registrado en ``app.main`` la traduce a HTTP 404.
    """


class EmailAlreadyRegisteredError(DomainError):
    """Se lanza cuando el correo electrónico ya está registrado.

    La lanza la capa de servicios tras comprobar con el repositorio si existe
    otro usuario con ese correo. El manejador de ``app.main`` la traduce a
    HTTP 409.
    """


class InvalidCredentialsError(DomainError):
    """Se lanza cuando el correo o la contraseña no son válidos.

    La lanza la capa de servicios sin revelar cuál de las dos credenciales
    es incorrecta. El manejador de ``app.main`` la traduce a HTTP 401.
    """


class NullFieldError(DomainError):
    """Se lanza cuando una actualización parcial envía ``null`` en un campo.

    La lanza la capa de servicios al validar el payload de actualización.
    El manejador de ``app.main`` la traduce a HTTP 422 e indica el campo
    afectado.
    """

    def __init__(self, field: str) -> None:
        self.field = field

    def __str__(self) -> str:
        return f"El campo {self.field} no puede ser null"
