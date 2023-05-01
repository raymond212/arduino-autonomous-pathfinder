import cv2 as cv
import numpy as np
import math

RED = (0, 0, 255)
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DIST_THRESHOLD = 60


# img = cv.imread('Photos/Grid9.jpg')
# cv.imshow("Image", img)

def rescale_frame(frame, scale):
    # Images, Videos, and Live Video
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)


def get_dist(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def insert_into_clusters(a, clusters):
    for cluster in clusters:
        if get_dist(a, cluster[0]) < DIST_THRESHOLD:
            cluster.append(a)
            return
    clusters.append([a])


def insert_into_xy_clusters(x, clusters):
    for cluster in clusters:
        if abs(x - cluster[0]) < DIST_THRESHOLD:
            cluster.append(x)
            return
    clusters.append([x])


def condense_clusters(condensed, clusters):
    for cluster in clusters:
        mean = sum(cluster) // len(cluster)
        condensed.append(mean)


def get_coordinates(a, rows, cols):
    x, y = a
    row, col = -1, -1
    for i in range(len(rows)):
        if abs(y - rows[i]) < DIST_THRESHOLD:
            row = i
    for j in range(len(cols)):
        if abs(x - cols[j]) < DIST_THRESHOLD:
            col = j
    return (row, col)


def identify_obstacles(img):
    # Pre-processing

    scaled = rescale_frame(img, 1)
    cv.imshow("Scaled", scaled)

    # cv.rectangle(scaled, (240, 30), (320, 100), WHITE, thickness=-1)
    # cv.rectangle(scaled, (240, 30), (320, 100), BLACK, thickness=3)

    cropped = scaled
    # cropped = img[30:420, 150:520]

    # adjusted = cv.convertScaleAbs(cropped, alpha=1, beta=50)
    # cv.imshow('Adjused', adjusted)

    gray = cv.cvtColor(cropped, cv.COLOR_BGR2GRAY)
    cv.imshow('Gray', gray)

    blur = cv.medianBlur(gray, 5)
    cv.imshow('Blur', blur)

    canny = cv.Canny(blur, 100, 175)
    cv.imshow('Canny', canny)

    contours, hierarchies = cv.findContours(canny, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    # print(f'{len(contours)} contour(s) found')

    # blank = scaled
    blank = np.zeros(cropped.shape, dtype='uint8')

    # cv.line(blank, (0,0), (150,20), RED, 1)
    # cv.line(blank, (640,480), (520,410), RED, 1)

    clusters = []
    gridpoints = []
    obstacles = set()
    good_rectangles = 0

    for cnt in contours:
        x, y, w, h = cv.boundingRect(cnt)
        area = w * h
        ratio = float(w) / h
        if area > 5000 and area < 50000 and 0.5 <= ratio and 0.5 <= (1 / ratio):
            cv.rectangle(blank, (x, y), (x + w, y + h), GREEN, thickness=1)
            insert_into_clusters((x, y), clusters)
            insert_into_clusters((x + w, y), clusters)
            insert_into_clusters((x, y + h), clusters)
            insert_into_clusters((x + w, y + h), clusters)
            good_rectangles += 1
        elif area > 300 and area < 5000 and 0.9 <= ratio and 0.9 <= (1 / ratio):
            if len(cv.approxPolyDP(cnt, 0.01 * cv.arcLength(cnt, True), True)) == 8:
                cv.rectangle(blank, (x, y), (x + w, y + h), RED, thickness=1)
                obstacles.add((x + w // 2, y + h // 2))
                cv.putText(blank, 'Obstacle', (x, y), cv.FONT_ITALIC, 0.5, RED, 1)

    # print(good_rectangles)

    for cluster in clusters:
        x_sum, y_sum = 0, 0
        for x, y in cluster:
            x_sum += x
            y_sum += y
        x_mean = x_sum // len(cluster)
        y_mean = y_sum // len(cluster)
        gridpoints.append((x_mean, y_mean))

    # print(f'{len(gridpoints)} gridpoints found')

    column_clusters = []
    row_clusters = []

    for gridpoint in gridpoints:
        x, y = gridpoint
        cv.circle(blank, gridpoint, 20, BLUE, thickness=1)
        insert_into_xy_clusters(x, column_clusters)
        insert_into_xy_clusters(y, row_clusters)

    cols = []
    rows = []

    condense_clusters(cols, column_clusters)
    condense_clusters(rows, row_clusters)

    cols.sort()
    rows.sort()

    # print(cols)
    # print(rows)

    # for row in rows:
    #     cv.line(blank, (0,row), (scaled.shape[1],row), RED, thickness=1)

    # for column in cols:
    #     cv.line(blank, (column,0), (column,scaled.shape[0]), RED, thickness=1)

    obstacle_coordinates = set()
    for obstacle in obstacles:
        coordinates = get_coordinates(obstacle, rows, cols)
        if coordinates[0] >= 0 and coordinates[1] >= 0:
            obstacle_coordinates.add(coordinates)

    # print(obstacles)
    # print(obstacle_coordinates)

    cv.imshow('Contours Drawn', blank)
    return list(obstacle_coordinates)


def main():
    cap = cv.VideoCapture(1)
    while True:
        success, frame = cap.read()

        if not success:
            break

        identify_obstacles(frame)
        # cv.imshow('Video', frame)

        # exits when q key is pressed
        if cv.waitKey(20) & 0xFF == ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
