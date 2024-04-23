import cv2
import numpy as np


def get_pixel_coor(circles):
    pxl = np.zeros((len(circles[0]),2))
    x = circles[0, :, 0]
    y = circles[0, :, 1]
    for i in range(len(circles[0])):
        pxl[i] = [x[i], y[i]]
    return pxl

def get_nine_coor(x0, y0):
    STC_points_robot = np.zeros((9,2))
    STC_points_robot[0] = np.array([x0, y0])
    STC_points_robot[1] = np.array([x0, y0 + 81])
    STC_points_robot[2] = np.array([x0, y0 + 162])

    STC_points_robot[3] = np.array([x0 + 81, y0])
    STC_points_robot[4] = np.array([x0 + 81, y0 + 81])
    STC_points_robot[5] = np.array([x0 + 81, y0 + 162])

    STC_points_robot[6] = np.array([x0 + 162, y0])
    STC_points_robot[7] = np.array([x0 + 162, y0 + 81])
    STC_points_robot[8] = np.array([x0 + 162, y0 + 162])
    return STC_points_robot


def sort_array(arr):
    sorted_arr = arr[np.argsort(arr[:, 1])]
    sorted_result = np.empty_like(sorted_arr)

    for i in range(0, len(arr), 3):

        batch = sorted_arr[i:i+3]

        sorted_batch = batch[np.argsort(batch[:, 0])]
        sorted_result[i:i+3] = sorted_batch
    return sorted_result

def bwExtend(a, b):
    c = []
    c.extend(a)
    c.extend(b)
    return len(a), c

class HandInEyeCalibration:

    def get_m(self, STC_points_camera, x0, y0):
        STC_points_robot = get_nine_coor(x0, y0)
        m, _ = cv2.estimateAffine2D(STC_points_camera, STC_points_robot)
        return m

    def get_points_robot(self, STC_points_camera, x0, y0, x_camera, y_camera):
        m = self.get_m(STC_points_camera, x0, y0)
        robot_x = (m[0][0] * x_camera) + (m[0][1] * y_camera) + m[0][2]
        robot_y = (m[1][0] * x_camera) + (m[1][1] * y_camera) + m[1][2]
        return np.array([robot_x, robot_y])

if __name__ == '__main__':
    
    circles = np.array([[[ 944,  424,   25],
        [ 948,  608,   24],
        [1132,  422,   24],
        [ 744,  232,   27],
        [ 764,  612,   24],
        [1132,  228,   26],
        [1132,  604,   23],
        [ 756,  426,   24],
        [ 938,  232,   25]]])

    x0, y0 = 227.9508, -173.1939

    STC_points_robot = get_nine_coor(x0, y0)

    STC_points_camera = sort_array(get_pixel_coor(circles))
    
    a = HandInEyeCalibration()
    m = a.get_m(STC_points_camera, x0, y0)
    x, y = a.get_points_robot(STC_points_camera, x0, y0, 746, 232)
    print(x, y)