import tkinter as tk
from tkinter import messagebox
import phase_4_backend as backend  # CONNECTING TO PHASE 4!

# --- Global State & Configuration ---
is_online = True
animation_id = None
pulse_radius = 20
crash_timer_id = None
countdown_time = 5

# --- Theming Dictionaries ---
themes = {
    "online": {
        "bg": "#0f172a", "text": "#38bdf8", "sub_text": "#94a3b8",
        "btn_medical": "#ef4444", "btn_police": "#3b82f6", 
        "btn_mechanic": "#f59e0b", "btn_atm": "#8b5cf6",
        "map_bg": "#1e293b", "route": "#10b981", "pulse": "#10b981"
    },
    "offline": {
        "bg": "#f4f6f9", "text": "#2c3e50", "sub_text": "#7f8c8d",
        "btn_medical": "#ff4d4d", "btn_police": "#3385ff", 
        "btn_mechanic": "#ffb366", "btn_atm": "#9b59b6",
        "map_bg": "#e8f4f8", "route": "#95a5a6", "pulse": None
    }
}

# ==========================================
# UI TO BACKEND LOGIC BRIDGE
# ==========================================
def process_ui_login():
    name = entry_name.get().strip()
    phone = entry_phone.get().strip()
    plate = entry_plate.get().strip()
    pwd = entry_pwd.get().strip()
    
    if not name or not phone or not plate or not pwd:
        messagebox.showerror("Setup Error", "All fields are required.")
        return
        
    # Send data to Phase 4 to save
    backend.save_profile(name, phone, plate)
    transition_to_dashboard()

def trigger_delete_profile():
    confirm = messagebox.askyesno("Reset App", "Delete driver profile and reset app?")
    if confirm:
        # Tell Phase 4 to wipe the data
        backend.delete_profile()
        
        # Reset the UI
        entry_name.delete(0, tk.END)
        entry_phone.delete(0, tk.END)
        entry_plate.delete(0, tk.END)
        entry_pwd.delete(0, tk.END)
        dashboard_frame.pack_forget()
        btn_network.pack_forget()
        login_frame.pack(fill="both", expand=True)

def transition_to_dashboard():
    login_frame.pack_forget()
    btn_network.pack(fill="x")
    dashboard_frame.pack(fill="both", expand=True)
    
    # Read the saved plate and name from Phase 4
    sub_header.config(text=f"Vehicle: {backend.driver_profile['car_plate']} | Driver: {backend.driver_profile['name']}")
    apply_theme()

# ==========================================
# DASHBOARD VISUALS & ANIMATIONS
# ==========================================
def toggle_network():
    global is_online
    is_online = not is_online
    if is_online:
        btn_network.config(text="📶 STATUS: ONLINE (LIVE GPS)", bg="#10b981", fg="white")
    else:
        btn_network.config(text="⚠️ STATUS: OFFLINE (SURVIVAL MODE)", bg="#e74c3c", fg="white")
    apply_theme()

def apply_theme():
    theme = themes["online"] if is_online else themes["offline"]
    root.configure(bg=theme["bg"])
    dashboard_frame.configure(bg=theme["bg"])
    tracker_frame.configure(bg=theme["bg"])
    header.configure(bg=theme["bg"], fg=theme["text"])
    sub_header.configure(bg=theme["bg"], fg=theme["sub_text"])
    tracker_title.configure(bg=theme["bg"], fg=theme["text"])
    tracker_info.configure(bg=theme["bg"])
    sep.configure(bg=theme["bg"])
    btn_medical.configure(bg=theme["btn_medical"])
    btn_police.configure(bg=theme["btn_police"])
    btn_mechanic.configure(bg=theme["btn_mechanic"])
    btn_atm.configure(bg=theme["btn_atm"])

def animate_radar():
    global animation_id, pulse_radius
    map_canvas.delete("pulse_ring")
    if is_online and tracker_frame.winfo_ismapped():
        map_canvas.create_oval(60 - pulse_radius, 320 - pulse_radius, 60 + pulse_radius, 320 + pulse_radius, 
                               outline=themes["online"]["pulse"], width=2, tags="pulse_ring")
        pulse_radius += 2
        if pulse_radius > 40: pulse_radius = 5
        animation_id = root.after(50, animate_radar)

