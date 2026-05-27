from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select

from database import engine, crear_db
from models import Paciente

app = FastAPI()

crear_db()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def inicio(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

@app.get("/registrar")
def registrar(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="registrar.html"
    )

@app.post("/guardar")
def guardar(
    request: Request,
    nombre: str = Form(...),
    enfermedad: str = Form(...),
    prioridad: int = Form(...)
):
    paciente = Paciente(
        nombre=nombre,
        enfermedad=enfermedad,
        prioridad=prioridad
    )

    with Session(engine) as session:
        session.add(paciente)
        session.commit()

    return templates.TemplateResponse(
        request=request,
        name="registrar.html",
        context={"mensaje": "Paciente registrado correctamente"}
    )

@app.get("/pacientes")
def ver_pacientes(request: Request):
    with Session(engine) as session:
        pacientes = session.exec(select(Paciente)).all()

    return templates.TemplateResponse(
        request=request,
        name="pacientes.html",
        context={"pacientes": pacientes}
    )