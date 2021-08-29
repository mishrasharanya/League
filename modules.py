#modules - getting geolocation, calculating distance.
import requests
from database_modules import *
import math


def create_waypoint(mail):
    name = input("Enter name of the waypoint: ")
    while True:
        waypoint_selection = input("Do you want to create a waypoint on your current location?(y/n): ")
        if waypoint_selection.lower() == 'y' or waypoint_selection == '':
            latitude = get_location()[0]
            longitude = get_location()[1]
            waypoint_confirmation = input(f"Latitude: {latitude}\nLongitude: {longitude}\nare the latitudes for the "
                                          f"waypoint, is it fine?(y,n): ")
            if waypoint_confirmation.lower() == 'y' or waypoint_confirmation == '':
                print("Okay, coordinates are confirmed")
            elif waypoint_confirmation.lower() == 'n':
                print("Okay, coordinates discarded")
                return

            while True:
                try:
                    radius = float(input("Enter the radius: "))
                except ValueError:
                    print("Radius must be a floating point value")
                    continue

                radius_confirmation = input(f"Radius set to {radius}m, is this fine?(y/n): ")
                if radius_confirmation.lower() == 'y' or radius_confirmation == '':
                    print("Okay, radius is confirmed!")
                    break
                else:
                    print("Okay, radius discarded")
                    return
            print("Writing to database...")
            insert_waypoint(latitude, longitude, radius, name, mail)
            break
        elif waypoint_selection.lower() == 'n':
            while True:
                try:
                    latitude = float(input("Enter latitude: "))
                    longitude = float(input("Enter longitude: "))
                    coordinates_confirmation = input(f"Latitude: {latitude}\nLongitude: {longitude}\nare the "
                                                     f"coordinates, is this fine?(y,n): ")
                    if coordinates_confirmation.lower() == 'y' or coordinates_confirmation == '':
                        print("Okay, coordinates confirmed!")
                    elif coordinates_confirmation.lower() == 'n':
                        print("Okay, coordinates discarded")
                        return
                    break
                except ValueError:
                    print("Latitude and longitude must be floating point only")
                    continue

            while True:
                try:
                    radius = float(input("Enter the radius: "))
                    break
                except ValueError:
                    print("Please enter floating point variables only")
                    continue

            radius_confirmation = input(f"Radius set to {radius}m, is this fine?(y/n): ")
            if radius_confirmation.lower() == 'y' or radius_confirmation == '':
                print("Okay, radius is confirmed!")
            else:
                print("Okay, radius discarded")
                return
            print("Writing to database...")
            insert_waypoint(latitude, longitude, radius, name, mail)
            break

        else:
            print(f"Please enter \"y\" or \"n\", {waypoint_selection} is not valid")
# Calculates the distance


def distance_calculation(latitude, longitude):
    waypoint_location = fetch_waypoint(latitude, longitude)
    if waypoint_location is None:
        return False
    client_location = get_location()
    print("client-")
    print(f"Latitude: {client_location[0]}, Longitude: {client_location[1]}")
    print("waypoint - ")
    waypoint_latitude = float(waypoint_location["latitude"])
    waypoint_longitude = float(waypoint_location["longitude"])
    client_latitude = float(client_location[0])
    client_longitude = float(client_location[1])
    print(f"Latitude: {waypoint_latitude}, Longitude: {waypoint_longitude}")

    a = (math.sin(math.radians(abs(client_latitude - waypoint_latitude))/2) ** 2) + (math.cos(math.radians(waypoint_latitude)) * math.cos(math.radians(client_latitude)) * math.sin(math.radians(abs(waypoint_longitude - client_longitude)))**2 )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    waypoint_dist = 6371*c
    dist = waypoint_dist - waypoint_location["radius"]


    return dist


def get_location():
    ip = get_ip()
    url = f"http://ipwhois.app/json/{ip}"

    response = requests.get(url, params=None)

    data = response.json()
    latitude = data["latitude"]
    longitude = data["longitude"]
    array = [latitude, longitude]

    return array
def get_ip():
    ip = requests.get("https://api.ipify.org/").text

    return ip


def sign_in_module(username, password):
    details = fetch_user_details(username, password)

    if details is None:
        return False
    else:
        return True


def sign_up_module(mail, password, phone_number, name, role):
    check = create_user_account(mail, password, phone_number, name, role)
    return check


def show_waypoints(mail):

    waypoints = fetch_all_waypoint(mail)
    print("Waypoints with the registered mail: ")
    i = 1
    for waypoint in waypoints:
        name = waypoint["name"]
        latitude = waypoint["latitude"]
        longitude = waypoint["longitude"]
        radius = waypoint["radius"]
        print(f"{i}) {name}\n\tLatitude: {latitude}\n\tLongitude: {longitude}\n\tRadius: {radius}m")
        i += 1
        print()


if __name__ == "__main__":

    # Unit testing
    unit_testing = input("Enter module to test: ")
    if unit_testing.lower() == "create_waypoint":
        create_waypoint("amogh@gmail.com")
    elif unit_testing.lower() == "get_location":
        print(get_location())
    elif unit_testing.lower() == "get_ip":
        print(get_ip())
    elif unit_testing.lower() == "distance":
        distance = distance_calculation("12.975340", "77.674520")
        print(distance)
        if (distance < 0):
            print("You are inside the geofence")
        else:
            print("You are outside")
    elif unit_testing.lower() == "show_waypoints":
        show_waypoints("amogh@gmail.com")
    else:
        print("no module named such")