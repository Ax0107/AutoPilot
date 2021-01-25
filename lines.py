import numpy as np
from sklearn.cluster import DBSCAN


def average_lane(img, lines):

    lines_fit = []
    while lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            # if abs(y1 - y2) < 40:
            #     continue

            parameters = np.polyfit((x1, x2), (y1, y2), 1)
            slope = parameters[0]
            intercept = parameters[1]
            lines_fit.append((slope, intercept, x1, y1, x2, y2))

        if len(lines_fit) == 1:
            lines_fit = np.array(lines_fit).reshape(-1, 1)

        cluster_model = DBSCAN(eps=100, min_samples=1)
        clusters = cluster_model.fit_predict(np.array(lines_fit))

        # TODO: Refactor to func

        result_lines = []

        clusters_lines = {i: [] for i in list(set(clusters))}
        for i, cluster in enumerate(list(set(clusters))):
            clusters_lines[cluster].append(lines_fit[i])

        #print('DC', clusters_lines[0], '\n===========')

        for cluster, data in clusters_lines.items():
            data = np.abs(data)
            data = np.average(data, axis=0)
            print(data)
            data = make_coordinates(img, data[:2], *data[2:])
            data = np.abs(data)
            print('Data for cluster {}: {}\n======'.format(cluster, data))
            result_lines.append(data)

        #print(len(clusters_lines))

        # try:
        #     left_fit_average = np.average(left_fit, axis=0)
        #
        #     left_line = make_coordinates(img, left_fit_average)
        #
        #     right_fit_average = np.average(right_fit, axis=0)
        #     right_line = make_coordinates(img, right_fit_average)
        # except:
        #     pass
        # if left_line is None:
        #     left_line = ((0, 600), (200, 400))
        #
        # if right_line is None:
        #     right_line = ((800, 600), (600, 400))

        # return np.array([left_line, right_line])
        return result_lines


def make_coordinates(img, line_params, x1, y1, x2, y2):
    slope, intercept = line_params

    # y1 = y1
    # y2 = int(y1 * 3.5 / 7)
    # x1 = x1
    # x2 = int((x1 - intercept) / slope)

    return np.array([x1, y1, x2, y2])
