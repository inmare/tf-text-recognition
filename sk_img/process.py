from skimage import morphology
from skimage import io, color, filters
import numpy as np


def read(file_path: str, do_gray: bool = True) -> np.ndarray:
    image = io.imread(file_path)
    crop_image = image[400:700, :400]

    if do_gray and len(crop_image.shape) > 2:
        gray_image = color.rgb2gray(crop_image)
        return gray_image
    else:
        return crop_image


def invert(image: np.ndarray) -> np.ndarray:
    invert_img = np.invert(image)

    return invert_img


def binarization(image: np.ndarray, thresh: int, do_invert: bool = True) -> np.ndarray:
    invert_img = None

    if do_invert:
        invert_img = invert(image)
    else:
        invert_img = image

    binary_img = invert_img > thresh

    return binary_img


def dilation(image: np.ndarray, kernel_size: list) -> np.ndarray:
    kernel = np.ones(tuple(kernel_size))
    dilate_img = morphology.dilation(image, kernel)

    return dilate_img


def erosion(image: np.ndarray, kernel_size: list) -> np.ndarray:
    kernel = np.ones(tuple(kernel_size))
    erode_img = morphology.erosion(image, kernel)

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
