import numpy as np
import cv2
from mss import mss
from config import CORDS
from lines import average_lane


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

        averaged_lines = average_lane(img, lines)
        print(averaged_lines)

        polygon = np.array([[averaged_lines[0][0], averaged_lines[0][1]], [averaged_lines[0][2], averaged_lines[0][3]],
                              [averaged_lines[1][2], averaged_lines[1][3]], [averaged_lines[1][0], averaged_lines[1][1]]])
        cv2.fillPoly(layer, pts=[polygon], color=color)
        # cv2.polylines(layer, [polygon], 1, color, 5)

    except Exception as e:
        print(e)
    return layer


def screen_capture():
    while True:

        with mss() as sct:
            img = np.array(sct.grab(CORDS))

        # Преобразование в Gray
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # cv2.line(img, (0, 250), (800, 250), (0, 0, 0), 3)

        # Блюр
        blur = cv2.GaussianBlur(img_gray, (3, 3), 3)

        # Затемнение
        # ret, thresh = cv2.threshold(blur, 100, 200, cv2.THRESH_BINARY)

        # Фильтр Canny
        edges = cv2.Canny(blur, 70, 200)

        # Выделение ROI (Region of Interests) - участка с дорогой
        vertices = np.array([[10, 400], [100, 300], [700, 300], [800, 400]])
        edges_roi = roi(edges, vertices)

        # Получаем layer с нарисованной фигурой дороги
        layer = draw_road(img, edges_roi, color=(0, 0, 255), thickness=3)
        # Наслаиваем layer с прозрачностью
        alpha = 0.3
        cv2.addWeighted(layer, alpha, img, 1 - alpha,
                        0, img)

        cv2.imshow('img', img)
        cv2.imshow('edges', edges)


        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


if __name__ == "__main__":
    screen_capture()
