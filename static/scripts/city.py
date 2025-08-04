import requests
import json
import urllib.parse


def get_all_states():
    try:
        res = requests.get(
            "https://iran-locations-api.vercel.app/api/v1/fa/states", timeout=10)
        if res.status_code == 200:
            data = res.json()
            if isinstance(data, list):
                return data
            print("Error: States response is not a list")
            return []
        else:
            print(f"Error: States API returned status code {res.status_code}")
            return []
    except requests.RequestException as e:
        print(f"Error fetching states: {e}")
        return []


def get_cities_for_state(state_name):
    try:
        encoded_state = urllib.parse.quote(state_name)
        url = f"https://iran-locations-api.vercel.app/api/v1/fa/cities?state={encoded_state}"
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            data = res.json()
            print(f"Raw response for {state_name}: {data}")
            if isinstance(data, list) and len(data) > 0 and "cities" in data[0]:
                return data[0]["cities"]
            elif isinstance(data, list):
                return data
            print(
                f"Error: Cities response for {state_name} does not match expected format: {data}")
            return []
        else:
            print(
                f"Error: Cities API for {state_name} returned status code {res.status_code}")
            return []
    except requests.RequestException as e:
        print(f"Error fetching cities for {state_name}: {e}")
        return []


def collect_all_destinations():
    states = get_all_states()
    destinations = []

    if not states:
        print("No states found. Exiting.")
        return destinations

    print("Provinces fetched:", [state.get("name") for state in states])

    for state in states:
        state_name = state.get("name")
        if not state_name:
            print("Warning: State name is missing, skipping.")
            continue

        cities = get_cities_for_state(state_name)
        for city in cities:
            city_name = city.get("name")
            if city_name:
                destination = {
                    "name": city_name,
                    "province": state_name}
                if "latitude" in city and city["latitude"] is not None:
                    destination["latitude"] = float(city["latitude"])
                if "longitude" in city and city["longitude"] is not None:
                    destination["longitude"] = float(city["longitude"])
                destinations.append(destination)
            else:
                print(
                    f"Warning: City name is missing for {state_name}, skipping: {city}")

    print(f"Collected {len(destinations)} cities.")

    with open('destinations.json', 'w', encoding='utf-8') as f:
        json.dump(destinations, f, ensure_ascii=False, indent=4)

    return destinations


output = collect_all_destinations()
print(json.dumps(output, ensure_ascii=False, indent=4))
