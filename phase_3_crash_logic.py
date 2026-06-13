import time

def evaluate_telemetry(g_force, speed_kmh, orientation_angle):
    """
    A declarative logic engine that evaluates raw sensor data (telemetry).
    It returns a True/False trigger and a status message.
    """
    
    # RULE 1: Vehicle Rollover
    # If the car tilts more than 75 degrees in any direction, it has flipped.
    if abs(orientation_angle) > 75:
        return True, "CRITICAL: Vehicle Rollover Detected!"

    # RULE 2: Severe Frontal/Rear Impact
    # High impact force (over 4.0 Gs) AND the vehicle comes to a near-instant stop.
    if g_force >= 4.0 and speed_kmh < 5:
        return True, "CRITICAL: High-Impact Collision Detected!"

    # RULE 3: False Positive Filter (Pothole or Hard Braking)
    # High G-force, BUT the car is still moving at a decent speed. 
    # This means they hit a pothole or slammed the brakes, but didn't crash.
    if g_force >= 3.0 and speed_kmh >= 5:
        return False, "WARNING: Hard braking or rough road detected. Monitoring..."

    # RULE 4: Normal Driving Conditions
    return False, "Status Normal: Sensors nominal."


def trigger_sos_protocol(status_message):
    """
    This function runs ONLY if the logic engine detects a real crash.
    It simulates the 10-second cancel window before calling Phase 2.
    """
    print("\n" + "="*50)
    print(f"🚨 {status_message} 🚨")
    print("="*50)
    print("WARNING: Auto-SOS will trigger in 5 seconds.")
    print("Press the screen to CANCEL if you are okay.")
    
    # Simulating a short countdown 
    for i in range(5, 0, -1):
        print(f"Countdown: {i}...")
        time.sleep(1) # Pauses the code for 1 second
        
    print("\n--> [SYSTEM] No cancellation received.")
    print("--> [SYSTEM] Auto-triggering Phase 2 (Spatial Router) for Police and Hospital...")


if __name__ == "__main__":
    # ---------------------------------------------------------
    # TEST SIMULATIONS: Let's feed the AI different sensor readings
    # ---------------------------------------------------------

    print("--- SIMULATION 1: Normal Highway Cruising ---")
    is_crash, msg = evaluate_telemetry(g_force=1.1, speed_kmh=80, orientation_angle=0)
    print(f"Result: {msg}\n")

    print("--- SIMULATION 2: Hitting a huge pothole / Speed breaker ---")
    is_crash, msg = evaluate_telemetry(g_force=3.5, speed_kmh=65, orientation_angle=5)
    print(f"Result: {msg}\n")

    print("--- SIMULATION 3: Severe Highway Collision ---")
    # 5.2 Gs of force, and the car's speed instantly drops to 0.
    is_crash, msg = evaluate_telemetry(g_force=5.2, speed_kmh=0, orientation_angle=12)
    print(f"Result: {msg}")
    
    if is_crash:
        trigger_sos_protocol(msg)