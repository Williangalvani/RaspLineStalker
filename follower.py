__author__ = 'will'

from interface import RobotInterface
import time
import numpy
import cv2
from scipy import ndimage
RESX = 128
RESY = 128

CENTERX = RESX/2
CENTERY = RESY/2

class Controller:

    def __init__(self):
        self.interface = RobotInterface()
        self.interface.set_left_speed(0.1)
        self.interface.set_right_speed(0.1)



        while True:

            self.tracking_points, self.colored_tracking_image = self.process_image()

            self.control()

            cv2.imshow("target", self.colored_tracking_image)
            ch = cv2.waitKey(5) & 0xFF
            if ch == 27:
                break
            time.sleep(0.05)
        self.interface.stop()
        cv2.destroyAllWindows()

    def control(self):
        ypoint = 30
        try:
            cv2.circle(self.colored_tracking_image, (self.tracking_points[ypoint]), 5, (0, 255, 0), 2)
            cv2.circle(self.colored_tracking_image, (CENTERX,ypoint), 5, (0, 0, 255), 2)
        except:
            pass


    def process_image(self):
        img = None

        while not img:  img = self.interface.read_camera()
        img = numpy.array(img[2], dtype='int8').reshape(128, 128)
        cv2.imshow("camera", img[40:])

        ret,thresh2 = cv2.threshold(img.astype(numpy.uint8),127,255,cv2.THRESH_BINARY_INV)

        #mask = numpy.zeros((128, 128), numpy.uint8)

        colored = cv2.cvtColor(thresh2,cv2.COLOR_GRAY2RGB)

        tracker = []



        for y, line in enumerate(thresh2):
            cx = ndimage.measurements.center_of_mass(line)
            if 4<numpy.mean(line)<50:
                tracker.append((int(cx[0]),y))
                if not numpy.isnan(cx[0]):
                    cv2.circle(colored, (int(cx[0]), y ), 1, (255, 0, 0), 2)
        #cv2.imshow("target", colored)
        return tracker, colored





Controller()
