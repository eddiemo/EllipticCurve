from shara import *

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

            if lb == 1:
                lt = lt % self.p
                l = lt
            elif lb == 0:
                return Point(0, 0, self.p, True)
            else:
                l = (lt * inverse(lb, self.p)) % self.p

            a = (pow(l, 2, self.p) - ((2 * self.x) % self.p)) % self.p
            b = (((l * (self.x - a) % self.p) % self.p) - self.y) % self.p

            return Point(a, b, self.p, False)

        else:
            lt = (other.y - self.y) % self.p
            lb = (other.x - self.x) % self.p

            if lb == 1:
                lt = lt % self.p
                l = lt
            elif lb == 0:
                return Point(0, 0, self.p, True)
            else:
                l = (lt * inverse(lb, self.p)) % self.p

            a = (((pow(l, 2, self.p) - other.x) % self.p) - self.x) % self.p
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