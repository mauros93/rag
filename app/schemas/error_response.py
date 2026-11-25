from pydantic import BaseModel, Field, ConfigDict


class ErrorResponse(BaseModel):
    """
    Estructura estándar de las respuestas de error de la API.
    """

    detail: str = Field(
        description="Descripción del error ocurrido."
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "detail": "Usuario no encontrado."
            }
        }
    )