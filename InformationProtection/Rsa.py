import math
import random


def find_e(euler: int, n: int):
    gcd = []
    for i in range(1, n):
        if math.gcd(i, euler) == 1:
            gcd.append(i)

    #print(gcd)
    e = random.choice(gcd)
    print(f"e = {e}")
    return e


def rsa_sipher(p: int, q: int):
    n = p*q
    euler = (p-1) * (q-1)
    e = find_e(euler, n)
    #e = 5

    numerator = 1
    k = 1
    while numerator % e != 0:
        numerator = k * euler + 1
        k += 1

    d = numerator / e

    open_key = (d, n)

    alphabet = get_koefs()
    #print(alphabet)
    with open("../../InformationProtection/TestText", "r", encoding="utf-8") as f:
        text = list(f.read())
    print(text)
    with open("cyphered", "w") as f:
        for sym in text:
            C = ( int(alphabet[sym]) ** e) % n
            f.write(str(C) + " ")

    return d, n


def rsa_desypher(d: int, n: int):
    alphabet = get_koefs()
    alphabet = {v: k for k, v in alphabet.items()}

    with open("cyphered", "r", encoding="utf-8") as f:
        text = f.read().split()
    print(text)
    print(alphabet)
    with open("de_cyphered.txt", "w", encoding="utf-8") as f:
        for sym in text:
            T = (int(sym) ** d) % n
            f.write(alphabet[str(T)])


def get_koefs():
    alpahbet = {}
    with open("rsa_koefs.txt", "r") as f:
        for i in range(44):
            if i == 33:
                alpahbet[" "] = '34'
            else:
                tmp = f.readline().split()
                alpahbet[tmp[0]] = tmp[1]

    return alpahbet


def print_koefs():
    a = ord('а')
    alphabet = ''.join([chr(i) for i in range(a - 1, a+6)] + [chr(a+33)] + [chr(i) for i in range(a+6, a+32)])
    with open("rsa_koefs.txt", "w") as file:
        for i in range(1, 34):
            file.write(f"{alphabet[i]} {i} \n")


if __name__ == '__main__':
    d, n = rsa_sipher(7, 13)
    rsa_desypher(int(d), n)

