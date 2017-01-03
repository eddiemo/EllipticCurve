import point
import shara
def add(self, other, aa):
    if self.inf:
        return other
    elif other.inf:
        return self
    elif (self.x == other.x and ((self.y == 0 and other.y == 0) or self.y != other.y)):
        return point.Point(0, 0, self.p, True)
    elif (self.x == other.x and self.y == other.y):
        lt = (((3 * (self.x * self.x) % self.p) % self.p) + aa) % self.p
        lb = (2 * self.y) % self.p

        if lb == 1:
            lt = lt % self.p
            l = lt
        elif lb == 0:
            return point.Point(0, 0, self.p, True)
        else:
            l = (lt * shara.inverse(lb, self.p)) % self.p

        a = (pow(l, 2, self.p) - ((2 * self.x) % self.p)) % self.p
        b = (((l * (self.x - a) % self.p) % self.p) - self.y) % self.p

        return point.Point(a, b, self.p, False)

    else:
        lt = (other.y - self.y) % self.p
        lb = (other.x - self.x) % self.p

        if lb == 1:
            lt = lt % self.p
            l = lt
        elif lb == 0:
            return point.Point(0, 0, self.p, True)
        else:
            l = (lt * shara.inverse(lb, self.p)) % self.p

        a = (((pow(l, 2, self.p) - other.x) % self.p) - self.x) % self.p
        b = (((l * ((self.x - a) % self.p)) % self.p) - self.y) % self.p

        return point.Point(a, b, self.p, False)

p = 11
a = point.Point(3, 5, p, False)
b = point.Point(7, 10, p, False)
c = add(a, b, 3)
print(c.x, c.y, c.inf)