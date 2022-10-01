import numpy as np
import cv2


def gray(image: np.ndarray) -> np.ndarray:
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    return gray_img


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
    erode_img = cv2.erode(image, kernel, iterations=1)

    return erode_img


def denoise(
    image: np.ndarray, strength: int, templateSize: int, searchSize: int
) -> np.ndarray:
    denoise_img = cv2.fastNlMeansDenoising(
        image, None, strength, templateSize, searchSize
    )

    return denoise_img


def increase_contrast(image: np.ndarray, multiply: float, add: int) -> np.ndarray:
    contrast_img = cv2.convertScaleAbs(image, alpha=multiply, beta=add)

    return contrast_img


def rotate(image: np.ndarray, angle: float, center: list) -> np.ndarray:
    t_center = tuple(center)
    print(type(t_center))
    print(type(t_center[0]))
    matrix = cv2.getRotationMatrix2D(tuple(center), angle, 1)
    rotate_img = cv2.warpAffine(image, matrix, image.shape, flags=cv2.INTER_CUBIC)

    return rotate_img


if __name__ == "__main__":
    pass