def draw_map():
    map_canvas.delete("all")
    theme = themes["online"] if is_online else themes["offline"]
    map_canvas.configure(bg=theme["map_bg"], highlightbackground=theme["sub_text"])
    map_canvas.create_line(60, 320, 320, 60, width=12, fill=theme["route"], capstyle="round")
    map_canvas.create_line(60, 320, 320, 60, width=2, fill="white", dash=(15, 15))
    map_canvas.create_oval(300, 40, 340, 80, fill="#e74c3c", outline="white", width=2)
    map_canvas.create_text(320, 25, text="Target", font=("Arial", 10, "bold"), fill="#e74c3c")
    map_canvas.create_oval(50, 310, 70, 330, fill="#3498db", outline="white", width=2)
    map_canvas.create_text(60, 350, text="You", font=("Arial", 10, "bold"), fill="#3498db")

def show_tracker(category, distance):
    dashboard_frame.pack_forget()
    tracker_frame.pack(fill="both", expand=True)
    tracker_title.config(text=f"Routing to Nearest {category}...")
    
    # Tell Phase 4 to simulate the radio transmission
    backend.transmit_sos(category)
    
    if is_online:
        tracker_info.config(text=f"LIVE GPS: {distance} km | ETA: {int(distance * 1.5)} mins", fg="#10b981")
    else:
        tracker_info.config(text=f"OFFLINE DISTANCE: {distance} km | ETA: --", fg="#e74c3c")
    draw_map()
    if is_online: animate_radar()

def return_to_dashboard():
    global animation_id
    if animation_id: root.after_cancel(animation_id)
    tracker_frame.pack_forget()
    dashboard_frame.pack(fill="both", expand=True)

def trigger_medical_sos(): show_tracker("Hospital", 4.2)
def trigger_police_sos(): show_tracker("Police Station", 2.8)
def trigger_mechanic(): show_tracker("Mechanic", 6.5)
def trigger_atm(): show_tracker("ATM", 1.5)

# ==========================================
# UI CRASH COUNTDOWN
# ==========================================
def execute_emergency_calls(alert_window, lbl_text, btn_cancel):
    btn_cancel.destroy()
    alert_window.configure(bg="#000000")
    lbl_text.config(text=f"🚨 INITIATING EMERGENCY CALLS 🚨\n\nDialing 108...\nDialing Family...", fg="#10b981", bg="#000000")
    
    # Tell Phase 4 to run the terminal simulation
    backend.execute_auto_call()
    
    tk.Button(alert_window, text="END CALLS & RETURN", font=("Arial", 12, "bold"), 
              bg="#e74c3c", fg="white", command=alert_window.destroy).pack(pady=20)

def countdown_crash(alert_window, lbl_text, btn_cancel):
    global countdown_time, crash_timer_id
    if countdown_time > 0:
        lbl_text.config(text=f"HIGH-IMPACT CRASH DETECTED!\nVehicle: {backend.driver_profile['car_plate']}\n\nAuto-dialing in {countdown_time}...")
        countdown_time -= 1
        crash_timer_id = root.after(1000, lambda: countdown_crash(alert_window, lbl_text, btn_cancel))
    else:
        execute_emergency_calls(alert_window, lbl_text, btn_cancel)

def cancel_crash(alert_window):
    global crash_timer_id
    if crash_timer_id: root.after_cancel(crash_timer_id)
    alert_window.destroy()

def simulate_crash():
    global countdown_time
    countdown_time = 5
    alert = tk.Toplevel(root)
    alert.title("CRITICAL EMERGENCY")
    alert.geometry("450x300")
    alert.configure(bg="red")
    
    lbl = tk.Label(alert, text="", fg="white", bg="red", font=("Arial", 14, "bold"))
    lbl.pack(pady=40)
    
    cancel_btn = tk.Button(alert, text="I AM OKAY (CANCEL EMERGENCY)", font=("Arial", 12, "bold"), 
                           bg="white", fg="red", command=lambda: cancel_crash(alert))
    cancel_btn.pack()
    countdown_crash(alert, lbl, cancel_btn)

# ==========================================
# TKINTER WINDOW SETUP
# ==========================================
root = tk.Tk()
root.title("RoadSoS - Vehicle HUD")
root.geometry("450x780") 
root.configure(bg="#0f172a")

btn_network = tk.Button(root, text="📶 STATUS: ONLINE (LIVE GPS)", font=("Arial", 10, "bold"), bg="#10b981", fg="white", relief="flat", command=toggle_network)

