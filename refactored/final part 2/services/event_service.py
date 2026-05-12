#handles reservations

from pathlib import Path
from data.data_manager import (load_data, save_data)

events_file = Path("event copy.json")

def reserve_ticket(event_id, user):
    events = load_data(events_file)
