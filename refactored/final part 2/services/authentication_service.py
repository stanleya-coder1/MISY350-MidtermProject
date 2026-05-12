#for users
import uuid
from data.data_manager import (load_data, save_data, users_file)


def login(email, password):
    users = load_data(users_file)
    for user in users:
        if (user["email"].lower() == email.lower() and user["password"] == password):
            return user
    return None

def register_user(email, full_name, password, role):
    users = load_data(users_file)
    # duplicate email check
    for user in users:
        if user["email"].lower() == email.lower():
            return "duplicate"

    new_user = {
        "id": str(uuid.uuid4()),
        "email": email,
        "full_name": full_name,
        "password": password,
        "role": role
    }
    users.append(new_user)

    save_data(users_file, users)
    return "success"