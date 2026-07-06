from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")



def get_hash_password(password :str):
    return pwd_context.hash(password)

#验证密码verify返回值布尔
def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)