from werkzeug.security import check_password_hash, generate_password_hash

def hash_password(password):
    return generate_password_hash(password)

def check_password(hash, password):
    return check_password_hash(hash, password)