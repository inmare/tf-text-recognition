import numpy as np
import math
import cv2
import os
import re
import text_extract.process as process


def get_file_names(file_settings: dict) -> list:
    file_path = file_settings["path"]
    dir_names = os.listdir(file_path)

    has_prefix = file_settings["hasPrefix"]
    prefix = file_settings["prefix"]
    regex = None
    file_names = []

    if has_prefix:
        regex = re.compile(f"^{prefix}.*\.jpg$")
    else:
        regex = re.compile("\.jpg$")

    for name in dir_names:
        is_match = regex.search(name)
        if is_match:
            file_names.append(name)

    file_names.sort()

    return file_names


def read_image(path: str, name: str) -> np.ndarray:
    image = cv2.imread(path + name, cv2.IMREAD_GRAYSCALE)

    return image


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


def get_char_info(image: np.ndarray, crop_settings: dict, mode: str) -> list:
    """이미지에서 글자에 대한 정보를 반환하는 함수

    Args:
        image (np.ndarray): 텍스트박스 이미지
        crop_settings (dict): json파일에서 읽어온 setting
        mode (str): 어떤 방향으로 읽을건지 정하는 모드
            "h"면 글자, "v"면 줄 단위로 구분되는 지점을 반환한다

    Returns:
        두개의 정보를 list형태로 반환한다
            crop_points (np.ndarray): 글자, 혹은 줄이 구분되는 지점
            max_length (int): 글자, 혹은 줄의 최대 크기
    """
    min_thresh = crop_settings["minThresh"]
    crop_top = crop_settings["cropTop"]
    crop_side = crop_settings["cropSide"]
    # TODO 만약 값이 낮아야 할 부분이 높다면 그걸로 사진의 오염을 판단하는 함수도 추후에 만들수도?

    # 이미지의 픽셀들을 한 방향으로 더한 다음 그 방향의 픽셀 개수로 나누어서
    # 픽셀 값들이 이미지의 높이나 넓이에 상관없이 일정한 비율을 유지하도록 함
    pixel_sum = None
    if mode == "h":
        pixel_sum = np.sum(image, axis=0) / image.shape[0]
    elif mode == "v":
        pixel_sum = np.sum(image, axis=1) / image.shape[1]

    low_value = np.min(pixel_sum)
    low_thresh = low_value + min_thresh
    low_points = pixel_sum < low_thresh

    check_start = None
    check_end = None
    crop_points = []

    for idx, is_low in enumerate(low_points):
        if is_low:
            if check_start == None:
                check_start = idx

            if idx == len(low_points) - 1 or not low_points[idx + 1]:
                if idx == len(low_points) - 1:
                    check_end = idx
                else:
                    check_end = idx + 1

                check_section = pixel_sum[check_start:check_end]
                min_point = np.argmin(check_section) + check_start
                crop_points.append(min_point)
                check_start = None
                check_end = None

    max_size = np.max(np.diff(crop_points))

    return [np.array(crop_points), max_size]


if __name__ == "__main__":
    pass
