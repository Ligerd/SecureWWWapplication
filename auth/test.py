import string

from Crypto.Protocol.KDF import PBKDF2
from typing import Iterable
from Crypto.Random import get_random_bytes
from Crypto.Cipher import DES,AES
import math

def codesToStr(codes: Iterable[int]) -> str:
    return ''.join((chr(c) for c in codes))
iv = "JUST ASECRETSALT"
def password_encryption(password):
    entropija = len(password) * (math.log(len(string.ascii_lowercase), 2))
    print(entropija)
    if entropija < 30:
        print("hasło jest za słabe. Entropija wynosi:", entropija)
    key = PBKDF2(password, b"salt")
    password=str.encode(password)
    reszta = len(password) % 16
    if reszta != 0:
        f = 16 - reszta
        password = password + (f * str.encode('0'))
    aes = AES.new(key, AES.MODE_CBC, iv)
    chipter = aes.encrypt(password)
    return chipter.decode('iso8859-1')

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

def check_password(chipterDB,password):
    key = PBKDF2(password, b"salt")
    password = str.encode(password)
    reszta = len(password) % 16
    if reszta != 0:
        f = 16 - reszta
        password = password + (f * str.encode('0'))
    aes=AES.new(key,AES.MODE_CBC,iv)
    chipter=aes.encrypt(password)
    return chipter.decode('iso8859-1')==chipterDB

encrypt=password_encryption("test")
print(check_password(encrypt,"test"))


