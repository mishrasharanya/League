# functions to write, read and update stuff from and to the database
# Mongodb

import pymongo  
from pymongo import MongoClient
import random

if __name__=="__main__":
#with open("./password.txt", "r") as password_handle:
#cluster = MongoClient(password_handle.read())
    client=pymongo.MongoClient("mongodb://localhost:27017/")
    print(client)
    db = client['geofence']
    collection = db['testtable']
    waypoint_collection = db['waypoints']


# Admin field

# waypoint

def insert_waypoint(latitude, longitude, radius, name, mail):
    waypoint = None
    waypoint = waypoint_collection.find_one({"latitude": latitude, "longitude": longitude, "radius": radius})
    if waypoint is None:
        waypoint = waypoint_collection.insert_one(
            {"latitude": latitude, "longitude": longitude, "radius": radius, "name": name, "mail": mail})
        return True
    else:
        return False


def fetch_waypoint(latitude, longitude):
    waypoint = None
    waypoint = waypoint_collection.find_one({"latitude": latitude, "longitude": longitude})
    return waypoint


def fetch_all_waypoint(mail):
    many_waypoint = None
    many_waypoint = waypoint_collection.find({"mail": mail})

    array = []
    for waypoint in many_waypoint:
        array.append(waypoint)

    return array


def delete_waypoint(latitude, longitude):
    waypoint = waypoint_collection.delete_one({"latitude": latitude, "longitude": longitude})


# User account

def create_user_account(mail, password, phone_number, name, role):
    id = int(random.random() * 10 ** 16)

    account_check = None
    account_check = collection.find_one({"mail": mail})

    if account_check is None:
        account = collection.insert_one(
            {"mail": mail, "password": password, "phone number": phone_number, "name": name, "id": id, "role": role})
        return True
    else:
        return False


def fetch_user_details(mail, password):
    details = None
    details = collection.find_one({"mail": mail, "password": password})

    return details


if __name__ == "__main__":
    # print("Inserting waypoint")
    # status = insert_waypoint(12.9715987, 77.5945627, 5)
    # if status is False:
    #     print("Value already present!!")
    #
    # print("Deleting waypoint...")
    # delete_waypoint(12.9715987, 77.5945627)

    pass