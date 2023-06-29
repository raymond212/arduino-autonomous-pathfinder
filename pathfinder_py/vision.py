import cv2 as cv
import numpy as np
import math
from time import sleep

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

def identify_car_location(img):
    canny = cv.Canny(img, 100, 175)
    cv.imshow('Canny', canny)

    contours, hierarchies = cv.findContours(canny, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    # print(f'{len(contours)} contour(s) found')
    
    
    blank = np.zeros(img.shape, dtype='uint8')

    for i in range(len(contours)):
        cnt = contours[i]
        area = cv.contourArea(cnt)
        # if cv.contourArea(cnt) < 300:
        if (100 < area < 1000) and len(cv.approxPolyDP(cnt,0.05*cv.arcLength(cnt, True), True)) == 3:
            # print(area)
            cv.drawContours(blank, [cnt], 0, GREEN, 1)
            cv.imshow("Contour", blank)
            M = cv.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            return (cx, cy)
        # cnt = contours[i]
        # 
        # cv.imshow(f"Contour{i}", blank)

    # cv.drawContours(blank, contours, 0, GREEN, 1)
    return (-1, -1)

def process(img):
    cv.imshow('Original', img)

    scaled = rescale_frame(img, 1)

    cropped = scaled
    # cropped = img[30:420, 150:520]

    gray = cropped
    # gray = cv.cvtColor(cropped, cv.COLOR_BGR2GRAY)
    # cv.imshow('Gray', gray)

    blur = gray
    # blur = cv.medianBlur(gray, 0)
    # cv.imshow('Blur', blur)

    return blur



def identify_obstacles(img):

    processed = process(img)

    car_x, car_y = identify_car_location(processed)
    # print((car_x, car_y))

    if (car_x, car_y) != (-1, -1):
        car_w = 100
        car_h = 100
        cv.rectangle(processed, (car_x - car_w // 2, car_y - car_h // 2), (car_x + car_w // 2, car_y + car_h // 2), RED, thickness=-1)
        cv.rectangle(processed, (car_x - car_w // 2, car_y - car_h // 2), (car_x + car_w // 2, car_y + car_h // 2), BLACK, thickness=3)
    
    cv.imshow('Processed', processed)

    canny = cv.Canny(processed, 100, 175)
    cv.imshow('Canny', canny)    

    contours, hierarchies = cv.findContours(canny, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    # print(f'{len(contours)} contour(s) found')

    # blank = scaled
    blank = np.zeros(processed.shape, dtype='uint8')

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
        if tuple(processed[y + h // 2][x + w // 2]) == RED:
            continue
        elif area > 5000 and area < 50000 and 0.5 <= ratio and 0.5 <= (1 / ratio):
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

    for row in rows:
        cv.line(blank, (0,row), (processed.shape[1], row), RED, thickness=1)

    for column in cols:
        cv.line(blank, (column,0), (column, processed.shape[0]), RED, thickness=1)

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
    # success, frame = cap.read()
    # identify_obstacles(frame)
    # while True:
    #     if cv.waitKey(20) & 0xFF == ord('q'):
    #         break
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
