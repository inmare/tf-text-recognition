import numpy as np
import cv2


def crop(image: np.ndarray, top: int, side: int) -> np.ndarray:
    start_y = top
    end_y = image.shape[0] - side
    start_x = side
    end_x = image.shape[1] - side

    return image[start_y:end_y, start_x:end_x]


def invert(image: np.ndarray) -> np.ndarray:
    invert_img = cv2.bitwise_not(image)

    return invert_img


def binarization(image: np.ndarray, thresh: int, do_invert: bool = True) -> np.ndarray:
    if do_invert:
        image = invert(image)
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


def contrast(image, amount):
    # 출처: https://stackoverflow.com/questions/39308030/how-do-i-increase-the-contrast-of-an-image-in-python-opencv
    f = 131 * (amount + 127) / (127 * (131 - amount))
    alpha_c = f
    gamma_c = 127 * (1 - f)

    image = cv2.addWeighted(image, alpha_c, image, 0, gamma_c)

    return image


def rotate(image: np.ndarray, angle: float, center: list) -> np.ndarray:
    matrix = cv2.getRotationMatrix2D(tuple(center), angle, 1)
    rotate_img = cv2.warpAffine(
        image, matrix, (0, 0), flags=cv2.INTER_CUBIC, borderValue=255
    )

    return rotate_img


if __name__ == "__main__":
    pass
