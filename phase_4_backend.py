import json
import os

PROFILE_FILE = "driver_profile.json"

# Global memory for the driver
driver_profile = {
    "name": "",
    "phone": "",
    "car_plate": ""
}

def load_profile():
    """Loads profile from JSON if it exists."""
    if os.path.exists(PROFILE_FILE):
        try:
            with open(PROFILE_FILE, "r") as file:
                data = json.load(file)
                driver_profile.update(data)
                return True
        except:
            return False
    return False

def save_profile(name, phone, plate):
    """Saves the given data to the JSON file."""
    driver_profile["name"] = name
    driver_profile["phone"] = phone
    driver_profile["car_plate"] = plate.upper()
    
    with open(PROFILE_FILE, "w") as file:
        json.dump(driver_profile, file)

def delete_profile():
    """Deletes the JSON file and clears memory."""
    if os.path.exists(PROFILE_FILE):
        os.remove(PROFILE_FILE)
    driver_profile["name"] = ""
    driver_profile["phone"] = ""
    driver_profile["car_plate"] = ""

def transmit_sos(category):
    """Simulates sending data to police/hospitals via radio."""
    print(f"\n[SYSTEM ALERT TRANSMITTED TO {category.upper()}]")
    print(f"Target Vehicle: {driver_profile['car_plate']}")
    print(f"Contact No: {driver_profile['phone']}")

def execute_auto_call():
    """Simulates the hardware making phone calls after a crash."""
    print("\n" + "="*50)
    try:
        print("🚨 HARDWARE TRIGGER: DIALING AUTHORITIES...")
    except UnicodeEncodeError:
        print("[SOS ALERT] HARDWARE TRIGGER: DIALING AUTHORITIES...")
    print("--> Calling National Emergency (108)")
    print(f"--> Calling Emergency Contact ({driver_profile['phone']})")
    print(f"--> Sending GPS Location and Plate [{driver_profile['car_plate']}]")
    print("="*50 + "\n")