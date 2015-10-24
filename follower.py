__author__ = 'will'

from interface import RobotInterface
import time
import cv2

import math
from view.tracker import Tracker

class Controller:

    def __init__(self):
        self.interface = RobotInterface()
        self.tracker = Tracker(self.interface)

        self.interface.set_left_speed(0.1)
        self.interface.set_right_speed(0.1)

        while True:
            start = time.time()
            self.tracker.process_image()

            self.control()
            largeimg = cv2.resize(self.tracker.colored, (0, 0), fx=3, fy=3)
            cv2.imshow("target", largeimg)
            ch = cv2.waitKey(5) & 0xFF
            if ch == 27:
                break
            print "took", time.time() - start

        self.interface.stop()
        cv2.destroyAllWindows()

    def control(self):
        points = self.tracker.points
        #center = sum([point[0] for point in points if point is not None])/len(points)

        try:
            valid = [point for point in points if point is not None]
            erro = 64-valid[-1][0]
            #print erro
        except:
            erro = 0

        self.interface.set_right_speed(2+erro*-0.015)

        self.interface.set_left_speed(2+erro*0.015)

Controller()
