from sqlmodel import SQLModel, Field
from datetime import datetime


class Paciente(SQLModel, table=True):

    id: int | None = Field(
        default=None,
        primary_key=True
    )

    nombre: str

    enfermedad: str

    prioridad: int

    en_cola: bool = False

    atendido: bool = False


class HistorialAccion(SQLModel, table=True):

    id: int | None = Field(
        default=None,
        primary_key=True
    )

    descripcion: str

    fecha: datetime = Field(
        default_factory=datetime.now
    )