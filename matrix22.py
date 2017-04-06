class Matrix22:
    def __init__(self, n11, n12, n21, n22):
        self.m11 = n11
        self.m12 = n12
        self.m21 = n21
        self.m22 = n22

    def adjugate(self):
        return Matrix22(self.m22, -self.m12, -self.m21, self.m11)

    def determinant(self):
        return self.m11 * self.m22 - self.m12 * self.m21

    def multiply(self, m):
        self.m11 *= m
        self.m12 *= m
        self.m21 *= m
        self.m22 *= m
        return self

    def add_matrix(self, added_matrix):
        self.m11 += added_matrix.m11
        self.m12 += added_matrix.m12
        self.m21 += added_matrix.m21
        self.m22 += added_matrix.m22

    def inverse(self):
        return self.adjugate().multiply(1.0 / self.determinant())
