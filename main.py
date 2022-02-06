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
    search_result = list(collection.find({"name": name}, {"_id": 0}))
    if len(search_result) == 0:
        raise HTTPException(status_code=404, detail="Reservation not found")
    else:
        # for loop to get all the results in one json
        result = []
        for i in search_result:
            result.append(i)
        return result


@app.get("/reservation/by-table/{table}")
def get_reservation_by_table(table: int):
    search_result = list(collection.find({"table_number": table}, {"_id": 0}))
    if len(search_result) == 0:
        raise HTTPException(status_code=404, detail="Reservation not found")
    else:
        # for loop to get all the results in one json
        result = []
        for i in search_result:
            result.append(i)
        return result


@app.post("/reservation")
def reserve(reservation: Reservation):
    # If the reservation on the same table and same time is already made, return error
    search_result = collection.find_one({"time": reservation.time, "table_number": reservation.table_number}, {"_id": 0})
    if search_result is not None:
        raise HTTPException(status_code=409, detail="Reservation already exists")
    else:
        collection.insert_one(jsonable_encoder(reservation))
        return {"status": "Reservation successfully"}


@app.put("/reservation/update/")
def update_reservation(reservation: Reservation):
    reservation_to_update = collection.find_one({"name": reservation.name, "table_number": reservation.table_number}, {"_id": 0})
    if reservation_to_update is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    else:
        # Find in database that is that table and that time is already taken
        search_result = collection.find_one({"time": reservation.time, "table_number": reservation.table_number}, {"_id": 0})
        if search_result is not None:
            raise HTTPException(status_code=409, detail="Reservation already exists")
        else:
            collection.update_one({"name": reservation.name, "table_number": reservation.table_number}, {"$set": jsonable_encoder(reservation)})
            return {"status": "update successfully"}


@app.delete("/reservation/delete/{name}/{table_number}")
def cancel_reservation(name: str, table_number: int):
    reservation_to_delete = collection.find_one({"name": name, "table_number": table_number}, {"_id": 0})
    if reservation_to_delete is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    else:
        collection.delete_one({"name": name, "table_number": table_number})
        return {"status": "Reservation cancelled"}
