import json
import math

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = (math.sin(dLat/2) * math.sin(dLat/2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dLon/2) * math.sin(dLon/2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def estimate_scores(city):
    name = city["name"]
    province = city["province"]
    lat = city["latitude"]
    lon = city["longitude"]
    
    scores = {
        "proximate_nature": 0.4,
        "thrill_activities": 0.2,
        "cultural_sites": 0.3,
        "spa_facilities": 0.2,
    }


    natural_attractions = {
        "دریاچه ارومیه": (37.7, 45.3),
        "دماوند": (35.95, 52.11),
        "جنگل های شمال": (36.8, 50.9),
        "کویر مرکزی": (33.6, 54.3)
    }
    
    min_nature_dist = float('inf')
    for _, (att_lat, att_lon) in natural_attractions.items():
        dist = calculate_distance(lat, lon, att_lat, att_lon)
        if dist < min_nature_dist:
            min_nature_dist = dist
    
    if min_nature_dist < 50:
        scores["proximate_nature"] = 0.9
    elif min_nature_dist < 100:
        scores["proximate_nature"] = 0.7
    elif min_nature_dist < 200:
        scores["proximate_nature"] = 0.5

    if province in ["گیلان", "مازندران", "گلستان"]:
        scores["proximate_nature"] = max(scores["proximate_nature"], 0.85)
    elif name in ["شیراز", "اصفهان", "تبریز"]:
        scores["proximate_nature"] = max(scores["proximate_nature"], 0.6)

    ski_resorts = {
        "دیزین": (36.06, 51.24),
        "شهرکرد": (32.19, 50.51),
        "توچال": (35.81, 51.42)
    }
    
    for resort, (res_lat, res_lon) in ski_resorts.items():
        if calculate_distance(lat, lon, res_lat, res_lon) < 80:
            scores["thrill_activities"] = max(scores["thrill_activities"], 0.7)
            break
    
    if name in ["تهران", "مشهد", "کیش"]:
        scores["thrill_activities"] = max(scores["thrill_activities"], 0.6)
    elif province in ["چهارمحال بختیاری", "لرستان"]:
        scores["thrill_activities"] = max(scores["thrill_activities"], 0.5)

    cultural_cities = ["اصفهان", "شیراز", "یزد", "تبریز", "مشهد", "کرمان"]
    if name in cultural_cities:
        scores["cultural_sites"] = 0.9
    else:
        cultural_centers = {
            "اصفهان": (32.65, 51.67),
            "شیراز": (29.61, 52.54),
            "تبریز": (38.08, 46.30)
        }
        
        min_culture_dist = float('inf')
        for _, (cul_lat, cul_lon) in cultural_centers.items():
            dist = calculate_distance(lat, lon, cul_lat, cul_lon)
            if dist < min_culture_dist:
                min_culture_dist = dist
        
        if min_culture_dist < 100:
            scores["cultural_sites"] = max(scores["cultural_sites"], 0.7)
        elif min_culture_dist < 200:
            scores["cultural_sites"] = max(scores["cultural_sites"], 0.5)

    luxury_cities = ["تهران", "مشهد", "کیش", "اصفهان", "شیراز"]
    if name in luxury_cities:
        scores["spa_facilities"] = 0.8
    elif province in ["مازندران", "گیلان"]:
        scores["spa_facilities"] = 0.6
    
    for key in scores:
        scores[key] = round(scores[key], 2)
    
    return scores

with open('destinations.json', 'r', encoding='utf-8') as f:
    cities = json.load(f)

for city in cities:
    city.update(estimate_scores(city))

with open('destinations.json', 'w', encoding='utf-8') as f:
    json.dump(cities, f, ensure_ascii=False, indent=4)

print("تخمین دقیق با موفقیت انجام شد!")