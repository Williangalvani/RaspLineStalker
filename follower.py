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

        self.lastError = 0

        while True:
            start = time.time()

            ### esta funcao, do "tracker" faz o processamento da imagem
            self.tracker.process_image()

            ### esta funcao faz o controle do robo
            self.control()

            ## estas duas linhas servem apenas para mostrar uma das imagens da tela
            largeimg = cv2.resize(self.tracker.colored, (0, 0), fx=3, fy=3)
            cv2.imshow("target", largeimg)

            ## esta parte do codigo detecta se a barra de espaco foi pressionada, para parar a simulacao
            ch = cv2.waitKey(5) & 0xFF
            if ch == 27:
                break
            print "took", time.time() - start

        self.interface.stop()
        cv2.destroyAllWindows()

    def control(self):
        """
        Calcula o controle das rodas
        :return:
        """
        try:
            posicaoRelativa = self.tracker.trackedPoint[0] - 64 # (posical relativa ao meio do sensor
            self.lastError = -posicaoRelativa
        except:
            pass
        self.interface.set_right_speed(2+self.lastError*-0.025)

        self.interface.set_left_speed(2+self.lastError*0.025)

Controller()
