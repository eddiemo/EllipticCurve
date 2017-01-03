import random
import math
from tkinter.filedialog import *

def open_file():
    op = askopenfile()
    op = str(op)
    st = op.find('name=') + 6
    fin = op.find('mode') - 2
    path = op[st:fin]
    return path

def ex_gcd(a, b):
    reverse = False
    res = [0, 0, 0]
    if a < b:
        a, b = b, a
        reverse = True
    r, q, x0, y0, x1, y1, x, y = b, 0, 1, 0, 0, 1, 0, 0
    while a % b != 0:
        r, q, x, y, x0, y0 = a % b, a // b, x0 - q * x1, y0 - q * y1, x1, y1
        x1 = x
        y1 = y
        a = b
        b = r
    res[0] = r
    if reverse:
        res[1] = y
        res[2] = x
    else:
        res[1] = x
        res[2] = y
    return res[0]

def gcd(a, b):
    a = math.fabs(a)
    b = math.fabs(b)
    while b:
        a %= b
        a, b = b, a
    return a

def gcdex(a, b):
    a0, a1, b0, b1 = 1, 0, 0, 1
    while b != 0:
        q, r = divmod(a, b)
        a, b = b, r
        a0, a1, b0, b1 = b0, b1, a0 - q * b0, a1 - q * b1
    return a0

def inverse(z, p):
    return ((gcdex(z,p) % p + p) % p)

def to_bin(n):
    r = []
    while n > 0:
        r.append(n & 1)
        n //= 2
    return r

def test(a, n):
    b = to_bin(n - 1)
    k = 1
    for i in range(len(b) - 1, -1, -1):
        x = k
        k = (k * k) % n
        if k == 1 and x != 1 and x != n - 1:
            return True
        if b[i] == 1:
            k = (k * a) % n
    if k != 1:
        return True
    return False

def is_prime(n, bits):
    if n == 1:
        return False
    for j in range(0, bits):
        a = random.randint(2, n - 1)
        if test(a, n):
            return False
    return True

def gen_p(bits):
    while True:
        p = random.randint(2 ** (bits - 2), 2 ** (bits - 1))
        while p % 2 == 0:
            p = random.randint(2 ** (bits - 2), 2 ** (bits - 1))
        while not is_prime(p, bits):
            p = random.randint(2 ** (bits - 2), 2 ** (bits - 1))
            while p % 2 == 0:
                p = random.randint(2 ** (bits - 2), 2 ** (bits - 1))
        p = p * 2 + 1
        if is_prime(p, bits):
            return p

def gen_prime(start, fin):
    # int(input('Введите битность длинного простого числа: ')
    p = random.randint(start, fin)
    while not is_prime(p, len(to_bin(p))):
        p = random.randint(start, fin)
        while p % 2 == 0:
            p = random.randint(start, fin)
    return p