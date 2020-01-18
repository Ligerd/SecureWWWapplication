import string
from Crypto.Protocol.KDF import PBKDF2
import math
from Crypto.Random import get_random_bytes

def encrypt(password):
    entropija = len(password) * (math.log(len(string.ascii_lowercase), 2))
    print(entropija)
    if entropija < 30:
        print("hasło jest za słabe. Entropija wynosi:", entropija)
    iv = get_random_bytes(16)
    out=PBKDF2(password, iv)
    out=iv +out
    return out.decode("iso8859-1")

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

def password_verification(chipterTEXT,password):
    chipterTEXT = chipterTEXT.encode('iso8859-1')
    iv = chipterTEXT[:16]
    out = PBKDF2(password, iv)
    out = iv + out
    return out==chipterTEXT

def fild_verification(textFild):
    allowed_characters=list(string.digits)+list(string.ascii_letters)
    letters=list(textFild)
    for letter in letters:
        if letter not in allowed_characters:
            return letter
    return True

