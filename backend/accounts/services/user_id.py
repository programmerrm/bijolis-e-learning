import random

def GENERATE_USER_ID(role: str) -> str:
    role_prefixes = {
        'admin': 'A',
        'user': 'U',
    }

    prefix = role_prefixes.get(role.lower())
    if not prefix:
        raise ValueError("Invalid role provided. Must be 'admin' or 'user'.")

    random_number = random.randint(1000000, 9999999)
    return f"{prefix}-{random_number}"
