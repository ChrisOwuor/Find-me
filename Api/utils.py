import random
import hashlib


def generate_track_code(birthdate):
    # Prefix: Concatenate user-related information
    prefix = str(birthdate)[:2]

    # Random Number Component: Generate a random number
    random_number = str(random.randint(100000, 999999))

    # Combine components
    track_code = prefix + random_number

    # Checksum: Use hashlib to create a checksum
    checksum = hashlib.sha256(track_code.encode()).hexdigest()[:3]

    # Finalize the account number
    final_track_code = track_code + checksum

    return final_track_code
