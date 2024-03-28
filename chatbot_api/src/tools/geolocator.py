# https://nominatim.org/release-docs/develop/api/Search/#geocodejson


# https://project-osrm.org/docs/v5.24.0/api/?language=python#table-service
# "https://routing.openstreetmap.de/routed-foot/route/v1/"

import requests

headers = {
    'Accept-language': "en-US,en;q=0.9",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    'Content-Type':"text"
}

def get_geolocation(address):
    print(address)
    url = f"https://nominatim.openstreetmap.org/search?q={address}&format=geojson"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data:
            if data['features']:
                lon, lat = data['features'][0]['geometry']['coordinates']
                return lon, lat
    return None
    
def get_triptime(start_lon_lat, 
                 end_lon_lat,
                profile = "driving"):

    url = f"http://router.project-osrm.org/table/v1/{profile}/{start_lon_lat[0]},{start_lon_lat[-1]};{end_lon_lat[0]},{end_lon_lat[-1]}"
    response = requests.get(url, headers=headers)
    if response.status_code ==200:
        data = response.json()
        if data:
            duration = max(data['durations'][0])
            return duration
    return None