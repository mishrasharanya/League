from modules import*
from database_modules import*
import os
import time
import stdiomask
#from getpass import getpass


# Main file where everything happens

# Login form test

def login():    
    tries = 3
    is_login = False

    while tries >= 0:
        print("Enter the credentials: ")
        username = input("Username / mail: ")
        password = stdiomask.getpass()

        check = sign_in_module(username, password)

        if check is False:
            print("\nUsername or password incorrect, please try again")
            time.sleep(1)
            os.system("cls")
        else:
            print("Login successful")
            is_login = True
            details = fetch_user_details(username, password)
            return details
    if is_login is False:
        print("Too many incorrect attempts")


def sign_up():
    while True:
        role_choice = int(input("Do you want to be:\n1) Admin\n2) Client\n==>"))
        if role_choice == 1:
            role = "Admin"
            break
        elif role_choice == 2:
            role = "Client"
            break
        else:
            print("choose 1 or 2 only")

    name = input("Name: ")
    mail = input("Enter the mail-id: ")

    check = None
    check = collection.find_one({"mail": mail})
    if check is not None:
        print("An account with the mail id already exists, try something else..")
        return

    while True:
        password = stdiomask.getpass()
        password_check = stdiomask.getpass()
        if password_check == password:
            break
        else:
            print("Passwords do not match")
            print()

    phone_number = input("Phone number: ")

    create_user_account(mail, password, phone_number, name, role)

    print("Account created!")

if __name__ == "__main__":
    choice = int(input("Choose an option:\n1) login\n2) Sign-up\n==> "))
    if choice == 1:
        details = login()
        time.sleep(3)
        os.system("cls")
        role = details["role"]
        mail = details["mail"]

        print(f"You are: {role}")
        if role == "Admin":
            print("waypoints:\n")
            waypoints = fetch_all_waypoint(mail)

            i = 0
            for waypoint in waypoints:
                name = waypoint["name"]
                latitude = waypoint["latitude"]
                longitude = waypoint["longitude"]
                radius = waypoint["radius"]
                print(f"{i + 1}) {name}\n\tLatitude: {latitude}\n\tLongitude: {longitude}\n\tRadius: {radius}")
                i += 1
            if i == 0:
                print("You do not have any waypoints set")

            choice = input("Do you want to add a new waypoint?(y,n): ")
            if choice.lower() == "y" or choice == '':
                print("Okay, adding new waypoint..")
                create_waypoint(mail)
                print()
                print("Waypoint has been created!")
            elif choice == "n":
                print("Okay, no waypoints being added")

    elif choice == 2:
        sign_up()
