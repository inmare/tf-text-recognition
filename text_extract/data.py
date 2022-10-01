import numpy as np
import math
import cv2
import text_extract.process as process


def read_image(path: str, name: str) -> np.ndarray:
    image = cv2.imread(path + name + ".jpg")
    gray_img = process.gray(image)

    return gray_img


def get_rect_point(contour: np.ndarray) -> list:
    contour_poly = cv2.approxPolyDP(contour, 3, True)
    bounding_rect = cv2.boundingRect(contour_poly)

    start_point = np.intp((bounding_rect[0], bounding_rect[1]))
    end_point = np.intp(
        (bounding_rect[0] + bounding_rect[2], bounding_rect[1] + bounding_rect[3])
    )

    return [start_point, end_point]


def get_main_contour(image: np.ndarray) -> np.ndarray:
    contours, hier = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    main_contour = max(contours, key=len)

    return main_contour


def get_roation_info(contour: np.ndarray) -> float:
    min_rect = cv2.minAreaRect(contour)
    box = cv2.boxPoints(min_rect)
    box = np.int0(box)

    # opencv에서 얻은 box좌표들을 오른쪽 위 좌표부터 시계방향으로 정렬함
    sorted_box = []
    for point in box:
        sorted_box.append(list(point))

    sorted_box.sort()

    # 직사각형 왼쪽 위 좌표와 오른쪽 위 좌표를 이용해 두 점을 잇는 선이 빗변이 되는 직각삼각형을 만들고,
    # 이를 이용해서 얼마나 사각형이 회전했는지 확인한다
    top_left = np.array(sorted_box[0])
    top_right = np.array(sorted_box[2])
    vertex = np.array([top_right[0], top_left[1]])

    diag_len = np.linalg.norm(top_right - top_left)
    hori_len = np.linalg.norm(vertex - top_left)
    angle = np.rad2deg(math.acos(hori_len / diag_len))

    center = [int(top_left[0]), int(top_left[1])]

    return angle, center


if __name__ == "__main__":
    pass
