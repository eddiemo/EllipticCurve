import shara
import point
import random

print("Генерация p, q, n, phin...")
nn = int(input("Введите количество бит в числе p: "))
p = shara.gen_p(nn)
while p % 6 != 5:
    p = shara.gen_p(nn)#;print(p)
nn = int(input("Введите количество бит в числе q: "))
q = shara.gen_p(nn)
while q % 6 != 5:
    q = shara.gen_p(nn)#;print(q)
n = p * q#; print(n)
phin = (p + 1) * (q + 1)#;print(phin)
x = random.randint(1, n)
y = random.randint(1, n)
P = point.Point(x, y, n)
k = int(input("Количество генирируемых чисел: "))
b = int(input("Количество бит с одной точки: "))
x = []
for i in range(k):
    P = P + P
    x.append(int(str(bin(P.x))[-b:], 2))
print(str(x)[1:-1])