from sqlmodel import SQLModel, Field
from typing import Optional

class Paciente(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    nombre: str
    enfermedad: str
    prioridad: int

    en_cola: bool = False

    atendido: bool = False