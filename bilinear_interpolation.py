import cv2
import numpy as np
import math


class BilinearInterpolation:
    def __init__(self, img, width, height):
        self.width = width
        self.height = height
        self.new_image = np.zeros((height, width, 3), np.uint8)
        self.original_image = img

    def generate(self, from_grid, to_grid):
        for i in range(len(to_grid)):
            self.fill(to_grid[i], from_grid[i])

        return self.new_image

    def fill(self, source_points, filling_points):
        x0 = max(filling_points[0].x, 0)
        y0 = max(filling_points[0].y, 0)
        x1 = min(filling_points[2].x, self.width - 1)
        y1 = min(filling_points[2].y, self.height - 1)
        for i in range(x0, x1):
            xl = (i - x0) / float(x1 - x0)
            xr = 1 - xl
            top_x = xr * source_points[0].x + xl * source_points[1].x
            top_y = xr * source_points[0].y + xl * source_points[1].y
            bottom_x = xr * source_points[3].x + xl * source_points[2].x
            bottom_y = xr * source_points[3].y + xl * source_points[2].y
            for j in range(y0, y1):
                yl = (j - y0) / float(y1 - y0)
                yr = 1 - yl
                src_x = top_x * yr + bottom_x * yl
                src_y = top_y * yr + bottom_y * yl
                if src_x < 0 or src_x > self.width-1 or src_y < 0 or src_y > self.height-1:
                    self.new_image[j][i][0] = 255
                    self.new_image[j][i][1] = 255
                    self.new_image[j][i][2] = 255
                    continue

                src_x1 = int(math.floor(src_x))
                src_y1 = int(math.floor(src_y))
                self.new_image[j][i][0] = self.original_image[src_y1][src_x1][0]
                self.new_image[j][i][1] = self.original_image[src_y1][src_x1][1]
                self.new_image[j][i][2] = self.original_image[src_y1][src_x1][2]

