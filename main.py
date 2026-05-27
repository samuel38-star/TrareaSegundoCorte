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

# =========================
# VARIABLES GLOBALES
# =========================

cola_atencion = []
historial_acciones = []

# =========================
# INICIO
# =========================

@app.get("/")
def inicio(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

# =========================
# REGISTRAR PACIENTE
# =========================

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
        context={
            "mensaje": "Paciente registrado correctamente"
        }
    )

# =========================
# AGREGAR A LA COLA
# =========================

@app.post("/agregar_cola")
def agregar_cola(
    request: Request,
    nombre: str = Form(...)
):

    mensaje = ""

    with Session(engine) as session:

        paciente = session.exec(
            select(Paciente).where(
                Paciente.nombre == nombre
            )
        ).first()

        if paciente:

            paciente.en_cola = True

            session.add(paciente)

            session.commit()

            mensaje = (
                f"{paciente.nombre} agregado correctamente"
            )

        else:

            mensaje = "Paciente no encontrado"

    return templates.TemplateResponse(
        request=request,
        name="agregar_cola.html",
        context={
            "mensaje": mensaje
        }
    )

# =========================
# VER COLA DE ATENCION
# =========================

@app.get("/pacientes")
def ver_pacientes(request: Request):

    with Session(engine) as session:

        pacientes = session.exec(

            select(Paciente)

            .where(Paciente.en_cola == True)

            .order_by(Paciente.prioridad)

        ).all()

    return templates.TemplateResponse(
        request=request,
        name="pacientes.html",
        context={
            "pacientes": pacientes
        }
    )

# =========================
# ATENDER PACIENTE
# =========================

@app.post("/atender")
def atender_paciente(request: Request):

    mensaje = "No hay pacientes en la cola"

    with Session(engine) as session:

        paciente = session.exec(

            select(Paciente)

            .where(Paciente.en_cola == True)

            .order_by(Paciente.prioridad)

        ).first()

        if paciente:

            paciente.en_cola = False

            paciente.atendido = True

            session.add(paciente)

            session.commit()

            mensaje = (
                f"Paciente atendido correctamente: "
                f"{paciente.nombre}"
            )

        pacientes = session.exec(

            select(Paciente)

            .where(Paciente.en_cola == True)

            .order_by(Paciente.prioridad)

        ).all()

    return templates.TemplateResponse(
        request=request,
        name="pacientes.html",
        context={
            "pacientes": pacientes,
            "mensaje": mensaje
        }
    )

# =========================
# HISTORIAL
# =========================

@app.get("/historial")
def historial(request: Request):

    with Session(engine) as session:

        historial = session.exec(

            select(Paciente)

            .where(Paciente.atendido == True)

        ).all()

    return templates.TemplateResponse(
        request=request,
        name="historial.html",
        context={
            "historial": historial
        }
    )