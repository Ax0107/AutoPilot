import numpy as np

def average_lane(img, lines):

    left_fit = []
    right_fit = []

    while lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            parameters = np.polyfit((x1, x2), (y1, y2), 1)
            slope = parameters[0]
            intercept = parameters[1]

            # print(slope)
            if slope < 0:
                left_fit.append((slope, intercept))
            else:
                right_fit.append((slope, intercept))

        left_line = None
        right_line = None
        try:
            left_fit_average = np.average(left_fit, axis=0)
            # print('LEFT:', left_fit_average)
            left_line = make_coordinates(img, left_fit_average)

            right_fit_average = np.average(right_fit, axis=0)
            # print('RIGHT:', right_fit_average)
            right_line = make_coordinates(img, right_fit_average)
        except:
            pass
        if left_line is None:
            left_line = ((0, 600), (200, 400))

        if right_line is None:
            right_line = ((800, 600), (600, 400))

        return np.array([left_line, right_line])


def make_coordinates(img, line_params):
    slope, intercept = line_params

    y1 = img.shape[0]
    y2 = int(y1 * 4 / 7)

    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)

    return np.array([x1, y1, x2, y2])
