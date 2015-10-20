__author__ = 'will'

from interface import RobotInterface
import time
import cv2

from view.tracker import Tracker

class Controller:

    def __init__(self):
        self.interface = RobotInterface()
        self.tracker = Tracker(self.interface)

        self.interface.set_left_speed(0.1)
        self.interface.set_right_speed(0.1)




        while True:
            ok, ways, intersections,com, self.colored_tracking_image = self.tracker.process_image()
            if ok:
                self.control(com)
                largeimg = cv2.resize(self.colored_tracking_image,(0,0),fx=3,fy=3)
                cv2.imshow("target", largeimg)

            ch = cv2.waitKey(5) & 0xFF
            if ch == 27:
                break
            time.sleep(0.05)

        self.interface.stop()
        cv2.destroyAllWindows()

    def control(self,center_of_mass):
        try:
            x = int(center_of_mass[1])-5
            print x
        except:
            return
        self.interface.set_right_speed(0.6+x*0.04)

        self.interface.set_left_speed(0.6+x*-0.04)

Controller()
