import math
from matrix22 import Matrix22


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def subtract(self, o):
        return Point(self.x - o.x, self.y - o.y)

    def add(self, o):
        return Point(self.x + o.x, self.y + o.y)

    def get_wxtx(self, w):
        return Matrix22(  # TODO: Define the matrix22
            self.x * self.x * w, self.x * self.y * w,
            self.y * self.x * w, self.y * self.y * w
        )

    def get_dot_p(self, o):
        return self.x * o.x + self.y * o.y

    # TODO: Raname
    def multiply(self, o):
        return Point(self.x * o.m11 + self.y * o.m21, self.x * o.m12 + self.y * o.m22)

    def multiply_d(self, o):
        return Point(self.x * o, self.y * o)

    def get_infinity_norm_distance(self, o):
        return max(abs(self.x - o.x), abs(self.y - o.y))


def get_weigted_average(p, w):
    sx = 0
    sy = 0
    sw = 0
    for i in range(len(p)):
        sx += p[i].x * w[i]
        sy += p[i].y * w[i]
        sw += w[i]

    return Point(sx / sw, sy / sw)