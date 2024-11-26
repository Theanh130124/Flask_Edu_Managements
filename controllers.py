import  hashlib




def hash_password(password):
    return str(hashlib.md5(password.encode('utf-8')).hexdigest())