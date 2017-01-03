import math
import random

class Point(object):
    def __init__(self, x = None, y = None, p = None, inf = None):
        self.x = x
        self.y = y
        self.p = p
        self.inf = inf

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y and self.p == other.p:
            return True
        else:
            return False

    def __neg__(self):
        return Point(self.x, -self.y, self.p, self.inf)

    def __add__(self, other):
        if self.inf:
            return other
        elif other.inf:
            return self
        elif (self.x == other.x and ((self.y == 0 and other.y == 0) or self.y != other.y)):
            return Point(0, 0, self.p, True)
        elif (self.x == other.x and self.y == other.y):
            lt = (3 * (self.x * self.x) % self.p) % self.p
            lb = (2 * self.y) % self.p

            if lb < 0:
                lt = -lt
                lb = -lb
            if lb == 1:
                lt = lt % self.p
                l = lt
            elif lb == 0:
                return Point(0, 0, self.p, True)
            else:
                l = (lt * inverse(lb, self.p)) % self.p

            a = (pow(l, 2, p) - ((2 * self.x) % self.p)) % self.p
            b = (((l * (self.x - a) % self.p) % self.p) - self.y) % self.p

            return Point(a, b, self.p, False)

        else:
            lt = (other.y - self.y) % self.p
            lb = (other.x - self.x) % self.p

            if lb < 0:
                lt = -lt
                lb = -lb
            if lb == 1:
                lt = lt % self.p
                l = lt
            elif lb == 0:
                return Point(0, 0, self.p, True)
            else:
                l = (lt * inverse(lb, self.p)) % self.p

            a = (((pow(l, 2, p) - other.x) % self.p) - self.x) % self.p
            b = (((l * (self.x - a) % self.p) % self.p) - self.y) % self.p

            return Point(a, b, self.p, False)

    def __mul__(self, k):
        if k == 1:
            return self
        other = self
        n = 2
        i = 1
        while n <= k:
            n *= 2
            i += 1
        if i > 1:
            i -= 1
            n //= 2
        for j in range(0, i):
            other = other + other
        n1 = 0
        if n < k:
            n1 = k - n
            other = other + (self * n1)
        return other

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

def L(a, p):
    p12 = (p - 1) // 2
    if a < 0:
        return (((-1) ** p12) * pow(-a, p12, p)) % p
    elif a == 1:
        return 1
    elif a >= 0:
        l = pow(a, p12, p)
        if l == 1:
            return l
        elif l == p - 1:
            return -1
    return 0

