#!/usr/bin/env python3
import datetime
import os
import requests
import sys

ASTRONOMYAPI_ID = os.environ.get("eb24270e-a8cf-4a9f-b1b4-a461f5f0c4e6")
ASTRONOMYAPI_SECRET = os.environ.get("84a1627a903cf9776f51556940afe16838e2c7eddb23650053bd94f6b37589beec0bd8ece903094bfdaf2121dbd2cce3f8465c57cc8cf59016f825db36faa2cb51c2d4f63ca8dbc039fe67b58b58bafad7ec42e01679b544d7190ad15a6d83aff614ae90d02e6731077feac1ad4f7869")

def get_observer_location():
    """Returns the longitude and latitude for the location of this machine.
    Returns:
    str: latitude
    str: longitude"""
    url = "http://ip-api.com/json/"
    try:
        response = requests.get(url)
        if not response.status_code == 200:
            return None, None
    except requests.exceptions.ConnectionError:
        return None, None
    except requests.exceptions.Timeout:
        return None, None
    data = response.json()
    # NOTE: Replace with your real return values!
    return data.get("lat"), data.get("lon")

def get_sun_position(latitude, longitude, body="sun"):
    """Returns the current position of the sun in the sky at the specified location
    Parameters:
    latitude (str)
    longitude (str)
    Returns:
    float: azimuth
    float: altitude
    """
    body = body or "sun"
    url = f"https://api.astronomyapi.com/api/v2/bodies/positions/{body}"
    now = datetime.datetime.now()
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "elevation": 0,
        "from_date": now.date().isoformat(),
        "to_date": now.date().isoformat(),
        "time": now.strftime("%H:%M:%S"),
    }
    try:
        response = requests.get(
            url, params=params,
            auth=(ASTRONOMYAPI_ID, ASTRONOMYAPI_SECRET))
        if not response.status_code == 200:
            return None, None
    except requests.exceptions.ConnectionError:
        return None, None
    except requests.exceptions.Timeout:
        return None, None
    data = response.json()
    body_data = data["data"]["table"]["rows"][0]["cells"][0]
    position = body_data["position"]["horizontal"]
    alt = position["altitude"]["degrees"]
    az = position["azimuth"]["degrees"]
    return az, alt

def print_position(azimuth, altitude):
    """Prints the position of the sun in the sky using the supplied coordinates
    Parameters:
    azimuth (float)
    altitude (float)"""
    print(
        f"The Sun is currently at: "
        f"{altitude} deg altitude, {azimuth} deg azimuth."
    )

if __name__ == "__main__":
    latitude, longitude = get_observer_location()
    if latitude is None or longitude is None:
        print("Could not find your location by IP!")
        sys.exit(1)
    azimuth, altitude = get_sun_position(latitude, longitude)
    if azimuth is None or altitude is None:
        print("Could not get Sun position from Astronomy API")
        sys.exit(2)
    print_position(azimuth, altitude)