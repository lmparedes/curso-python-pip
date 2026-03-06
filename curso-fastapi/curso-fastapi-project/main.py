import zoneinfo
from datetime import datetime
from fastapi import FastAPI, HTTPException

from models import Costumer, CostumerCreate, Transaction, Invoice
from db import SessionDep

app = FastAPI()

country_timezones = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "PE": "America/Lima",
}

@app.get("/time/{iso_code}")
async def time(iso_code: str, format: str = "24"):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)

    if not timezone_str:
        raise HTTPException(status_code=404, detail="País no soportado")

    tz = zoneinfo.ZoneInfo(timezone_str)
    now = datetime.now(tz)

    if format == "12":
        time_str = now.strftime("%I:%M:%S %p")
    else:
        time_str = now.strftime("%H:%M:%S")

    return {
        "country": iso,
        "timezone": timezone_str,
        "time": time_str,
        "format": format
    }

db_costumers: list[Costumer] = []

#Crea un nuevo costumer y lo agrega a la base de datos simulada, luego devuelve el costumer creado
@app.post("/costumers", response_model=Costumer)
async def create_costumer(costumer_data: CostumerCreate, session: SessionDep):
    costumer = Costumer.model_validate(costumer_data.model_dump())
    #Asumiendo que se hace en la base de datos
    costumer.id = len(db_costumers)
    db_costumers.append(costumer)
    return costumer

#devuelve el costumer pasando el id del costumer, si no lo encuentra devuelve un error 404
@app.get("/costumers/{costumer_id}", response_model=Costumer)
async def get_costumer(costumer_id: int):
    for costumer in db_costumers:
        if costumer.id == costumer_id:
            return costumer
    
    raise HTTPException(status_code=404, detail="Costumer not found")

#devuelve la lista de costumers registrados en la base de datos simulada
@app.get("/costumers", response_model=list[Costumer])
async def list_costumer():
    return db_costumers

@app.post("/Transactions")
async def create_transaction(transaction_data: Transaction):
    # Aquí podrías agregar lógica para guardar la transacción en una base de datos
    return transaction_data

@app.post("/invoices")
async def create_invoice(invoice_data: Invoice):
    # Aquí podrías agregar lógica para guardar el cliente en una base de datos
    return invoice_data