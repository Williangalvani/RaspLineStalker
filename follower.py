__author__ = 'will'

from interface import RobotInterface
import time
import numpy
from matplotlib import pyplot as plt
import cv2

class Controller:

    def __init__(self):
        self.interface = RobotInterface()
        self.interface.set_left_speed(0.1)

        while True:

            img = None
            while not img:  img = self.interface.read_camera()
            img = numpy.array(img[2],dtype='int8').reshape(128, 128)
            cv2.imshow("camera",img)




            ch = cv2.waitKey(5) & 0xFF
            if ch == 27:
                break
            time.sleep(0.05)
        cv2.destroyAllWindows()


Controller()
