from datetime import datetime, timedelta
import random
from pymongo import MongoClient
from dotenv import dotenv_values

config = dotenv_values(".env")

client = MongoClient(config["mongo_uri"])
db = client["fleetpulse"]
collection = db["trips"]

vehicles = db.get_collection("vehicle")
drivers = db.get_collection("driver")
routes = db.get_collection("route")

vehicle_ids = []
route_ids = []
driver_ids = []
locations = ["Pune", "Mumbai", "Delhi", "Nagpur", "Chennai", "Ahemdabad"]

trip_ids = list(range(1010, 1015))
trip_data = []


def gen_entity_ids(entity_db):
    for entity in list(entity_db.find()):
        if entity_db.name == "vehicle":
            vehicle_ids.append(entity["id"])
        elif entity_db.name == "route":
            route_ids.append(entity["route_id"])
        elif entity_db.name == "driver":
            driver_ids.append(entity["driver_id"])


for entity in [vehicles, drivers, routes]:
    gen_entity_ids(entity)

start_location = random.choices(locations)[0]
end_location = random.choices(
    [location for location in locations if location != start_location]
)[0]


def generate_trip_data():

    used_vehicle_ids = set()

    for id in trip_ids:

        available_vehicle_ids = list(set(vehicle_ids) - used_vehicle_ids)

        if not available_vehicle_ids:
            break
        vehicle_id = random.choice(available_vehicle_ids)
        used_vehicle_ids.add(vehicle_id)

        start_location = random.choices(locations)[0]
        end_location = random.choices(
            [location for location in locations if location != start_location]
        )[0]

        pickup_time = datetime.utcnow() + timedelta(days=random.randint(1, 10))
        delivery_time = pickup_time + timedelta(days=random.randint(1, 3))

        trip_json = {
            "trip_id": id,
            "vehicle_id": vehicle_id,
            "route_id": random.choice(route_ids),
            "driver_id": random.choice(driver_ids),
            "pickup_time": pickup_time.strftime("%Y-%m-%d %H:%M:%S"),
            "delivery_time": delivery_time.strftime("%Y-%m-%d %H:%M:%S"),
            "start_location": start_location,
            "end_location": end_location,
            "distance_travelled": 0,
            "status": "Departed",
            "cargo_weight": round(random.uniform(500, 5000)),
        }
        trip_data.append(trip_json)

    return trip_data


if __name__ == "__main__":

    trip_data = generate_trip_data()
    try:
        collection.insert_many(trip_data)
        print("Trip data inserted into database collection")
    except Exception as e:
        print(e)
