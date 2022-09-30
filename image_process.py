import numpy as np
import math
import cv2


def crop(image: np.ndarray, top: int, side: int) -> np.ndarray:
    """이미지를 잘라서 반환하는 함수

    Args:
        image (np.ndarray): 자르고 싶은 이미지
        margin_top (int): 상단부를 자르고 싶은 정도
        margin_side (int): 상단부 외 나머지를 자르고 싶은 정도

    Returns:
        np.ndarray: 잘린 이미지를 반환함
    """
    start_y = top
    end_y = image.shape[0] - side
    start_x = side
    end_x = image.shape[1] - side

    return image[start_y:end_y, start_x:end_x]


def binarization(image: np.ndarray, thresh: int, invert: bool = True) -> np.ndarray:
    if invert:
        image = cv2.bitwise_not(image)
    ret, dst = cv2.threshold(image, thresh, 255, cv2.THRESH_BINARY)

    return dst


def dilation(image: np.ndarray, kernel_size: list) -> np.ndarray:
    kernel = np.ones(tuple(kernel_size))
    dilate_img = cv2.dilate(image, kernel, iterations=1)

    return dilate_img


def erosion(image: np.ndarray, kernel_size: list) -> np.ndarray:
    kernel = np.ones(tuple(kernel_size))
    erode_img = cv2.erode(image, np.ones((15, 1)), iterations=1)

    return erode_img


def denoise(image: np.ndarray, strength: int, templateSize: int, searchSize: int) -> np.ndarray:
    denoise_img = cv2.fastNlMeansDenoising(
        image, None, strength, templateSize, searchSize)

    return denoise_img


def increase_contrast(image: np.ndarray, multiply: float, add: int) -> np.ndarray:
    contrast_img = cv2.convertScaleAbs(image, multiply=alpha, add=beta)

    return contrast_img


def get_main_contour(image: np.ndarray) -> np.ndarray:
    contours, hier = cv2.findContours(
        image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    main_contour = max(contours, key=len)

    return main_contour


def get_roation_angle(contour: np.ndarray) -> float:
    min_rect = cv2.minAreaRect(contour)
    box = cv2.boxPoints(min_rect)
    box = np.intp(box)

    # 직사각형 왼쪽 위 좌표와 오른쪽 위 좌표를 이용해 두 점을 잇는 선이 빗변이 되는 직각삼각형을 만들고,
    # 이를 이용해서 얼마나 사각형이 회전했는지 확인한다
    p_1 = box[0]
    p_2 = box[1]
    p_3 = [p_2[0], p_1[1]]
    diag_len = np.linalg.norm(p_2 - p_1)
    hori_len = np.linalg.norm(p_3 - p_2)
    angle = np.rad2deg(math.acos(hori_len/diag_len))
    print(box)

    return angle, tuple(p_1)


def rotate(image: np.ndarray, angle: float, center: tuple) -> np.ndarray:
    matrix = cv2.getRotationMatrix2D(center, angle, 1)
    rotate_img = cv2.warpAffine(
        image, matrix, image.shape, flags=cv2.INTER_CUBIC)

    return rotate_img


def get_rect_point(contour: np.ndarray) -> list:
    contour_poly = cv2.approxPolyDP(contour, 3, True)
    bounding_rect = cv2.boundingRect(contour_poly)

    start_point = np.intp((bounding_rect[0], bounding_rect[1]))
    end_point = np.intp(
        (bounding_rect[0] + bounding_rect[2], bounding_rect[1] + bounding_rect[3]))

    return [start_point, end_point]


def extract_textbox(image: np.ndarray, settings: dict) -> np.ndarray:
    binary_thresh = settings.binarization.thresh
    binary_img = binarization(image, thresh)

    dilation_kernel_size = settings.dilation.kernel.toFindRect
    erosion_kernel_size = settings.erosion.kernel.toFindRect
    dilate_img = dilation(binary_img, dilation_kernel_size)
    erode_img = erosion(dilate_img, erosion_kernel_size)

    main_contour = get_main_contour(erode_img)
    [start_point, end_point] = get_rect_point(main_contour)

    textbox_img = image[start_point[1]:end_point[1], start_point[0]:end_point[0]]

    return textbox_img