def sqrtp(D, p):
    fail = False
    p1 = p - 1
    s = 0
    while p1 & 1 == 0:
        p1 >>= 1
        s += 1
    q = p1
    if s == 1:
        fail = False
        return pow(D, (p+1) // 4, p), fail

    z = 0
    while True:
        z = random.randint(1, p)
        if L(z, p) != -1:
            continue
        else:
            break
    c = pow(z, q, p)

    r = pow(D, (q+1) // 2, p)
    t = pow(D, q, p)
    m = s

    ix = 0
    while True:
        if ix > 100:
            fail = True
            return r, fail
        if t == 1:
            fail = False
            return r, fail
        k = 0
        for i in range(1, m):
            if pow(t, 2**i, p) == 1:
                k = i
                break
        b = pow(int(c), int(pow(2, (m - i - 1))), int(p))
        r = (r * b) % p
        t = (t * pow(b, 2, p)) % p
        m = i
        ix += 1

def factorization(p, D):
    ax = 0
    bx = 0
    symL = L(-D, p)
    if symL != 1:
        print ("babats na 2 shage")
        return

    fail = False
    ux, fail = sqrtp(-D, p)
    if fail:
        return ax, bx, fail
    assert((ux ** 2) % p == (-D) % p)

    i = 0
    u = []
    u.append(ux)
    m = []
    m.append(p)
    a = []
    b = []

    while True:
        m.append((u[i]**2 + D) // m[i])
        u.append(min(u[i] % m[i+1], m[i+1] - (u[i] % m[i+1])))

        if m[i+1] == 1:
            break
        else:
            a.append(0)
            b.append(0)
            i += 1

    a.append(u[i])
    b.append(1)

    while True:
        if i == 0:
            ax = a[i]
            bx = b[i]
            break
        else:
            ch = (u[i-1] * a[i]) + (D * b[i])
            zn = (a[i] * a[i]) + (D * (b[i] * b[i]))
            if ch % zn == 0:
                a[i-1] = ch // zn
            else:
                ch = (-u[i - 1] * a[i]) + (D * b[i])
                a[i-1] = ch // zn
            ch = (u[i - 1] * b[i]) - a[i]
            zn = (a[i] * a[i]) + (D * (b[i] * b[i]))
            if ch % zn == 0:
                b[i - 1] = ch // zn
            else:
                ch = (-u[i - 1] * b[i]) - a[i]
                b[i - 1] = ch // zn

            i -= 1

    return ax, bx, fail

def to_bin(n):
    r = []
    while n > 0:
        r.append(n & 1)
        n >>= 1
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

def cube_residue(a, p):
    if p % 3 == 2:
        return 1
    elif p % 3 == 1:
        if pow(a, (p - 1) // 3, p) == 1:
            return 1
    return -1

def steps(l):
    while True:

        # 1 step: generation p

        p = random.randint(0, 2 ** (l1))
        p += 2 ** (l1)
        while True:
            while p % 6 != 1:
                p += 1
            if not is_prime(p, l):
                p += 6
                continue
            else:
                break

        # 2 step: factorization p

        D = 3
        cx, dx, fail = factorization(p, D)
        if fail:
            continue
        assert (cx * cx + 3 * dx * dx == p)

        # 3 step: check N

        flag = False
        T = [cx + 3 * dx, cx - 3 * dx, 2 * cx, -(cx + 3 * dx), -(cx - 3 * dx), -2 * cx]
        for t in T:
            Nx = p + 1 + t
            NT = [Nx // x for x in [1, 2, 3, 6]]
            flag = False
            for elem in NT:
                if elem - int(elem) == 0:
                    if is_prime(elem, len(to_bin(elem))):
                        flag = True
                        r = elem
                        break
            if flag:
                N = Nx
                break
        if not flag:
            continue

        # 4 step: check p, r

        m = 10
        flag = False
        for i in range(1, m + 1):
            if p == r or pow(p, i, r) == 1:
                flag = True
                break
        if flag:
            continue
        else:
            return (N, p, r)


if __name__ == "__main__":

    l = int(input("Enter l: "))
    l1 = int(l - 1)

    N, p, r = steps(l)

    # 5 step: gen random P and find B

    x = random.randint(1, p - 1)
    y = random.randint(1, p - 1)
    P0 = Point(x, y, p, False)
    coef = N // r
    B = 0

    ix = 0
    while True:

        if ix > 50:
            ix = 0
            N, p ,r = steps(l)
            coef = N // r
        P0.x = random.randint(1, p - 1)
        P0.y = random.randint(1, p - 1)
        ix += 1
        B = (pow(P0.y, 2, p) - pow(P0.x, 3, p)) % p
        if coef == 1:
            if L(B, p) != -1 or cube_residue(B, p) != -1:
                continue
        elif coef == 6:
            if L(B, p) != 1 or cube_residue(B, p) != 1:
                continue
        elif coef == 2:
            if L(B, p) != -1 or cube_residue(B, p) != 1:
                continue
        elif coef == 3:
            if L(B, p) != 1 and cube_residue(B, p) != -1:
                continue

        # 6 step: N * (x, y) = P~
        pinf = P0 * N
        if pinf.inf == True:
            break

        continue

    # 7 step: Q = (N/r) * (x0, y0)

    Q = P0 * coef

    print()
    print("p = " + str(p))
    print("B = " + str(B))
    print("Q = " + "(" + str(Q.x) + ", " + str(Q.y) +")")
    print("r = " + str(r))

    if l <= 20:
        f = open("coordsX", "w")
        g = open("coordsY", "w")
        for i in range(1, r):
            QQ = Q * i
            f.write(str(QQ.x) + "\n")
            g.write(str(QQ.y) + "\n")
        g.close()
        f.close()

        exit(0)
    else:
        exit(0)