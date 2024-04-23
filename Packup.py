
import numpy as np
from Transformation import sort_array
from Transformation import get_pixel_coor
from Transformation import HandInEyeCalibration


def Packup(circles, STC_points_camera, x0, y0):

    circles = get_pixel_coor(circles)
    STC_points_camera = sort_array(get_pixel_coor(STC_points_camera))
    a = HandInEyeCalibration()
    m = a.get_m(STC_points_camera, x0, y0)

    m_circles = np.zeros((len(circles),2))
    for i in range(len(circles)):
        m_circles[i] = a.get_points_robot(STC_points_camera, x0, y0, circles[i, 0], circles[i, 1])


    Buf = np.zeros((len(circles),6))
    for i in range(len(m_circles)):
        Buf[i] = np.append(m_circles[i], np.array([75.010 ,-180, 0, 0]))
    m_circles = Buf
    return m_circles

if __name__ == '__main__':

    circles = np.array([[[1132,  682,   24],
        [ 950,  692,   25],
        [1020,  516,   25],
        [1066,  358,   25],
        [1170,  490,   25],
        [ 944,  528,   25],
        [ 948,  608,   25],
        [1118,  520,   24],
        [ 896,  362,   26],
        [ 728,  698,   26],
        [1068,  420,   25],
        [ 996,  596,   25],
        [ 878,  626,   25],
        [1028,  252,   27],
        [ 626,  106,   22]]])

    STC_points_camera = np.array([[[ 944,  424,   25],
        [ 948,  608,   24],   
        [1132,  422,   24],
        [ 744,  232,   27],
        [ 764,  612,   24],
        [1132,  228,   26],
        [1132,  604,   23],
        [ 756,  426,   24],
        [ 938,  232,   25]]])

    x0, y0 = 227.9508, -173.1939

    m_circles = Packup(circles, STC_points_camera, x0, y0)
    for elements in m_circles:
        print(elements)
    print(type(elements))
