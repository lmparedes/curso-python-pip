from fastapi import FastAPI
import datetime

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, Liliana!"}

@app.get("/hora")
async def obtener_hora():
    ahora = datetime.datetime.now()
    return {"hora": ahora.strftime("%H:%M:%S")}