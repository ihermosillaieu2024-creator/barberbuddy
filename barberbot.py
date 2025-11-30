from datetime import date as _date
from pathlib import Path
import json

# === RUTA PORTABLE A LA DB (misma carpeta que este .py) ===
DB_FILE = Path(__file__).with_name("barberbot_db.json")
print("[DEBUG] Using DB at:", DB_FILE.resolve())

def _fresh_db():
    return {
        "shops": {
            "1": {"name": "Pozuelo Barbershop"},
            "2": {"name": "La Moraleja Barbershop"},
        },
        "barbers": {
            "ivan@gmail.com":   {"barber_id": 1, "shop_id": 1, "name": "Ivan",   "password": "ivan123"},
            "david@gmail.com":  {"barber_id": 2, "shop_id": 1, "name": "David",  "password": "david123"},
            "laura@gmail.com":  {"barber_id": 3, "shop_id": 1, "name": "Laura",  "password": "laura123"},
            "pedro@gmail.com":  {"barber_id": 4, "shop_id": 2, "name": "Pedro",  "password": "pedro123"},
            "marta@gmail.com":  {"barber_id": 5, "shop_id": 2, "name": "Marta",  "password": "marta123"},
        },
        "services": {
            "1": {"name": "Haircut",              "price": 15, "duration": 30},
            "2": {"name": "Haircut + Beard",      "price": 25, "duration": 45},
            "3": {"name": "Beard Trim",           "price": 10, "duration": 15},
            "4": {"name": "Haircut + Eyebrows",   "price": 18, "duration": 40},
        },
        "clients": {},
        "appointments": [],
    }

def _load_db():
    if not DB_FILE.exists():
        print("[DEBUG] DB not found, creating fresh one...")
        db = _fresh_db()
        _save_db(db)
        return db
    with DB_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

