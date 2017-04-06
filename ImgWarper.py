import cv2
import datetime
import numpy as np
from Point import *
from matrix22 import Matrix22
from bilinear_interpolation import BilinearInterpolation


class ImgWarper:
    def __init__(self, img, opt_grid_size=0, opt_alpha=0):
        self.img = img
        self.alpha = opt_alpha or 1
        self.gridSize = opt_grid_size or 20

        self.height, self.width, channels = img.shape
        self.bilinearInterpolation = BilinearInterpolation(self.img, self.width, self.height)

        self.grid = []
        for i in xrange(0, self.width, self.gridSize):
            for j in xrange(0, self.height, self.gridSize):
                a = Point(i, j)
                b = Point(i+self.gridSize, j)
                c = Point(i+self.gridSize, j+self.gridSize)
                d = Point(i, j+self.gridSize)
                self.grid.append([a, b, c, d])

    def show_img(self, img):
        cv2.imshow('image', self.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def warp(self, from_points, to_points):
        t0 = datetime.datetime.now()
        deformation = AffineDeformation(from_points, to_points, self.alpha)
        transformed_grid = []
        for i in range(len(self.grid)):
            transformed_grid.append([
                deformation.move_point(self.grid[i][0]),
                deformation.move_point(self.grid[i][1]),
                deformation.move_point(self.grid[i][2]),
                deformation.move_point(self.grid[i][3])
            ])

        t1 = datetime.datetime.now()
        new_img = self.bilinearInterpolation.generate(self.grid, transformed_grid)

        t2 = datetime.datetime.now()
        print 'Deform: ' + str(t1 - t0) + 'ms; interpolation: ' + str(t2 - t1) + 'ms'
        return new_img


class AffineDeformation:
    def __init__(self, from_points, to_points, alpha):
        self.w = None
        self.pRelative = None
        self.qRelative = None
        self.A = None
        if len(from_points) is not len(to_points):
            print 'Points are not same length'
            return

        self.n = len(from_points)
        self.from_points = from_points
        self.to_points = to_points
        self.alpha = alpha

    def move_point(self, point):
        if self.pRelative is None or len(self.pRelative) < self.n:
            self.pRelative = [0]*self.n

        if self.qRelative is None or len(self.qRelative) < self.n:
            self.qRelative = [0] * self.n

        if self.w is None or len(self.w) < self.n:
            self.w = [0] * self.n

        if self.A is None or len(self.A) < self.n:
            self.A = [0] * self.n

        for i in range(self.n):
            t = self.from_points[i].subtract(point)
            self.w[i] = math.pow(t.x * t.x + t.y*t.y, -self.alpha)

        p_average = get_weigted_average(self.from_points, self.w)
        q_average = get_weigted_average(self.to_points, self.w)

        for i in range(self.n):
            self.pRelative[i] = self.from_points[i].subtract(p_average)
            self.qRelative[i] = self.to_points[i].subtract(q_average)

        mat = Matrix22(0, 0, 0, 0)
        for i in range(self.n):
            mat.add_matrix(self.pRelative[i].get_wxtx(self.w[i]))
        mat = mat.inverse()

        for i in range(self.n):
            self.A[i] = point.subtract(p_average).multiply(mat).get_dot_p(self.pRelative[i]) * self.w[i]

        r = q_average
        for i in range(self.n):
            r = r.add(self.qRelative[i].multiply_d(self.A[i]))

        return r
