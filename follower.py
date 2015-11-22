__author__ = 'will'

from interface import RobotInterface
import time
import cv2


class Controller:

    def __init__(self):
        self.interface = RobotInterface()

        self.interface.set_left_speed(0.1)
        self.interface.set_right_speed(0.1)

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
        self.interface.set_right_speed(0.025)

        self.interface.set_left_speed(0.025)

Controller()
