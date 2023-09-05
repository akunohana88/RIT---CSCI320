import hashlib


def encode(hashstr):
    hashed = hashlib.sha256(str(hashstr).encode('utf-8')).hexdigest()
    return hashed
