
import sys
import time
import socket
import numpy as np
from Packup import Packup
from CameraRead import OpenCamera


def Connect(circles, STC_points_camera, x0, y0):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # AF_INET (IPv4): address.
            # SOCK_STREAM: type, use TCP as the protocol.
        except socket.error as msg:
            print('Failed to create socket(ﾟДﾟ*)ﾉ! Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1])
            sys.exit()

        print('Socket Created!(*^▽^*)')

        try:
            remote_ip = '192.168.5.1'
            port = 6601

        # When it could not be resolved:
        except socket.gaierror:
            print('Hostname could not be resolved. Exiting.')
            sys.exit()
    
        print('Ip address of the client is ' + remote_ip + '. Connecting...')

        # Connect to remote server.
        s.connect((remote_ip , port))

        print('Socket Connected to the client!☆*: .｡. o(≧▽≦)o .｡.:*☆')

        # Send some data to remote server.
        m_circles = Packup(circles, STC_points_camera, x0, y0)

        for m_circle in m_circles:
            try:
              message = str(m_circle)
              messagebytes = bytes(message,'UTF-8')
              s.sendall(messagebytes)
                  
            except socket.error:
            #Send failed.
                 print('Send failed!')
                 sys.exit()

            localtime = time.strftime('%H:%M:%S', time.localtime())
            print(localtime + ':Message send successfully! o((>ω< ))o:\n' + str(message))

          # Now receive data.
            reply = s.recv(4096)
            # print('reply received from the remote server!ヾ(≧ ▽ ≦)ゝ')
            # print(reply)
        print('All circles in the batch has been sent!')
        s.close()


if __name__ == '__main__':
    STC_points_camera = np.array([[[1112,  438,   28],
        [1110,  640,   28],
        [ 910,  438,   28],
        [ 910,  232,   28],
        [1318,  642,   28],
        [ 910,  642,   28],
        [1114,  232,   28],
        [1322,  232,   28],
        [1320,  438,   28]]])
    
    print('Acquiring 9 points for the calibration...\n')
    # circles_b, circles_w, STC_points_camera = OpenCamera(0)
    print('9 points acquired!\n')
    print(STC_points_camera)
    
    x0, y0 = 227.3687, -111.1425

    circles_b, circles_w, circles_sorted = OpenCamera(0)
    Connect(circles_sorted, STC_points_camera, x0, y0)



