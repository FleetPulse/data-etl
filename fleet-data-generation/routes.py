import requests
from dotenv import dotenv_values
from pymongo import MongoClient

config = dotenv_values(".env")

google_api_key = config['google_api_key']
mongo_uri = config['mongo_uri']

client = MongoClient(mongo_uri)
db = client["fleetpulse"] 
collection = db["route"]  

origin_destination_mapping = [
     {'origin':'Pune','destination':'Mumbai'}
    ,{'origin':'Mumbai','destination':'Nagpur'}
    ,{'origin':'Mumbai','destination':'Chennai'}
    ,{'origin':'Ahemdabad','destination':'Mumbai'}
    ,{'origin':'Mumbai','destination':'Delhi'}
    ]

google_direction_api_url = 'https://maps.googleapis.com/maps/api/directions/json'

def get_route_coordinates():

    route_info = {}
    route_master_data = []
    route_id  = 100

    for route in origin_destination_mapping:
      
      route_info = dict()
      route_coordinates = []
      origin = route['origin']
      destination = route['destination']

      response = requests.get(google_direction_api_url, params={'destination':destination,
                                                  'origin':origin,
                                                  'key':google_api_key})
      data = response.json()
      distance = data['routes'][0]['legs'][0]['distance']['text']

      for direction in data['routes'][0]['legs'][0]['steps']:
          lat,long = direction.get('end_location').values()
          route_coordinates.append([lat,long])

      route_info['route_id'] = route_id  
      route_info['origin'] = origin
      route_info['destination'] = destination
      route_info['origin_coordinates'] = route_coordinates[0]
      route_info['destination_coordinates'] = route_coordinates[-1]
      route_info['distance'] = distance
      route_info['coordinates'] = route_coordinates
      
      route_master_data.append(route_info)
      route_id += 1 

    return route_master_data

if __name__=='__main__':
   
    routes_data = get_route_coordinates()
    try:
        collection.insert_many(routes_data)
        print('Route data inserted into database collection')
    except Exception as e:
        print(e)


