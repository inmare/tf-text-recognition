from skimage import io, color, filters, morphology, transform, restoration, exposure
import numpy as np


def gray(image):
    return color.rgb2gray(image)


def read(file_path: str, do_gray: bool = True) -> np.ndarray:
    image = io.imread(file_path)
    crop_image = image[400:700, :400]

    if do_gray and len(crop_image.shape) > 2:
        gray_image = gray(crop_image)
        return gray_image
    else:
        return crop_image


def save(image: np.ndarray, save_path: str):
    io.imsave(f"{save_path}/sample-textbox.png", image)


def invert(image: np.ndarray) -> np.ndarray:
    invert_img = np.invert(image)

    return invert_img


def binarize(image: np.ndarray, thresh: int, do_invert: bool = True) -> np.ndarray:
    binary_img = image > thresh

    invert_img = None
    if do_invert:
        invert_img = invert(binary_img)
    else:
        invert_img = binary_img

    return invert_img


def dilate(image: np.ndarray, kernel_size: list) -> np.ndarray:
    kernel = np.ones(tuple(kernel_size))
    dilate_img = morphology.dilation(image, kernel)

    return dilate_img


def erode(image: np.ndarray, kernel_size: list) -> np.ndarray:
    kernel = np.ones(tuple(kernel_size))
    erode_img = morphology.erosion(image, kernel)

    return erode_img


def denoise(
    image: np.ndarray, kernel_size: int, sigma_color: float, sigma_space: float
) -> np.ndarray:
    denoise_img = restoration.denoise_bilateral(
        image, kernel_size, sigma_color, sigma_space
    )

    return denoise_img


def contrast(image: np.ndarray, contrast_min: float, contrast_max: float) -> np.ndarray:
    contrast_img = exposure.rescale_intensity(
        image, in_range=(contrast_min, contrast_max)
    )

    return contrast_img


def rotate(image: np.ndarray, angle: float, center: list) -> np.ndarray:
    rotate_img = transform.rotate(image, angle, center=center, cval=1.0)

    return rotate_img


if __name__ == "__main__":
    pass
