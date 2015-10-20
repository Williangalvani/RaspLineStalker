__author__ = 'will'

from interface import RobotInterface
import time
import numpy as np
import cv2
from scipy import ndimage
from thining import thinning

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
        img = np.array(img[2], dtype='uint8').reshape(128, 128)
        cv2.imshow("camera", img[40:])

        h, w = img.shape[:2]
        threshold = int(np.mean(img[h/1.5]))*0.5
        print threshold


        ret, thresh2 = cv2.threshold(img.astype(np.uint8), threshold, 255, cv2.THRESH_BINARY_INV)
        erosion = thinning(thresh2)

        colored = cv2.cvtColor(erosion.astype(np.uint8), cv2.COLOR_GRAY2RGB)

        tracker = []

        for y, line in enumerate(thresh2):
            cx = ndimage.measurements.center_of_mass(line)
            if 4<np.mean(line)<50:
                tracker.append((int(cx[0]),y))
                if not np.isnan(cx[0]):
                    pass
                    cv2.circle(colored, (int(cx[0]), y), 1, (255, 0, 0), 2)
        #cv2.imshow("target", colored)
        return tracker, colored





Controller()
