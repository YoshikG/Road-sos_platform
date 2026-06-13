from flask import Flask, render_template, request, jsonify
import phase_4_backend as backend
import random
import logging

# Suppress 'Running on...' server startup banner output except for 127.0.0.1 link
class WerkzeugStartupFilter(logging.Filter):
    def filter(self, record):
        if isinstance(record.msg, str) and 'Running on' in record.msg:
            lines = record.msg.split('\n')
            filtered_lines = []
            for line in lines:
                if 'Running on' in line:
                    if '127.0.0.1' in line:
                        filtered_lines.append(line)
                else:
                    filtered_lines.append(line)
            record.msg = '\n'.join(filtered_lines)
        return True

logging.getLogger('werkzeug').addFilter(WerkzeugStartupFilter())

app = Flask(__name__)

# ---------------------------------------------------
# HOME
# ---------------------------------------------------

@app.route('/')
def home():
    return render_template('index.html')

# ---------------------------------------------------
# PROFILE
# ---------------------------------------------------

@app.route('/api/profile', methods=['GET', 'POST', 'DELETE'])
def manage_profile():

    if request.method == 'GET':
        exists = backend.load_profile()
        return jsonify({
            "exists": exists,
            "profile": backend.driver_profile
        })

    elif request.method == 'POST':

        data = request.json

        backend.save_profile(
            data.get('name'),
            data.get('phone'),
            data.get('car_plate')
        )

        return jsonify({
            "status": "success"
        })

    elif request.method == 'DELETE':

        backend.delete_profile()

        return jsonify({
            "status": "success"
        })

# ---------------------------------------------------
# SOS
# ---------------------------------------------------

@app.route('/api/sos', methods=['POST'])
def instant_sos():

    backend.execute_auto_call()

    return jsonify({
        "status": "CRITICAL ALERT SENT"
    })

# ---------------------------------------------------
# CHATBOT
# ---------------------------------------------------

@app.route('/chat', methods=['POST'])
def chat():

    user_message = request.json.get("message", "").lower()

    action = "chat"
    target = ""
    distance = 0.0

    # Mechanic

    if any(word in user_message for word in [
        "mechanic",
        "breakdown",
        "tyre",
        "repair"
    ]):

        target = "Highway Auto Care (Mechanic)"

        distance = round(random.uniform(1.0, 3.5), 1)

        response = f"Locating nearest mechanic for vehicle {backend.driver_profile.get('car_plate', 'Unknown')}."

        action = "route"

        backend.transmit_sos("Mechanic")

    # Police

    elif any(word in user_message for word in [
        "police",
        "crash",
        "accident",
        "help"
    ]):

        target = "Central Police Station"

        distance = round(random.uniform(1.0, 3.0), 1)

        response = "CRITICAL EMERGENCY. Routing to nearest Police Station..."

        action = "route"

        backend.execute_auto_call()

    # Fire Station

    elif any(word in user_message for word in [
        "fire",
        "burn",
        "smoke"
    ]):

        target = "Nearest Fire Station"

        distance = round(random.uniform(1.0, 4.0), 1)

        response = "EMERGENCY. Finding the fastest route to the nearest fire station."

        action = "route"

    # Hospital

    elif any(word in user_message for word in [
        "hospital",
        "medical",
        "heart",
        "hurt"
    ]):

        target = "Nearest Local Clinic"

        distance = round(random.uniform(0.3, 0.8), 1)

        response = "Medical emergency detected. Finding the fastest route to the nearest hospital."

        action = "route"

        backend.transmit_sos("Hospital")

    # Pharmacy

    elif any(word in user_message for word in [
        "pharmacy",
        "medicine",
        "drugs",
        "pills"
    ]):

        target = "Nearest Pharmacy"

        distance = round(random.uniform(0.5, 1.5), 1)

        response = "Finding the fastest route to the nearest pharmacy."

        action = "route"

    # ATM

    elif any(word in user_message for word in [
        "atm",
        "cash",
        "money"
    ]):

        target = "24/7 Local ATM"

        distance = round(random.uniform(0.5, 2.0), 1)

        response = "Locating nearest secure ATM."

        action = "route"

    # Locksmith

    elif any(word in user_message for word in [
        "lock",
        "key",
        "locksmith",
        "locked"
    ]):

        target = "24/7 Mobile Locksmith"

        distance = round(random.uniform(1.0, 4.0), 1)

        response = "Locating nearest mobile locksmith for your vehicle."

        action = "route"

    # Greetings

    elif any(word in user_message for word in [
        "hello",
        "hi",
        "hey",
        "morning"
    ]):

        name = backend.driver_profile.get("name", "Driver")

        response = f"Hello {name}! I am monitoring your vehicle telemetry. Drive safe!"

    elif "how are you" in user_message:

        response = "I am operating at 100% capacity. Ready to assist you."

    elif "who are you" in user_message or "what can you do" in user_message:

        response = "I am RoadSoS, your AI co-pilot. I can call the police or navigate you to safety during a crisis."

    else:

        response = "I am actively monitoring your route. Let me know if you need assistance."

    return jsonify({
        "response": response,
        "action": action,
        "target": target,
        "distance": distance
    })

# ---------------------------------------------------
# TELEMETRY
# ---------------------------------------------------

@app.route('/api/telemetry', methods=['POST'])
def telemetry_monitor():

    data = request.json

    status = data.get('status', 'normal')

    location = data.get('location', 'Unknown Location')

    if not backend.driver_profile.get("name"):
        backend.load_profile()

    name = backend.driver_profile.get("name", "Unknown Driver")

    plate = backend.driver_profile.get("car_plate", "Unknown Plate")

    # Heart attack

    if status == 'heart_attack' or status == 'abnormal_steering':

        backend.transmit_sos("Hospital")

        alert_msg = f"MEDICAL EMERGENCY DETECTED: {name} ({plate}) at {location}"

        return jsonify({
            "alert": True,
            "message": alert_msg,
            "type": "medical"
        })

    # Crash

    elif status == 'accident' or status == 'crash':

        backend.execute_auto_call()

        alert_msg = f"CRITICAL CRASH DETECTED: {name} ({plate}) at {location}"

        return jsonify({
            "alert": True,
            "message": alert_msg,
            "type": "crash"
        })

    return jsonify({
        "alert": False,
        "message": "Telemetry normal"
    })

# ---------------------------------------------------
# RUN
# ---------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
