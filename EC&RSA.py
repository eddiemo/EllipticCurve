import random
import shara
from point import *

def gen_keys():
    p = shara.gen_p(100)
    while p % 6 != 5:
        p = shara.gen_p(100)
    #print(p)
    q = shara.gen_p(100)
    while q % 6 != 5:
        q = shara.gen_p(100)
    #print(q)
    n = p * q#; print(n)
    phin = (p + 1) * (q + 1)
    e = random.randint(2, n)
    while True:
        if shara.ex_gcd(e, phin) == 1:
            break
        else:
            e = (e + 1) % n
            if e < 2:
                e = 2
    d = shara.inverse(e, phin)
    #print(str(e) + str(d))
    open('pubkey', 'tw', encoding='utf-8').close()
    f = open('pubkey', 'w')
    f.write(str(n) + ' ' + str(e)); f.close()
    open('privkey', 'tw', encoding='utf-8').close()
    f = open('privkey', 'w')
    f.write(str(n) + ' ' + str(d)); f.close()

def get_blocks(mes, n):
    res = []
    s = ''
    for i in range(0, len(mes)):
        if mes[i] // 100 > 0:
            s += str(mes[i])
        elif mes[i] // 10 > 0:
            s += '0' + str(mes[i])
        else:
            s += '00' + str(mes[i])

    if len(str(n)) % 3 == 0:
        blcklen = len(str(n)) - 3
    else:
        blcklen = len(str(n)) // 3 * 3
    for i in range(0, len(s), blcklen):
        j = blcklen
        if i + blcklen >= len(s):
            j = len(s) - i
        res.append(int(s[i:i+j]))
    return res

def get_bytes(crypt_points):
    mes = ''
    for i in range(len(crypt_points)):
        if len(str(crypt_points[i].x)) % 3 == 0:
            mes += str(crypt_points[i].x)
        elif len(str(crypt_points[i].x)) % 3 == 1:
            mes += "00" + str(crypt_points[i].x)
        else:
            mes += "0" + str(crypt_points[i].x)
    #print(mes)
    res = []
    j = 0
    for i in range(len(mes) // 3):
        res.append(int(mes[j:j+3]))
        j += 3
    return res

def encrypt():
    print("Выберите файл с сообщением")
    path = shara.open_file()
    f = open(path, 'rb')
    message = f.read(); f.close()
    print("Выберите файл с открытым ключом")
    path2 = shara.open_file()
    f = open(path2, 'r')
    keysplt = (f.read()).split(); f.close()
    n = int(keysplt[0])
    e = int(keysplt[1])
    open(path + '.enc', 'tw', encoding='utf-8').close()
    f = open(path + '.enc', 'w')
    blocks = get_blocks(message, n)#; print(str(blocks))
    for m in blocks:
        y = random.randint(1, n)
        Q = Point(m, y, n)
        C = Q * e
        f.write(str(C.x) + ' ' + str(C.y) + '\n')

def decrypt():
    print("Выберите файл с зашифрованным сообщением")
    path = shara.open_file()
    print("Выберите файл с закрытым ключом")
    path2 = shara.open_file()
    f = open(path2, 'r')
    keysplt = (f.read()).split(); f.close()
    n = int(keysplt[0])
    d = int(keysplt[1])
    decrypt_mes = []
    with open(path, 'r')as f:
        for line in f:
            pointsplt = line.split()
            C = Point(int(pointsplt[0]), int(pointsplt[1]), n)
            Q = C * d
            decrypt_mes.append(Q)
    message = get_bytes(decrypt_mes)#; print(str(message))
    open(path + '.dec', 'tw').close()
    f = open(path + '.dec', 'w')
    f.write(bytearray(message).decode('windows-1251')); f.close()

if __name__ == '__main__':
    mode = input("Введите режим:\n1 - генерация ключей\n2 - шифрование\n3 - дешифрование\n4 - выход ")
    while True:
        if mode == "1":
            gen_keys()
        elif mode == "2":
            encrypt()
        elif mode == "3":
            decrypt()
        elif mode == "4":
            exit(0)
        else:
            print("Не тот режим")
        mode = input("Выберите режим снова: ")