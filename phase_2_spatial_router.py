import csv
import math

def calculate_haversine(lat1, lon1, lat2, lon2):
    """
    Calculates the exact distance in kilometers between two GPS coordinates
    accounting for the curvature of the Earth.
    """
    R = 6371.0  # Radius of Earth in kilometers
    
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = math.sin(dlat / 2)**2 + \
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

def find_nearest_facility(user_lat, user_lon, category_needed, database_file="Chirala_Highway_Data.csv"):
    """
    Scans the offline database to find the absolute closest facility.
    Includes smart filtering for broad terms like 'Mechanic'.
    """
    nearest_facility = None
    shortest_distance = float('inf') # Start with an infinitely large distance
    
    # The Smart Filter: Link the word "Mechanic" to both repair types
    search_targets = [category_needed.lower()]
    if category_needed.lower() == "mechanic":
        search_targets = ["car_repair", "motorcycle_repair"]
        
    print(f"\n[SOS TRIGGERED] Searching offline database for nearest: {category_needed.upper()}")
    
    try:
        with open(database_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                # Check if the row's category matches ANY of our targets
                if row['Category'].lower() in search_targets:
                    fac_lat = float(row['Latitude'])
                    fac_lon = float(row['Longitude'])
                    
                    # Calculate distance
                    distance = calculate_haversine(user_lat, user_lon, fac_lat, fac_lon)
                    
                    # If this is closer than the last one we found, update our record
                    if distance < shortest_distance:
                        shortest_distance = distance
                        nearest_facility = row
                        
        if nearest_facility:
            print("--------------------------------------------------")
            print(f"✅ MATCH FOUND: {nearest_facility['Name']} ({nearest_facility['Category']})")
            print(f"📍 LOCATION: {nearest_facility['Latitude']}, {nearest_facility['Longitude']}")
            print(f"📏 DISTANCE: {round(shortest_distance, 2)} km away")
            print("--------------------------------------------------")
            return nearest_facility
        else:
            print(f"❌ No {category_needed} found in the local database.")
            return None
            
    except FileNotFoundError:
        print(f"[!] Error: The database file '{database_file}' is missing. Did you run Phase 1?")

if __name__ == "__main__":
    # Let's simulate Srinu's car breaking down near Chirala.
    # His car's GPS hardware feeds these exact coordinates into the app:
    srinu_lat = 15.8350
    srinu_lon = 80.3600
    
    # Scenario 1: Srinu has a heart attack
    find_nearest_facility(srinu_lat, srinu_lon, "Hospital")
    
    # Scenario 2: Srinu locks his keys in the car
    find_nearest_facility(srinu_lat, srinu_lon, "Locksmith")
    
    # Scenario 3: Srinu's tire bursts and he hits the general "Mechanic" button
    find_nearest_facility(srinu_lat, srinu_lon, "Mechanic")