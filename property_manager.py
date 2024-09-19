import json
import pandas as pd
from tabulate import tabulate


# Load JSON data
def load_data(filename='property_data.json'):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Failed to parse {filename}.")
        return None


data = load_data()


# check if operator is authorized
def authenticate_operator(first_name, last_name):
    for person in data['people']:
        if person['first_name'].lower() == first_name.lower() and person['last_name'].lower() == last_name.lower():
            return person
    return None


# List users and devices by unit
def list_users_and_devices(first_name, last_name, accessible_unit, is_admin=False):
    if is_admin:
        users_in_unit = [person for person in data['people'] if
                         person['unit'] == str(accessible_unit) and 'Resident' in person['roles']]
    else:
        users_in_unit = [person for person in data['people'] if
                         person['unit'] == str(accessible_unit) and 'Resident' in person['roles']
                         and person['first_name'].lower() == first_name.lower() and person['last_name'].lower() == last_name.lower()]
    devices_in_unit = {
        'thermostats': [device for device in data['devices']['thermostats'] if
                        device['unit'] == int(accessible_unit) and (
                            device['admin_accessible'] == "true" if is_admin else True)],
        'lights': [device for device in data['devices']['lights'] if
                   device['unit'] == int(accessible_unit) and (
                       device['admin_accessible'] == "true" if is_admin else True)],
        'locks': [device for device in data['devices']['locks'] if
                  device['unit'] == int(accessible_unit) and (
                      device['admin_accessible'] == "true" if is_admin else True)],
    }

    users_df = pd.DataFrame(users_in_unit, columns=['first_name', 'last_name', 'unit', 'roles'])
    devices_df = pd.DataFrame(
        [{'category': category, 'model': device['model'], 'id': device['id']} for category, items in
         devices_in_unit.items() for device in items]
    )

    return users_df, devices_df


# Retrieve user information by name
def get_user_info(first_name, last_name):
    for person in data['people']:
        if (person['first_name'].lower() == first_name.lower() and person[
            'last_name'].lower() == last_name.lower() and 'Resident' in
                person['roles']):
            user_unit = person['unit']
            devices = {
                'thermostats': [device for device in data['devices']['thermostats'] if
                                device['unit'] == int(user_unit)],
                'lights': [device for device in data['devices']['lights'] if device['unit'] == int(user_unit)],
                'locks': [device for device in data['devices']['locks'] if device['unit'] == int(user_unit)],
            }

            user_df = pd.DataFrame([person])
            devices_df = pd.DataFrame(
                [{'category': category, 'model': device['model'], 'id': device['id']} for category, items in
                 devices.items() for device in items]
            )

            return user_df, devices_df
    return None, None


# To move in a new resident
def move_in_resident(first_name, last_name, unit):
    for person in data['people']:
        if person['first_name'].lower() == first_name.lower() and person['last_name'].lower() == last_name.lower() and \
                person['unit'] == unit:
            print(f"{first_name} {last_name} is already a resident in unit {unit}.")
            return

    new_resident = {
        "first_name": first_name,
        "last_name": last_name,
        "unit": unit,
        "roles": ["Resident"]
    }

    data['people'].append(new_resident)
    save_data()
    print(f"{first_name} {last_name} has been moved into unit {unit}.")


# To move out a resident
def move_out_resident(first_name, last_name):
    resident_exists = any(
        person['first_name'].lower() == first_name.lower() and person['last_name'].lower() == last_name.lower() for
        person in data['people'])

    if not resident_exists:
        print(f"{first_name} {last_name} does not exist in the system.")
        return

    data['people'] = [person for person in data['people'] if
                      not (person['first_name'].lower() == first_name.lower() and person[
                          'last_name'].lower() == last_name.lower())]
    save_data()
    print(f"{first_name} {last_name} has been moved out.")


# to save changes to property_data.json
def save_data(filename='property_data_changes.json'):
    try:
        with open(filename, 'w') as new_state_file:
            json.dump(data, new_state_file, indent=4)
        print(f"Changes saved to {filename}.")
    except Exception as e:
        print(f"Error saving data: {e}")


# Process menu choice based on user role
def process_menu_choice(choice, operator, first_name, last_name,):
    if choice == "1":
        if 'Admin' in operator['roles']:
            unit = input("Enter the unit number: ").strip()
            is_admin = True
        elif 'Resident' in operator['roles']:
            unit = operator['unit']
            is_admin = False
        users_df, devices_df = list_users_and_devices(first_name, last_name, unit, is_admin)

        print("\nResidents Data:")
        print(tabulate(users_df, headers='keys', tablefmt='simple_grid'))

        print("\nDevices Data:")
        print(tabulate(devices_df, headers='keys', tablefmt='simple_grid'))

    elif choice == "2":
        user_first_name = input("Enter user's first name: ").strip()
        user_last_name = input("Enter user's last name: ").strip()
        if 'Admin' in operator['roles'] or (first_name.lower() == user_first_name.lower() and last_name.lower() == user_last_name.lower()):
            user_df, user_devices_df = get_user_info(user_first_name, user_last_name)
            if user_df is not None:
                print("\nUser Information:")
                print(tabulate(user_df, headers='keys', tablefmt='simple_grid'))

                print("\nUser Devices:")
                print(tabulate(user_devices_df, headers='keys', tablefmt='simple_grid'))
            else:
                print("User not found or User role is not a Resident.")
        else:
            print("You don't have privileges to search other users information")

    elif choice == "3" and 'Admin' in operator['roles']:
        new_first_name = input("Enter new resident's first name: ").strip()
        new_last_name = input("Enter new resident's last name: ").strip()
        unit = input("Enter the unit number: ").strip()
        move_in_resident(new_first_name, new_last_name, unit)

    elif choice == "4" and 'Admin' in operator['roles']:
        out_first_name = input("Enter the first name of the resident to move out: ").strip()
        out_last_name = input("Enter the last name of the resident to move out: ").strip()
        move_out_resident(out_first_name, out_last_name)

    elif choice == "5":
        print("Exiting the system. Goodbye!")
        return False

    else:
        print("Invalid option")

    return True


# Main function to run the CLI
def main():
    print("Welcome to the Property Management System")
    first_name = input("Please Enter your first name: ").strip()
    last_name = input("Please Enter your last name: ").strip()

    operator = authenticate_operator(first_name, last_name)

    if not operator:
        print("You are not authorized to use this system.")
        return

    print("Your Authentication is successful..!")
    print(f"Welcome, {operator['first_name']} {operator['last_name']}!")

    while True:
        print("\nMenu:")
        print("1. View users and devices by unit")
        print("2. Search user information by name")
        if 'Admin' in operator['roles']:
            print("3. Move in a new resident")
            print("4. Move out an old resident")
        print("5. Exit")

        choice = input("Select an option (1-5): ").strip()
        if not process_menu_choice(choice, operator,  first_name, last_name):
            break


if __name__ == "__main__":
    if data:  # Proceed only if data is loaded successfully
        main()
