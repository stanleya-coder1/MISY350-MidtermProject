import uuid

from data.data_manager import (load_data, save_data, users_file)


def login(email, password):
    users = load_data(users_file)
    for user in users:
        if (user["email"].lower() == email.lower() and user["password"] == password):
            return user
    return None

