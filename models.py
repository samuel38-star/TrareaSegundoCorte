from sqlmodel import SQLModel, Field
from typing import Optional

class Paciente(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    enfermedad: str
    prioridad: int