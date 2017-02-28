__author__ = 'will'

import pickle
import time
import cv2
from input.keylistener import KeyListener
from interface import RobotInterface

saved_data = []

GRAVA = True

USAREDE = not GRAVA

if USAREDE:
    import tensorflowtests.sklearntest

class Controller:
    def __init__(self):
        self.interface = RobotInterface()

        self.interface.set_left_speed(0.0)
        self.interface.set_right_speed(0.0)

        self.listener = KeyListener()
        next = time.time()

        self.velocidade = 0
        self.direcao = 0
        while True:

            ### esta funcao, do "tracker" faz o processamento da imagem
            img = self.interface.get_image_from_camera()

            if GRAVA:
                if time.time() > next:
                    saved_data.append((self.direcao, self.velocidade, img))
                    next = time.time() + 0.03
                    print(len(saved_data))

            if USAREDE:
                self.direcao = tensorflowtests.sklearntest.predict_direction(img)
                # print self.direcao
                time.sleep(0.001)

            ### esta funcao faz o controle do robo
            self.control()

            ## estas duas linhas servem apenas para mostrar uma das imagens da tela
            cv2.imshow("target", cv2.resize(img, (280, 280)))

            ## esta parte do codigo detecta se a barra de espaco foi pressionada, para parar a simulacao
            ch = cv2.waitKey(5) & 0xFF
            if ch == 27:
                if GRAVA:
                    pickle.dump(saved_data, open("trainingdata.p", "wb"))
                break

        self.interface.stop()
        cv2.destroyAllWindows()

    def control(self):
        """
        Calcula o controle das rodas
        :return:
        """

        self.velocidade = 0

        if not USAREDE:
            self.direcao = 0

            if self.listener.get_key(97):
                self.direcao = -1
            elif self.listener.get_key(100):
                self.direcao = 1

        if self.listener.get_key(119):
            self.velocidade = 3
        elif self.listener.get_key(115):
            self.velocidade = -3

        ganho = 0.2 if GRAVA else 0.6
        self.interface.set_right_speed(0.8 * self.velocidade + self.direcao * ganho)
        self.interface.set_left_speed(0.8 * self.velocidade - self.direcao * ganho)

Controller()
