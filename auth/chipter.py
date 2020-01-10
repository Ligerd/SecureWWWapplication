import string
from Crypto import Random
from typing import Iterable
from Crypto.Cipher import DES,AES
import math

key="key4567890123456"

def codesToStr(codes: Iterable[int]) -> str:
    return ''.join((chr(c) for c in codes))

def encrypt(password):
    entropija = len(password) * (math.log(len(string.ascii_lowercase), 2))
    print(entropija)
    if entropija < 30:
        print("hasło jest za słabe. Entropija wynosi:", entropija)
    password=pad(password)
    iv = Random.new().read(AES.block_size)
    chipter = AES.new(key, AES.MODE_CBC, iv)
    out=iv + chipter.encrypt(password)
    return out.decode('iso8859-1')

def entropy(data: bytes)->float:
    count = [0] * 256
    dataSize = len(data)
    for b in data:
        count[b] = count[b] + 1
    entropy = 0
    for b in range(256):
        if count[b]/dataSize>0:
            entropy =entropy + (count[b] / dataSize) *math.log(count[b]/dataSize,2)
    return -entropy

def decrypt(chipterTEXT):
    chipterTEXT=chipterTEXT.encode('iso8859-1')
    iv=chipterTEXT[:AES.block_size]
    chipter=AES.new(key,AES.MODE_CBC,iv)
    text=chipter.decrypt(chipterTEXT[AES.block_size:])
    return text.rstrip(b"0").decode()


def login_verification(login):
    allowed_characters=list(string.digits)+list(string.ascii_letters)
    letters=list(login)
    for letter in letters:
        if letter not in allowed_characters:
            return letter
    return True

def password_verification(login):
    allowed_characters=list(string.digits)+list(string.ascii_letters)
    letters=list(login)
    for letter in letters:
        if letter not in allowed_characters:
            return letter
    return True

def pad(s):
    return s+"0"*(AES.block_size-len(s)%AES.block_size)