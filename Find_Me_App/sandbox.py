import string
import random


def gen_code():
    length = 10
    code = "LST"

    for i in range(length):
        rand_code = random.choice(string.ascii_uppercase)
        code = code + rand_code
    return code + str(254)