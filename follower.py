__author__ = 'will'

from interface import RobotInterface
import time
import cv2
from input.keylistener import KeyListener


class Controller:

    def __init__(self):
        self.interface = RobotInterface()

        self.interface.set_left_speed(0)
        self.interface.set_right_speed(0)

        self.listener = KeyListener()

        while True:
            start = time.time()

            ### esta funcao, do "tracker" faz o processamento da imagem
            img = self.interface.get_image_from_camera()

            ### esta funcao faz o controle do robo
            self.control()

            ## estas duas linhas servem apenas para mostrar uma das imagens da tela
            cv2.imshow("target", img)

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


        velocidade = 0
        direcao = 0

        if self.listener.get_key(97):
            direcao = -1
        elif self.listener.get_key(100):
            direcao = 1
        if self.listener.get_key(119):
            velocidade = 1
        elif self.listener.get_key(115):
            velocidade = -1

        print direcao, velocidade
        self.interface.set_right_speed(0.8*velocidade + direcao*0.2)

        self.interface.set_left_speed(0.8*velocidade - direcao*0.2)

Controller()
