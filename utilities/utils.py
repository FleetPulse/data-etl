from pymongo import MongoClient
from dotenv import dotenv_values

config = dotenv_values(".env")

client = MongoClient(config["mongo_uri"])
db = client["fleetpulse"]

def get_all_entity_ids():

    vehicles = db.get_collection("vehicle")
    drivers = db.get_collection("driver")
    routes = db.get_collection("route")
    trips = db.get_collection("trips")

    vehicle_ids = []
    route_ids = []
    driver_ids = []
    trip_ids = []

    for entity in [vehicles, routes, drivers, trips]:
        if entity.name == "vehicle":
            for value in entity.find():
                vehicle_ids.append(value["id"])
        elif entity.name == "route":
            for value in entity.find():
                route_ids.append(value["route_id"])
        elif entity.name == "driver":
            for value in entity.find():
                driver_ids.append(value["driver_id"])
        elif entity.name == "trips":
            for value in entity.find():
                trip_ids.append(value["trip_id"])

    return {
        "vehicle_ids": vehicle_ids,
        "route_ids": route_ids,
        "trip_ids": trip_ids,
        "driver_ids": driver_ids,
    }
