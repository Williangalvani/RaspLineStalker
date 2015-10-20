__author__ = 'will'
import numpy as np
import cv2
from scipy import ndimage
from thining import thinning



RESX = 128
RESY = 128

CENTERX = RESX/2
CENTERY = RESY/2

HEIGHT_SCAN = 100
WINDOW_SIZE = 10



class Tracker():

    windows_pos = (CENTERX,0+WINDOW_SIZE)

    def __init__(self, camera_interface):
        self.interface = camera_interface
        self.found_line = False

    def get_image_from_camera(self):
        """
        Loads image from camera.
        :return:
        """
        img = None
        while not img:  img = self.interface.read_camera()
        return img

    def prepare_image(self, img):
        """
        turns image to black and white and thins the line
        :return:
        """
        img = np.array(img[2], dtype='uint8').reshape(128, 128)
        cv2.imshow("camera", img)

        h, w = img.shape[:2]
        threshold = int(np.mean(img[h/1.5]))*0.5
        #print threshold


        ret, thresh2 = cv2.threshold(img.astype(np.uint8), threshold, 255, cv2.THRESH_BINARY_INV)
        erosed = thinning(thresh2)
        return erosed


    def square(self):
        """
        generates square coodinates for the window
        :return:
        """
        bottom = [(x-WINDOW_SIZE/2, WINDOW_SIZE/2)  for x in range(WINDOW_SIZE+1)]
        top =    [(x-WINDOW_SIZE/2, -WINDOW_SIZE/2) for x in range(WINDOW_SIZE+1)]
        left =   [(-WINDOW_SIZE/2, y-WINDOW_SIZE/2) for y in range(WINDOW_SIZE+1)]
        right =  [(WINDOW_SIZE/2, y-WINDOW_SIZE/2)  for y in range(WINDOW_SIZE+1)]

        points = bottom + top + left + right

        return points



    def find_line(self, image):
        x = ndimage.measurements.center_of_mass(image[HEIGHT_SCAN])[0]
        y = HEIGHT_SCAN
        #print image[y][x]

        if image[y][x] > 100:
            self.found_line = True
            self.last_center = [x,y]
            return (x,y)
        return None

    def find_square(self,image):
        if not self.found_line:
            self.find_line(image)
            print "Found line at", self.last_center
            return None
        else:
            square = self.square()
            ways = 0
            intersections = []

            last_point_was_checked = False
            for point in square:
                px, py = point
                x = int(self.last_center[0]+px)
                y = int(self.last_center[1]+py)

                is_crossing = image[y][x]==255

                if is_crossing:
                    intersections.append((px,py))

                if not last_point_was_checked and is_crossing:
                    ways += 1
                last_point_was_checked = is_crossing

                color = (255, 0, 0) if is_crossing else (0, 0, 255)
                self.colored[y][x] = color

            x1,y1 = self.last_center
            x2,y2 = self.last_center
            x1-=WINDOW_SIZE/2
            y1-=WINDOW_SIZE/2
            x2+=WINDOW_SIZE/2
            y2+=WINDOW_SIZE/2

            subimage = image[y1:y2, x1:x2]
            #cv2.imshow("batata", subimage)
            com = ndimage.measurements.center_of_mass(subimage)
            if not np.isnan(com[0]):
                self.last_center[0] = com[0]-WINDOW_SIZE/2 + self.last_center[0]
            #print ways, intersections, com
            return ways, intersections, com


    def process_image(self):
        img = self.get_image_from_camera()
        prepared_image = self.prepare_image(img)
        self.colored = cv2.cvtColor(prepared_image.astype(np.uint8), cv2.COLOR_GRAY2RGB)
        result = None
        ok = False
        intersections = None
        com = None
        ways = None
        try:
            result =  self.find_square(prepared_image)
            ok = True
            ways, intersections, com = result
        except Exception, e:
            print e

        return ok, ways, intersections, com, self.colored
