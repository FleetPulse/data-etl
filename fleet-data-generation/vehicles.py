import random
from dotenv import dotenv_values
from pymongo import MongoClient
import string

config = dotenv_values(".env")

google_api_key = config["google_api_key"]
mongo_uri = config["mongo_uri"]

client = MongoClient(mongo_uri)
db = client["fleetpulse"]
collection = db["vehicle"]

vehicle_ids = list(range(1001, 1010))
vehicle_class = ["PICK-UP"] * 10 + ["TRAILER"] * 20
year = list(range(2000, 2025))
capacity = [random.randint(500, 5000) for _ in vehicle_ids]


vehicle_data = []


def generate_registration_number(vehicle_id):
    return f"MH{vehicle_id}{''.join(random.choices(string.ascii_uppercase + string.digits, k=5))}"


def generate_vehicle_data():

    for id in vehicle_ids:
        json_data = {
            "id": id,
            "registration": generate_registration_number(id),
            "class": random.choice(vehicle_class),
            "year": random.choice(year),
            "capacity(KG)": random.choice(capacity),
        }

        vehicle_data.append(json_data)

    return vehicle_data


if __name__ == "__main__":

    routes_data = generate_vehicle_data()
    try:
        collection.insert_many(vehicle_data)
        print("Vehicle data inserted into database collection")
    except Exception as e:
        print(e)
