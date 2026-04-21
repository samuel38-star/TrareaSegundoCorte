from pydantic import BaseModel

class Producto(BaseModel):
    codigo: int
    nombre: str
    valoru: float
    existencias: int