def _save_db(db):
    # por si la carpeta no existe (útil si usas data/)
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DB_FILE.open("w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)
    print("[DEBUG] DB saved.")


DB = _load_db()


def _today_str():
   return _date.today().isoformat()


def _find_barber(barber_email):
   return DB["barbers"].get(barber_email)


def _get_shop_name(shop_id):
   shop = DB["shops"].get(str(shop_id))
   return shop["name"] if shop else "Unknown shop"


def _list_services():
   result = []
   for sid, svc in DB["services"].items():
       result.append(f"{sid}. {svc['name']} - {svc['price']}€ ({svc['duration']} min)")
   return "\n".join(result)


def _list_appointments_for_barber(barber_id):
   appts = [a for a in DB["appointments"] if a["barber_id"] == barber_id]
   if not appts:
       return "You have no appointments."
   appts = sorted(appts, key=lambda x: (x["date"], x["time"]))
   lines = []
   for a in appts:
       client = DB["clients"].get(a["client_phone"], {"name": "Unknown"})
       service = DB["services"].get(str(a["service_id"]), {"name": "Unknown"})
       lines.append(
           f"{a['date']} at {a['time']} - {client['name']} ({a['client_phone']}), {service['name']}"
       )
   return "\n".join(lines)


def _list_appointments_for_client(phone):
   appts = [a for a in DB["appointments"] if a["client_phone"] == phone]
   if not appts:
       return "You have no appointments booked."
   appts = sorted(appts, key=lambda x: (x["date"], x["time"]))
   lines = []
   for a in appts:
       barber = next((b for b in DB["barbers"].values() if b["barber_id"] == a["barber_id"]), None)
       service = DB["services"].get(str(a["service_id"]), {"name": "Unknown"})
       barber_name = barber["name"] if barber else "Unknown barber"
       lines.append(
           f"{a['date']} at {a['time']} with {barber_name} - {service['name']}"
       )
   return "\n".join(lines)


def _make_appointment(phone, service_id, barber_id, date_str, time_str):
   DB["appointments"].append({
       "client_phone": phone,
       "service_id": service_id,
       "barber_id": barber_id,
       "date": date_str,
       "time": time_str,
   })
   _save_db(DB)
   return "Your appointment has been booked."


def _cancel_appointment(phone, date_str, time_str):
   before = len(DB["appointments"])
   DB["appointments"] = [
       a for a in DB["appointments"]
       if not (a["client_phone"] == phone and a["date"] == date_str and a["time"] == time_str)
   ]
   after = len(DB["appointments"])
   if after < before:
       _save_db(DB)
       return "Your appointment was cancelled."
   else:
       return "No matching appointment found."



STATE = {
   "mode": None,   # "client" or "barber"
   "barber_email": None,
   "client_phone": None,
   "pending": None,  # for multi-step operations
}


def reset_state():
   STATE["mode"] = None
   STATE["barber_email"] = None
   STATE["client_phone"] = None
   STATE["pending"] = None



def handle(db, message):
   text = message.strip()

   if text.upper() == "SWITCH":
       reset_state()
       return "Mode reset. Are you a client or barber? (Type 'client' or 'barber')"

   if STATE["mode"] is None:
       if text.lower() in ["client", "1"]:
           STATE["mode"] = "client"
           return "Great! Please enter your phone number to continue."
       elif text.lower() in ["barber", "2"]:
           STATE["mode"] = "barber"
           return "Please enter your barber email to log in."
       else:
           return "Welcome to BarberBuddy! Are you a client or a barber? (Type 'client' or 'barber')"

   if STATE["mode"] == "barber":
       return _handle_barber(text)

   if STATE["mode"] == "client":
       return _handle_client(text)

   return "I didn't understand. Type 'switch' to restart."


def _handle_barber(text):
   if STATE["barber_email"] is None:
       email = text.strip()
       barber = _find_barber(email)
       if not barber:
           return "I couldn't find a barber with that email. Try again or type SWITCH."
       STATE["barber_email"] = email
       return (
           f"Hello {barber['name']} at {_get_shop_name(barber['shop_id'])}!\n"
           "Options:\n"
           "- Type 'appointments' to see your appointments.\n"
           "- Type 'today' to see today's appointments.\n"
           "- Type 'switch' to change mode."
       )

   lower = text.lower()
   barber = _find_barber(STATE["barber_email"])
   if not barber:
       reset_state()
       return "Your barber session was lost. Type 'barber' to log in again."

   if lower == "appointments":
       return _list_appointments_for_barber(barber["barber_id"])

   if lower == "today":
       today = _today_str()
       appts = [
           a for a in DB["appointments"]
           if a["barber_id"] == barber["barber_id"] and a["date"] == today
       ]
       if not appts:
           return "You have no appointments today."
       lines = []
       for a in appts:
           client = DB["clients"].get(a["client_phone"], {"name": "Unknown"})
           service = DB["services"].get(str(a["service_id"]), {"name": "Unknown"})
           lines.append(
               f"{a['time']} - {client['name']} ({a['client_phone']}), {service['name']}"
           )
       return "\n".join(lines)

   return "Barber mode commands: 'appointments', 'today', or 'switch'."


def _handle_client(text):
   if STATE["client_phone"] is None:
       phone = text.strip()
       if phone not in DB["clients"]:
           DB["clients"][phone] = {"name": f"Client {phone}", "created": _today_str()}
           _save_db(DB)
       STATE["client_phone"] = phone
       return (
           "Welcome! You can:\n"
           "- Type 'book' to book an appointment.\n"
           "- Type 'my appointments' to see your appointments.\n"
           "- Type 'cancel' to cancel an appointment.\n"
           "- Type 'switch' to change mode."
       )

   lower = text.lower()

   if STATE["pending"]:
       p = STATE["pending"]
       if p["action"] == "book_service":
           if text not in DB["services"]:
               return "Invalid service ID. Please enter a valid service ID."
           p["service_id"] = int(text)
           STATE["pending"] = {"action": "book_date", "service_id": p["service_id"]}
           return "Please enter the date for the appointment (YYYY-MM-DD)."

       if p["action"] == "book_date":
           STATE["pending"] = {"action": "book_time", "service_id": p["service_id"], "date": text}
           return "Please enter the time for the appointment (HH:MM)."

       if p["action"] == "book_time":
           msg = _make_appointment(
               STATE["client_phone"],
               p["service_id"],
               barber_id=1,
               date_str=p["date"],
               time_str=text,
           )
           STATE["pending"] = None
           return msg

       if p["action"] == "cancel_date":
           STATE["pending"] = {"action": "cancel_time", "date": text}
           return "Please enter the time (HH:MM) of the appointment to cancel."

       if p["action"] == "cancel_time":
           msg = _cancel_appointment(
               STATE["client_phone"], STATE["pending"]["date"], text
           )
           STATE["pending"] = None
           return msg

   if lower == "book":
       STATE["pending"] = {"action": "book_service"}
       return "Which service do you want?\n" + _list_services()

   if lower == "my appointments":
       return _list_appointments_for_client(STATE["client_phone"])

   if lower == "cancel":
       STATE["pending"] = {"action": "cancel_date"}
       return "Please enter the date (YYYY-MM-DD) of the appointment to cancel."

   return (
       "Client mode commands:\n"
       "- 'book'\n"
       "- 'my appointments'\n"
       "- 'cancel'\n"
       "- 'switch'"
   )


