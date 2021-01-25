import numpy as np
import cv2
from mss import mss
from config import CORDS
from lines import average_lane
from pynput import keyboard
import pyautogui
from threading import Thread
from pynput.keyboard import Controller
import time
import random

from directkey import PressKey, W, S, D, A


keyboard_contr = Controller()

def roi(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, [vertices], 255)
    masked = cv2.bitwise_and(img, mask)
    return masked


def draw_road(img, edges, color=None, thickness=3):

    layer = img.copy()

    if color is None:
        color = (255, 255, 255)
    try:

        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=50, maxLineGap=50)

        averaged_lines = np.array(average_lane(img, lines))
        # averaged_lines = averaged_lines.reshape(len(averaged_lines), 4)
        # print('Average_lines', averaged_lines)

        p = np.array([[[averaged_lines[i][0], averaged_lines[i][1]], [averaged_lines[i][2], averaged_lines[i][3]]] for i in range(len(averaged_lines))]).astype(np.int32)
        for line in p:
            print(line)
            cv2.line(img, (line[0][0], line[0][1]), (line[1][0], line[1][1]), random.sample(range(0, 255), 3), 10)

        #
        # for line in averaged_lines:
        #     print('L', line, '+++')
        #     line = line.astype(np.int)
        #     cv2.line(img, (line[2], line[3]), (line[0], line[1]),  color, 10)

        #     polygon = np.array([[averaged_lines[0][0], averaged_lines[0][1]], [averaged_lines[0][2], averaged_lines[0][3]],
        #                           [averaged_lines[1][2], averaged_lines[1][3]], [averaged_lines[1][0], averaged_lines[1][1]]])
        # cv2.fillPoly(layer, pts=[polygon], color=color)
        # cv2.polylines(layer, [polygon], 1, color, 5)
        #
    except Exception as e:
        print(e)
    return layer


WORKING = True


def on_release(key):
    global WORKING
    if str(key) == "'l'":
        WORKING = False


# Collect events until released
listener = keyboard.Listener(
        on_release=on_release)
listener.start()


KEYBOARD_STACK = []


def keyboard_commands():
    global KEYBOARD_STACK
    while True:
        try:
            PressKey(KEYBOARD_STACK[0])
            KEYBOARD_STACK.pop(0)
        except:
            pass
        time.sleep(1)


def screen_capture():
    global WORKING
    global keyboard_contr

    Thread(target=keyboard_commands).start()

    while WORKING:

        with mss() as sct:
            img = np.array(sct.grab(CORDS))

        # Преобразование в Gray
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # cv2.line(img, (0, 250), (800, 250), (0, 0, 0), 3)

        # Блюр
        blur = cv2.GaussianBlur(img_gray, (5, 5), 3)

        # Затемнение
        ret, thresh = cv2.threshold(blur, 220, 250, cv2.THRESH_TRUNC)
        # blur = cv2.GaussianBlur(thresh, (3, 3), 5)
        # ret, thresh = cv2.threshold(blur, 150, 250, cv2.THRESH_BINARY)

        # Фильтр Canny
        edges = cv2.Canny(thresh, 70, 200)

        # Выделение ROI (Region of Interests) - участка с дорогой
        vertices = np.array([[0, 400], [0, 400], [200, 200], [600, 200], [800, 400], [800, 400]])
        edges_roi = roi(edges, vertices)

        # cv2.polylines(img, [vertices], 1, color=(0, 255, 255), thickness=2)

        # Получаем layer с нарисованной фигурой дороги
        layer = draw_road(img, edges_roi, color=(0, 0, 255), thickness=3)
        # Наслаиваем layer с прозрачностью
        alpha = 0.3
        cv2.addWeighted(layer, alpha, img, 1 - alpha,
                        0, img)

        cv2.imshow('edges_roi', edges_roi)
        cv2.imshow('img', img)
        # cv2.imshow('edges', edges)



        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


if __name__ == "__main__":

    screen_capture()
