import cv2
import numpy as np


def OpenCamera(idx):
   cap = cv2.VideoCapture(idx)
   print("Is camera opened? --- {}".format(cap.isOpened()))

   cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
   cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

   cv2.namedWindow('image_win',flags=cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_GUI_EXPANDED)

   global ret, circles, circles_b, circles_w
   count = 1
   img_count = 1
   ret, frame = cap.read()
   cv2.imwrite('origin.png', frame)

   while(True):
       # if read successfully, ret=True. type(frame) = np.ndarray.
       ret, frame = cap.read()

       cv2.imwrite("frame.png", frame)

       if not ret:
       # if failed.
           print("Video read failed or terminated.")
           break

##########################################################
    #    for the processing of the image.
       img = cv2.imread('frame.png')
       gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

       blurred = cv2.GaussianBlur(gray, (5, 5), 0)

       circles = cv2.HoughCircles(blurred,  method=cv2.HOUGH_GRADIENT,
                           dp=1, minDist=25, param1=100, param2=35,
                           minRadius=15, maxRadius=40)

       if circles is not None:
           circles_b = []
           circles_w = []
           circles = np.uint16(np.around(circles))

           for i in circles[0, :]:
               center = (i[0], i[1])
               if np.mean(gray[center[1] - 2:center[1] + 3, center[0] - 2:center[0] + 3]) < 127:
                   piece_color = "Black"
               else:
                   piece_color = "White"

               cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
               cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)
            #    print(f"{piece_color} piece detected at {center}.")
               if piece_color == "Black":
                   circles_b.append([center[0], center[1], i[2]])
               else:
                   circles_w.append([center[0], center[1], i[2]])
       
       circles_sorted = []
       for circle_b in circles_b:
           circles_sorted.append(circle_b)
       for circle_w in circles_w:
            circles_sorted.append(circle_w)
       circles_b = np.array([circles_b])
       circles_w = np.array([circles_w])
       circles_sorted = np.array([circles_sorted])
    
##########################################################

       cv2.imshow('image_win',frame)
       count += 1

       key = cv2.waitKey(1)
       if key == ord('q'):
           print("Video quitted successfully.")
           break
       elif key == ord('c'):
           cv2.imwrite("{}.png".format(img_count), frame)
           print("captured as {}.png successfully.".format(img_count))
           img_count += 1

   cap.release()
   cv2.destroyAllWindows()
   return circles_b, circles_w, circles_sorted

if __name__ == '__main__':
    circles_b, circles_w, circles_sorted = OpenCamera(0)
