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


    def square(self,size):
        """
        generates square coodinates for the window
        :return:
        """
        bottom = [(x-size, size)  for x in range(2*size+1)]
        top =    [(x-size, -size) for x in range(2*size+1)]
        left =   [(-size, y-size) for y in range(2*size+1)]
        right =  [(size, y-size)  for y in range(2*size+1)]
        points = bottom + top + left + right
        return points


    def square_around(self,x1,y1,size):
        bottom = [(x1+x-size,y1+ size)  for x in range(2*size+1)]
        top =    [(x1+x-size,y1+ -size) for x in range(2*size+1)]
        left =   [(x1+-size,y1+ y-size) for y in range(2*size+1)]
        right =  [(x1+size,y1+ y-size)  for y in range(2*size+1)]
        points = bottom + top + left + right
        return points


#######################################################3


    def find_start_point(self):
        lines, rows = self.prepared_image.shape # certo?
        for linenumber, line in enumerate(reversed(self.prepared_image)):
            size = len(line)
            middle = size/2
            for i in range(middle):
                if line[middle+i] == 255:
                    return (middle+i, lines-linenumber-1)

                elif line[middle-i] == 255:
                    return (middle-i, lines-linenumber-1)


    class Node():
        pos = 0,0
        children = []


    def find_closest_points_around(self,point):
        found = []
        maxrange = 6
        x,y = point
        for i in range(maxrange):
            points = self.square_around(x, y, i)
            for x,y in points:
                try:
                    if self.prepared_image[y][x]==255:
                        found.append((x,y))
                except:
                    pass
            if len(found):
                return found
            #print i == 4
        return []


    def tree_from_start_point(self,start_point):
        node = Node()
        node.pos = start_point
        x,y = start_point
        try:
            self.prepared_image[y][x]=127
        except Exception, e:
            print y, e
            return None
        points_around = self.find_closest_points_around((x,y))
        for p in points_around:
            childnode = self.tree_from_start_point(p)
            if childnode is not None:
                node.children.append(childnode)
        return node


    def find_path(self):
        start_point = self.find_start_point()
        print start_point
        cv2.circle(self.colored, start_point, 4, (255, 0, 0), 2)
        tree = self.tree_from_start_point(start_point)
        #return tree



    def process_image(self):

        img = self.get_image_from_camera()
        self.prepared_image = self.prepare_image(img)[1:124, 1:124]
        self.colored = cv2.cvtColor(self.prepared_image.astype(np.uint8), cv2.COLOR_GRAY2RGB)
        self.find_path()
        cv2.imshow("prepared",self.prepared_image)
        #for point in self.points:
        #    cv2.circle(self.colored, point, 4, (255, 0, 0), 1)