# --- FRAME 0: LOGIN ---
login_frame = tk.Frame(root, bg="#0f172a")
tk.Label(login_frame, text="RoadSoS", font=("Helvetica", 32, "bold"), fg="#38bdf8", bg="#0f172a").pack(pady=(40, 5))
tk.Label(login_frame, text="Emergency Profile Setup", font=("Helvetica", 14), fg="#94a3b8", bg="#0f172a").pack(pady=(0, 30))

tk.Label(login_frame, text="Driver Full Name:", fg="white", bg="#0f172a", font=("Arial", 10, "bold")).pack()
entry_name = tk.Entry(login_frame, font=("Arial", 14), width=25, justify="center")
entry_name.pack(pady=(0, 15))
tk.Label(login_frame, text="Emergency Phone Number:", fg="white", bg="#0f172a", font=("Arial", 10, "bold")).pack()
entry_phone = tk.Entry(login_frame, font=("Arial", 14), width=25, justify="center")
entry_phone.pack(pady=(0, 15))
tk.Label(login_frame, text="Vehicle License Plate:", fg="white", bg="#0f172a", font=("Arial", 10, "bold")).pack()
entry_plate = tk.Entry(login_frame, font=("Arial", 14), width=25, justify="center")
entry_plate.pack(pady=(0, 15))
tk.Label(login_frame, text="Secure Password:", fg="white", bg="#0f172a", font=("Arial", 10, "bold")).pack()
entry_pwd = tk.Entry(login_frame, font=("Arial", 14), width=25, justify="center", show="*")
entry_pwd.pack(pady=(0, 25))

tk.Button(login_frame, text="💾 SAVE & SECURE LOGIN", font=("Arial", 14, "bold"), bg="#10b981", fg="white", width=20, height=2, command=process_ui_login).pack()

# --- FRAME 1: DASHBOARD ---
dashboard_frame = tk.Frame(root)
header = tk.Label(dashboard_frame, text="RoadSoS", font=("Helvetica", 28, "bold"))
header.pack(pady=(15, 0))
sub_header = tk.Label(dashboard_frame, text="", font=("Helvetica", 12)) 
sub_header.pack(pady=(0, 10))

btn_medical = tk.Button(dashboard_frame, text="🚑 MEDICAL SOS", font=("Arial", 16, "bold"), fg="white", width=25, height=2, command=trigger_medical_sos)
btn_medical.pack(pady=8)
btn_police = tk.Button(dashboard_frame, text="🚓 POLICE SOS", font=("Arial", 16, "bold"), fg="white", width=25, height=2, command=trigger_police_sos)
btn_police.pack(pady=8)
btn_mechanic = tk.Button(dashboard_frame, text="🔧 BREAKDOWN / MECHANIC", font=("Arial", 16, "bold"), fg="white", width=25, height=2, command=trigger_mechanic)
btn_mechanic.pack(pady=8)
btn_atm = tk.Button(dashboard_frame, text="🏧 FIND NEAREST ATM", font=("Arial", 16, "bold"), fg="white", width=25, height=2, command=trigger_atm)
btn_atm.pack(pady=8)

sep = tk.Label(dashboard_frame, text="--------------------------------------------------")
sep.pack(pady=5)
btn_crash = tk.Button(dashboard_frame, text="⚠️ SIMULATE HARDWARE CRASH", font=("Arial", 12, "bold"), bg="#f1c40f", fg="black", width=30, height=2, command=simulate_crash)
btn_crash.pack(pady=5)

btn_delete = tk.Button(dashboard_frame, text="⚙️ DELETE / RESET PROFILE", font=("Arial", 10, "bold"), bg="#7f8c8d", fg="white", width=25, relief="flat", command=trigger_delete_profile)
btn_delete.pack(pady=10)

# --- FRAME 2: TRACKER MAP ---
tracker_frame = tk.Frame(root)
tracker_title = tk.Label(tracker_frame, font=("Helvetica", 18, "bold"))
tracker_title.pack(pady=(20, 5))
tracker_info = tk.Label(tracker_frame, font=("Helvetica", 12, "bold"))
tracker_info.pack(pady=(0, 15))
map_canvas = tk.Canvas(tracker_frame, width=380, height=380, highlightthickness=2)
map_canvas.pack(pady=10)
tk.Button(tracker_frame, text="❌ CANCEL ROUTE", font=("Arial", 14, "bold"), bg="#95a5a6", fg="white", width=20, height=2, command=return_to_dashboard).pack(pady=20)

# --- STARTUP LOGIC ---
if backend.load_profile():  # Ask Phase 4 if a profile exists
    transition_to_dashboard()
else:
    login_frame.pack(fill="both", expand=True)

root.mainloop()