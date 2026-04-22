import os
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.catalogo import Producto
from app.services import calcular_valor_total, calcular_estado

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "../templates"))
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home(request: Request):
    productos = [
        Producto(codigo=1, nombre="Cuaderno", valoru=5000, existencias=100),
        Producto(codigo=2, nombre="Esfero", valoru=2500, existencias=250),
        Producto(codigo=3, nombre="Lápiz", valoru=1500, existencias=300),
    ]

    resultado = []

    for p in productos:
        resultado.append({
            "codigo": p.codigo,
            "nombre": p.nombre,
            "valoru": p.valoru,
            "existencias": p.existencias,
            "valor_total": calcular_valor_total(p),
            "estado": calcular_estado(p)
        })
    print(resultado)
    return templates.TemplateResponse(
    request,
    "index.html",
    {
        "productos": resultado
    }
)