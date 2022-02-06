from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder


class Reservation(BaseModel):
    name: str
    time: int
    table_number: int


client = MongoClient('mongodb://localhost', 27017)

db = client["restaurant"]

collection = db["reservation"]

app = FastAPI()


@app.get("/reservation/by-name/{name}")
def get_reservation_by_name(name: str):
    search_result = collection.find_one({"name": name}, {"_id": 0})
    if search_result is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return search_result


@app.get("reservation/by-table/{table}")
def get_reservation_by_table(table: int):
    search_result = collection.find_one({"table_number": table}, {"_id": 0})
    if search_result is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return search_result


@app.post("/reservation")
def reserve(reservation: Reservation):
    p = jsonable_encoder(reservation)
    collection.insert_one(p)
    # return full details of the reservation
    return {"status": "ok"}

@app.put("/reservation/update/")
def update_reservation(reservation: Reservation):
    


@app.delete("/reservation/delete/{name}/{table_number}")
def cancel_reservation(name: str, table_number: int):
    pass
