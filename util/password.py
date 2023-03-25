from passlib.context import CryptContext

password_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")


def hash_password(password: str):
    return password_context.hash(password)
