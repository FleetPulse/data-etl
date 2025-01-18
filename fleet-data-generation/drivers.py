import random
from dotenv import dotenv_values
from faker import Faker
from pymongo import MongoClient

config = dotenv_values('.env')

mongo_uri = config['mongo_uri']
client = MongoClient(mongo_uri)

db = client['fleetpulse']
collection = db['driver']

fake = Faker()
driver_data =[]
driver_ids = list(range(110,120))

def generate_driver_data():

    for id in driver_ids:
        driver_json = {
            'driver_id' : id,
            'driver_name' : fake.name(),
            'license_number' : fake.license_plate(),
            'age' : random.randint(30,50),
            'experience' : random.randint(5,10),
            'status' : random.choice(['Active']*10 + ['Inactive'])
        }
        driver_data.append(driver_json)

    return driver_data

if __name__=='__main__':

    driver_data = generate_driver_data()
    try:
        collection.insert_many(driver_data)
        print('Driver data inserted into database collection')
    except Exception as e:
        print(e)

