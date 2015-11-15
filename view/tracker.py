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


class Node:
    children=[]
    pos = (0,0)

    def __repr__(self):
        for child in self.children:
            print child



class Tracker():
    trackedPoint = (0,0)
    windows_pos = (CENTERX,0+WINDOW_SIZE)
    points = []
    lines = [127, 120, 110, 100, 90, 80]

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



    def find_start_point(self):
        """
        procura o primeiro pixel branco do meio pra fora, de baixo pra cima
        :return:
        """
        lines, rows = self.prepared_image.shape # certo?
        for linenumber, line in enumerate(reversed(self.prepared_image)):
            size = len(line)
            middle = size/2
            for i in range(middle):
                if line[middle+i] == 255:
                    return (middle+i, lines-linenumber-1)

                elif line[middle-i] == 255:
                    return (middle-i, lines-linenumber-1)



    def find_path(self):
        start_point = self.find_start_point()
        cv2.circle(self.colored, start_point, 4, (255, 0, 0), 2)
        self.trackedPoint = start_point



    def process_image(self):

        img = self.get_image_from_camera()
        self.prepared_image = self.prepare_image(img)[1:124, 1:124]
        self.colored = cv2.cvtColor(self.prepared_image.astype(np.uint8), cv2.COLOR_GRAY2RGB)
        self.find_path()
        cv2.imshow("prepared",self.prepared_image)
