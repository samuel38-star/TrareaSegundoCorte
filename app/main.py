from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from sqlmodel import (SQLModel,Field,create_engine,Session,select)
from contextlib import asynccontextmanager
from typing import Optional


class Hotel(SQLModel, table=True):

    codigo: Optional[int] = Field(default=None,primary_key=True)
    nombre: str
    ciudad: str
    valornoche: float


class Cliente(SQLModel, table=True):
    __tablename__ = "clientes"
    id: Optional[int] = Field(default=None,primary_key=True)
    nombre: str
    correo: str

postgres_url = ("postgresql://postgres:123@localhost:12345/ventas")

engine = create_engine(postgres_url,echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()  
    yield

app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="templates")


@app.get("/")
def inicio(request: Request):

    with Session(engine) as session:

        hoteles = session.exec(select(Hotel)).all()

        clientes = session.exec(select(Cliente)).all()

        return templates.TemplateResponse(

            request=request,

            name="index.html",

            context={"hoteles": hoteles,"clientes": clientes}
        )


@app.get("/hotel/{codigo}")
def buscar_hotel(request: Request,codigo: int):

    with Session(engine) as session:
        hotel = session.get(Hotel,codigo)

        if not hotel:
            raise HTTPException(status_code=404,detail="Hotel no encontrado")

        return templates.TemplateResponse(

            request=request,

            name="hotel.html",

            context={"hotel": hotel}
        )


@app.get("/ciudad/{ciudad}")
def buscar_ciudad(request: Request,ciudad: str):

    with Session(engine) as session:

        hoteles = session.exec(select(Hotel).where(Hotel.ciudad == ciudad)).all()

        return templates.TemplateResponse(

            request=request,

            name="ciudad.html",

            context={"hoteles": hoteles,"ciudad": ciudad}
            )


@app.post("/hotel")
def adicionar_hotel(hotel: Hotel):

    if hotel.nombre.strip() == "":
        raise HTTPException(status_code=400,detail="Nombre inválido")

    if hotel.ciudad.strip() == "":
        raise HTTPException(status_code=400,detail="Ciudad inválida")

    if hotel.valornoche < 0:
        raise HTTPException(status_code=400,detail="Precio inválido")

    with Session(engine) as session:
        session.add(hotel)
        session.commit()
        session.refresh(hotel)
        return {"mensaje": "Hotel agregado correctamente","hotel": hotel}


@app.put("/hotel/{codigo}")
def modificar_hotel(codigo: int,datos: Hotel):

    with Session(engine) as session:
        hotel_db = session.get(Hotel,codigo)
        if not hotel_db:
            raise HTTPException(status_code=404,detail="Hotel no encontrado")
        if datos.nombre.strip() == "":
            raise HTTPException(status_code=400,detail="Nombre inválido")

        if datos.ciudad.strip() == "":
            raise HTTPException(status_code=400,detail="Ciudad inválida")

        if datos.valornoche < 0:
            raise HTTPException(status_code=400,detail="Precio inválido")
        hotel_db.nombre = datos.nombre
        hotel_db.ciudad = datos.ciudad
        hotel_db.valornoche = datos.valornoche
        session.add(hotel_db)
        session.commit()
        session.refresh(hotel_db)
        return {"mensaje": "Hotel actualizado correctamente","hotel": hotel_db}


@app.delete("/hotel/{codigo}")
def eliminar_hotel(codigo: int):

    with Session(engine) as session:
        hotel_db = session.get(Hotel,codigo)
        if not hotel_db:
            raise HTTPException(status_code=404,detail="Hotel no encontrado")
        session.delete(hotel_db)
        session.commit()
        return {"mensaje": "Hotel eliminado correctamente"}