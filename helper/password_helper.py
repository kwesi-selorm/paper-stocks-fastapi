from passlib.hash import pbkdf2_sha256

custom_algo = pbkdf2_sha256.using(rounds=10000)


def hash_password(password: str):
    return custom_algo.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return custom_algo.verify(plain_password, hashed_password)
