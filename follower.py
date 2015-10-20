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
        self.interface.set_right_speed(0.1)



        while True:

            self.process_image()

            ch = cv2.waitKey(5) & 0xFF
            if ch == 27:
                break
            time.sleep(0.05)
        self.interface.stop()
        cv2.destroyAllWindows()


    def process_image(self):
        img = None

        while not img:  img = self.interface.read_camera()
        img = numpy.array(img[2], dtype='int8').reshape(128, 128)
        cv2.imshow("camera", img[40:])

        ret,thresh2 = cv2.threshold(img.astype(numpy.uint8),127,255,cv2.THRESH_BINARY)
        cv2.imshow("bw", thresh2)

        mask = numpy.zeros((128, 128), numpy.uint8)
        print cv2.mean(img, mask)



Controller()
