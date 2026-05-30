from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from database import engine

from models.models import Paciente, HistorialAccion

router = APIRouter()

templates = Jinja2Templates(
    directory="templates"
)

# =========================
# INICIO
# =========================

@router.get("/")
def inicio(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

# =========================
# REGISTRAR PACIENTE
# =========================

@router.get("/registrar")
def registrar(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="registrar.html"
    )


@router.post("/guardar")
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

@router.get("/agregar_cola")
def vista_agregar_cola(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="agregar_cola.html"
    )


@router.post("/agregar_cola")
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

            if paciente.en_cola:

                mensaje = (
                    f"{paciente.nombre} ya se encuentra en la cola"
                )

            else:

                paciente.en_cola = True

                accion = HistorialAccion(
                    descripcion=
                    f"{paciente.nombre} ingresó a la cola"
                )

                session.add(accion)

                session.add(paciente)

                session.commit()

                mensaje = (
                    f"{paciente.nombre} fue agregado "
                    f"a la cola correctamente"
                )

        else:

            mensaje = (
                "No existe un paciente "
                "con ese nombre"
            )

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

@router.get("/pacientes")
def ver_pacientes(request: Request):

    with Session(engine) as session:

        pacientes = session.exec(

            select(Paciente)

            .where(
                Paciente.en_cola == True
            )

            .order_by(
                Paciente.prioridad
            )

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

@router.post("/atender")
def atender_paciente(request: Request):

    mensaje = "No hay pacientes en la cola"

    with Session(engine) as session:

        paciente = session.exec(

            select(Paciente)

            .where(
                Paciente.en_cola == True
            )

            .order_by(
                Paciente.prioridad
            )

        ).first()

        if paciente:

            paciente.en_cola = False

            paciente.atendido = True

            accion = HistorialAccion(
                descripcion=
                f"{paciente.nombre} fue atendido"
            )

            session.add(accion)

            session.add(paciente)

            session.commit()

            mensaje = (
                f"Paciente atendido correctamente: "
                f"{paciente.nombre}"
            )

        pacientes = session.exec(

            select(Paciente)

            .where(
                Paciente.en_cola == True
            )

            .order_by(
                Paciente.prioridad
            )

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

@router.get("/historial")
def historial(request: Request):

    with Session(engine) as session:

        acciones = session.exec(

            select(HistorialAccion)

            .order_by(
                HistorialAccion.fecha.desc()
            )

        ).all()

    return templates.TemplateResponse(
        request=request,
        name="historial.html",
        context={
            "acciones": acciones
        }
    )