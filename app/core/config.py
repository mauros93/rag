
# Importamos BaseSettings para gestionar configuraciones
# obtenidas desde variables de entorno o archivos .env.
from pydantic_settings import BaseSettings, SettingsConfigDict


# Esta clase representa la configuración global de nuestra aplicación.
# BaseSettings permite leer las variables y validar sus tipos.
class Settings(BaseSettings):

    # Credenciales necesarias para conectarnos a PostgreSQL.
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    # Configuraciones generales de FastAPI.
    # Estas variables sí tienen valores predeterminados.
    APP_NAME: str = "RAG API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Configuracion de JWT
    JWT_SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Configuración de Pydantic Settings.
    model_config = SettingsConfigDict(
        # Indica que debe leer las variables del archivo .env.
        env_file=".env",

        # Define la codificación del archivo.
        env_file_encoding="utf-8",

        # Ignora variables adicionales que no estén declaradas
        # en esta clase.
        extra="ignore"
    )


# Creamos una instancia global de Settings.
# Al importar este archivo, Pydantic carga y valida la configuración.
# Los demás módulos pueden importar esta instancia para utilizarla.
settings = Settings()
