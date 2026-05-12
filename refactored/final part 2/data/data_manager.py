import json
from pathlib import Path


users_file = Path("users.json")
if users_file.exists():
   with open(users_file, "r") as f:
        users = json.load(f)
else:
    users = [
     {
    "id": "1",
    "email": "admin@event.edu",
    "full_name": "System Admin",
    "password": "123ssag@43AE",
    "role": "Admin"
    }]


events_file = Path("events.json")
if events_file.exists():
   with open(events_file, "r") as f:
        events = json.load(f)
else:
    events = [
  {
    "id": "1",
    "name": "Graduation",
    "date": "5-24-2026",
    "time": "10:00 AM",
    "location": "Newark",
    "description": "Graduation ceremony for the 2026 class.",
    "tickets": 500,
    "reserved": 120
  },
  {
    "id": "2",
    "name": "Music Festival",
    "date": "6-1-2026",
    "time": "8:00 PM",
    "location": "Philadelphia",
    "description": "Live music and entertainment.",
    "tickets": 100,
    "reserved": 50
  }]

def load_data(json_path: Path):
    if json_path.exists():
        with open(json_path, "r") as f:
            return json.load(f)
    return []


def save_data(json_path: Path, data: list):
    with open(json_path, "w") as f:
        json.dump(data, f, indent=4)
