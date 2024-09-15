import os

import bcrypt  # For password hashing


def hash_password(password):
    """Hashes a password using bcrypt with a random salt and pepper."""
    # converting password to array of bytes
    bytes = password.encode('utf-8')

    # generating the salt
    salt = bcrypt.gensalt()

    # Hashing the password
    hash = bcrypt.hashpw(bytes, salt)
    return hash
def verify_password(hashed_password, plain_text_password):
    """Verifies a plain text password against a hashed password."""
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password.encode('utf-8'))