import requests
import csv
from datetime import datetime


client_id = "WuFldvTb86qCSmrVkXkKpJdcz8dgad3k"
client_secret = "9fFtUVNFyro6yQH1B5tiIyEY9b5PD6KiPQeDq6QdYygktiX59OTbfDxlz7u2bVGf"
token_url = "https://api2.arduino.cc/iot/v1/clients/token"

device_id = "51f1956e-1d79-4215-ad2e-e815cab2a2a9"
property_id_x = "cfb947a7-e33b-43b2-ab16-c79d4c171caf"
property_id_y = "af4da77f-d034-4829-ab57-c362a501564f"
property_id_z = "55a168d1-6d6a-4923-b69c-c5bac9fc34db"

def get_oauth_token():
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "audience": "https://api2.arduino.cc/iot"
    }

    response = requests.post(token_url, headers=headers, data=data)
    response_data = response.json()
    print(f"OAuth Token: {response_data['access_token']}")
    return response_data["access_token"]

# Fetch accelerometer data from Arduino Cloud
def fetch_accelerometer_data(token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Fetch X, Y, Z values
    url_x = f"https://api2.arduino.cc/iot/v2/things/{device_id}/properties/{property_id_x}"
    url_y = f"https://api2.arduino.cc/iot/v2/things/{device_id}/properties/{property_id_y}"
    url_z = f"https://api2.arduino.cc/iot/v2/things/{device_id}/properties/{property_id_z}"

    x_value = requests.get(url_x, headers=headers).json().get("last_value")
    y_value = requests.get(url_y, headers=headers).json().get("last_value")
    z_value = requests.get(url_z, headers=headers).json().get("last_value")

    print(f"Fetched X: {x_value}, Y: {y_value}, Z: {z_value}")
    return x_value, y_value, z_value

# Write data to CSV file
def write_data_to_csv(x, y, z):
    with open("accelerometer_data.csv", mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), x, y, z])

# Main code to run the data-fetching loop
if __name__ == "__main__":
    token = get_oauth_token()

    # Write CSV headers
    with open("accelerometer_data.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "x", "y", "z"])

    while True:
        # Fetch the data
        x, y, z = fetch_accelerometer_data(token)
        if x is not None:
            write_data_to_csv(x, y, z)
