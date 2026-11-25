# Este archivo tendrá una responsabilidad muy concreta: proporcionar una clase base común para todos los modelos de SQLAlchemy.


# DeclarativeBase es la clase que proporciona SQLAlchemy
# para definir modelos ORM mediante clases de Python.
from sqlalchemy.orm import DeclarativeBase


# Base será la clase padre de todos nuestros modelos.
#
# Cada modelo que herede de Base será registrado
# automáticamente en su colección de metadatos.
#
# Estos metadatos permitirán a SQLAlchemy y Alembic
# conocer la estructura de nuestras tablas.
class Base(DeclarativeBase):
    pass
