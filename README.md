# Property Management System

This is a command-line tool for managing a property system, designed to help operators retrieve and manage user and device information. The system allows for resident management, device control, and user information retrieval based on authorization roles.

## Features

- **User Authentication**: Authenticate operators based on first name and last name.
- **Role-Based Access Control**:
  - Admin users can view and control all devices, as well as move residents in and out.
  - Resident users can view their own information and devices associated with their unit.
- **Unit Lookup**: View all residents and devices in a given unit.
- **User Lookup**: Retrieve information about any user by their first and last name.
- **Resident Management**: Admins can move in or move out residents from the property.

## Prerequisites

- Python 3.9+
- tabulate
- pandas
- JSON file: `property_data.json` (provided in the same directory)

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/RajashekarPunna/property-management-system.git
cd property-management-system 
```

### 2. Follow the prompts

- Enter your first name and last name to authenticate as an operator.
- Use the menu options to interact with the system:
  - View users and devices by unit.
  - Search user information by name.
  - (Admin only) Move in a new resident.
  - (Admin only) Move out a resident.

### 3. Data Changes
- Changes to residents (moving in or out) will be saved in a new file property_data_changes.json. The original property_data.json remains unchanged.






