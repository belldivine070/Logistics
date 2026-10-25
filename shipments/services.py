import requests
import time


def geocode_address(query_string):
    """
    Geocodes an address string using the free OpenStreetMap Nominatim API.
    Returns (latitude, longitude) as floats or (None, None) if failed.
    """
    url = "https://nominatim.openstreetmap.org/search"
    headers = {
        'User-Agent': 'USLogisticsPlatform/1.0 (contact@uslogistics-example.com)'
    }
    params = {
        'q': query_string,
        'format': 'json',
        'limit': 1
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                lat = float(data[0]['lat'])
                lon = float(data[0]['lon'])
                return lat, lon
    except Exception as e:
        # Log geocoding failure gracefully
        print(f"Geocoding error for query '{query_string}': {e}")
        
    return None, None