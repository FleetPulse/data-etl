from pymongo import MongoClient
from dotenv import dotenv_values
import uuid
from datetime import datetime
import random

config = dotenv_values(".env")

client = MongoClient(config["mongo_uri"])
db = client["fleetpulse"]

import math

def calculate_distance_travelled(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    # Radius of Earth (in kilometers)
    R = 6371.0
    # Differences in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)) 
    # Distance in kilometers
    distance = R * c
    return distance


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


vehicle_ids,route_ids,trip_ids,driver_ids = get_all_entity_ids().values()

def get_new_trips():

    new_trips = db.get_collection('trips').find({'status':{'$nin': ['in-transit','completed']}})
    return new_trips

def get_route_data(route_id):

    route = db.get_collection('route').find_one({'route_id':route_id})
    return route

def get_trip_data(trip_id):

    trip = db.get_collection('trip').find({'route_id':trip_id})
    return trip

def publish_telemetry_data():

    new_trips = get_new_trips()

    for trip in list(new_trips):

        route =  get_route_data(trip['route_id'])
        route_id = trip['route_id']
        trip_id = trip['trip_id']
        vehicle_id = trip['vehicle_id']
        driver_id = trip['driver_id']
        coordinates = route['coordinates']

        json_payload = {}
        base_fuel_level = random.randint(80,90)

        for lat_long in coordinates:
            base_fuel_level= base_fuel_level-random.uniform(0,1)
            json_payload = {
                'event_id' : str(uuid.uuid4()),
                'trip_id' : trip_id,
                'vehicle_id' : vehicle_id,
                'driver_id' : driver_id,
                'route_id' : route_id,
                'event_timestamp' : datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                'latitude' : lat_long[0],
                'longitude' : lat_long[1],
                'avg_speed' : random.uniform(30,50),
                'fuel_level' :  round(base_fuel_level),
                'engine_status' : 'Active',
                'distance_travelled' : 120,
                'temperature' : 12
            }

            print('For vehicle id ',json_payload['vehicle_id'], ' ' ,json_payload['fuel_level'], end= '\n')

        break
        

publish_telemetry_data()