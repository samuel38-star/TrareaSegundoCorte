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

@app.get("/agregar_cola")
def vista_agregar_cola(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="agregar_cola.html"
    )

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

        cola_atencion.append(paciente)

        # Ordenar por prioridad
        cola_atencion.sort(
            key=lambda x: x.prioridad
        )

        historial_acciones.append(
            f"Paciente agregado a la cola: {paciente.nombre}"
        )

        mensaje = f"{paciente.nombre} agregado correctamente"

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

    cola_ordenada = sorted(
        cola_atencion,
        key=lambda x: x.prioridad
    )

    return templates.TemplateResponse(
        request=request,
        name="pacientes.html",
        context={
            "pacientes": cola_ordenada
        }
    )

# =========================
# ATENDER PACIENTE
# =========================

@app.post("/atender")
def atender_paciente(request: Request):

    mensaje = "No hay pacientes en la cola"

    if cola_atencion:

        paciente = cola_atencion.pop(0)

        historial_acciones.append(
            f"Paciente atendido: {paciente.nombre}"
        )

        mensaje = (
            f"Paciente atendido correctamente: "
            f"{paciente.nombre}"
        )

    return templates.TemplateResponse(
        request=request,
        name="pacientes.html",
        context={
            "pacientes": cola_atencion,
            "mensaje": mensaje
        }
    )

# =========================
# HISTORIAL
# =========================

@app.get("/historial")
def historial(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="historial.html",
        context={
            "historial": historial_acciones
        }
    )