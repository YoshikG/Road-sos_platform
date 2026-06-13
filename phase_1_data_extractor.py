import requests
import csv
import os

def fetch_highway_data(radius_meters, center_lat, center_lon, filename):
    """
    Connects to the OpenStreetMap Overpass API, requests comprehensive emergency, 
    logistical, and survival data within a radius, and parses it into an offline CSV.
    """
    print(f"[*] Initializing connection to OpenStreetMap Overpass API...")
    url = "http://overpass-api.de/api/interpreter"
    
    # THE MASTER QUERY: Every possible highway scenario is covered here.
    query = f"""
    [out:json][timeout:30];
    (
      /* CRITICAL EMERGENCIES */
      node["amenity"="hospital"](around:{radius_meters},{center_lat},{center_lon});
      node["amenity"="police"](around:{radius_meters},{center_lat},{center_lon});
      
      /* VEHICLE LOGISTICS & REPAIR */
      node["amenity"="fuel"](around:{radius_meters},{center_lat},{center_lon});
      node["shop"="tyres"](around:{radius_meters},{center_lat},{center_lon});
      node["shop"="car_repair"](around:{radius_meters},{center_lat},{center_lon});
      node["shop"="motorcycle_repair"](around:{radius_meters},{center_lat},{center_lon});
      
      /* PERSONAL CRISIS (Lost Phone / No Cash / Locked Out) */
      node["amenity"="atm"](around:{radius_meters},{center_lat},{center_lon});
      node["shop"="mobile_phone"](around:{radius_meters},{center_lat},{center_lon});
      node["shop"="locksmith"](around:{radius_meters},{center_lat},{center_lon});
      
      /* FOOD & SAFE REST ZONES */
      node["amenity"="restaurant"](around:{radius_meters},{center_lat},{center_lon});
      node["amenity"="fast_food"](around:{radius_meters},{center_lat},{center_lon});
      node["amenity"="cafe"](around:{radius_meters},{center_lat},{center_lon});
    );
    out center;
    """
    
    headers = {
        'User-Agent': 'RoadSoS_Hackathon_Platform/1.0 (Testing Data Extraction)'
    }
    
    try:
        print(f"[*] Fetching data for a {radius_meters/1000}km radius...")
        response = requests.post(url, data={'data': query}, headers=headers)
        response.raise_for_status() 
        
        data = response.json()
        elements = data.get('elements', [])
        
        if not elements:
            print("[!] No data found for this region. Try increasing the radius.")
            return

        print(f"[*] Successfully retrieved {len(elements)} raw data points.")
        save_to_csv(elements, filename)
        
    except requests.exceptions.RequestException as e:
        print(f"[!] Network or API Error: {e}")

def save_to_csv(elements, filename):
    """
    Translates the messy JSON data into a clean, uniform CSV file.
    """
    print(f"[*] Formatting data and writing to {filename}...")
    headers = ['Category', 'Name', 'Latitude', 'Longitude']
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        
        saved_count = 0
        for el in elements:
            lat = el.get('lat')
            lon = el.get('lon')
            tags = el.get('tags', {})
            
            # Categorize the data cleanly
            if 'amenity' in tags:
                category = tags['amenity'].capitalize()
            elif 'shop' in tags:
                category = tags['shop'].capitalize()
            else:
                category = "Unknown"
            
            # Handle missing names safely
            name = tags.get('name', f'Unnamed {category}')
            
            writer.writerow([category, name, lat, lon])
            saved_count += 1
            
        print(f"[*] SUCCESS: {saved_count} locations saved safely.")
        print(f"[*] File located at: {os.path.abspath(filename)}")

if __name__ == "__main__":
    # Settings for Phase 1 Test Run (Centered around Chirala)
    fetch_highway_data(
        radius_meters=30000, 
        center_lat=15.8246, 
        center_lon=80.3521, 
        filename="Chirala_Highway_Data.csv"
    )