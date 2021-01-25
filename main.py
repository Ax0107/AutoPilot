import numpy as np
import cv2
from mss import mss
from sklearn.cluster import DBSCAN

cords = {'top': 60, 'left': 1920, 'width': 800, 'height': 600-60}


def roi(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, [vertices], 255)
    masked = cv2.bitwise_and(img, mask)
    return masked


def draw_road(img, edges, color=None, thickness=3):
    if color is None:
        color = (255, 255, 255)

    try:

        # lines_data = []
        # for l in lines:
        #     l = l.reshape(2, len(l))
        #     data = [min(l[0]), min(l[1]), max(l[0]), max(l[1])]
        #     lines_data.append(data)
        # print(lines_data, '\n')
        # cluster_model = DBSCAN(eps=0.3, min_samples=2).fit(lines_data)
        #
        # print(cluster_model.labels_)
        # print(img.shape)
        cv2.line(img, (0, 250), (800, 250), (0, 0, 0), 3)
        contours, hierarchy = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        road_lines = []
        aps = []
        for n, c in enumerate(contours):
            # аппроксимируем (сглаживаем) контур
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(approx) > 1:
                cv2.drawContours(img, [approx], -1, color, 1)
                aps.append(approx)

        copy_approx = np.array(aps.copy())

        left = []
        right = []
        for line in aps:
            # print(line)
            # Если в правой части
            if line[0][0][0] > 400:
                right.append(line[0])
            else:
                left.append(line[0])

        xy_left = np.array(left).reshape(2, len(left))
        xy_right = np.array(right).reshape(2, len(right))

        max_x_left = max(xy_left[0])
        min_y_left = min(xy_left[1])

        min_x_right = min(xy_right[0])
        min_y_right = min(xy_right[1])

        cv2.line(img, (0, 400), (max_x_left, min_y_left), color, 5)
        cv2.line(img, (800, 400), (min_x_right, min_y_right), color, 5)

        # copy_approx = copy_approx.reshape(2, len(copy_approx))
        # min_y = min(copy_approx[1])
        # min_x = min(copy_approx[0])
        # print(min_y)
        # cv2.line(img, (min_x, min_y), (800, min_y), (255, 255, 255), 5)
        # [[[ 78 349]]
        #
        #  [[652 334]]
        #
        #  [[682 325]]
        #
        #  [[687 324]]
        #
        #  [[639 332]]
        #
        #  [[233 289]]
        #
        #  [[233 287]]
        #
        #  [[267 284]]]

        print(copy_approx, '\n\n\n\n')


        # polylines = ((0, 600), (0, min(copy_approx[1])), (max(copy_approx[0], max(copy_approx[1])), (max(copy_approx[0], max(copy_approx[1]))))
        # cv2.polylines(img, , color, thickness=10)

        # sorted_cntrs = sorted(cntrs_peri, key=lambda x: x[0])

        #cv2.drawContours(img, [i[1] for i in cntrs_peri], -1, color, thickness)
    except:
        pass
    return img

def screen_capture():
    while True:

        with mss() as sct:
            img = np.array(sct.grab(cords))

        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        vertices = np.array([[10, 400], [10, 400], [200, 250], [600, 250], [800, 400], [800, 400]])

        img = roi(img, vertices)
        cv2.line(img, (0, 250), (800, 250), (0, 0, 0), 3)

        blur = cv2.GaussianBlur(img, (3, 3), 3)
        ret, thresh = cv2.threshold(blur, 100, 200, cv2.THRESH_BINARY)
        edges = cv2.Canny(thresh, 70, 200)

        img = draw_road(img, edges)

        numpy_vertical = np.hstack((img, thresh))
        cv2.imshow('test', numpy_vertical)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


def process_img(img):
    pass


if __name__ == "__main__":
    screen_capture()