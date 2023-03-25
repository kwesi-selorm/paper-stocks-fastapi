from passlib.hash import pbkdf2_sha256

# password_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")
# password_context.update(
#     sha256_crypt__default_rounds=10000,
#     sha256_crypt__default_salt_size=16,
# )
custom_algo = pbkdf2_sha256.using(rounds=10000)


def hash_password(password: str):
    return custom_algo.hash(password)
    # return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    print(hashed_password)
    return custom_algo.verify(plain_password, hashed_password)
    # return password_context.verify(plain_password, hashed_password)
