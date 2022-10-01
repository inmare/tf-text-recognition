import text_extract.process as process
import text_extract.data as data
import numpy as np


def set_textbox_horizontally(image: np.ndarray, settings: dict):
    """글자가 수평이 되도록 이미지를 회전하는 함수

    Args:
        image (np.ndarray): 회전하고 싶은 이미지
        settings (dict): json파일에서 읽어온 setting

    Returns:
        np.ndarray: 회전한 이미지. 만약 이미지의 각도가 회전하지 않아도 되는 정도라면
        그냥 가장자리가 잘린 이미지를 반환한다
    """
    # crop_setting = settings["crop"]
    # crop_img = process.crop(image, **crop_setting)
    crop_img = image

    binary_thresh = settings["binarization"]["thresh"]
    binary_img = process.binarization(crop_img, binary_thresh, do_invert=True)

    dilation_setting = settings["dilation"]
    rotate_kernel_size = dilation_setting["kernel"]["toRotate"]
    dilate_img = process.dilation(binary_img, rotate_kernel_size)

    main_contour = data.get_main_contour(dilate_img)
    angle, center = data.get_roation_info(main_contour)

    rotation_thresh = settings["rotation"]["thresh"]
    if angle > -rotation_thresh and angle < rotation_thresh:
        return crop_img
    else:
        rotate_img = process.rotate(crop_img, -angle, center)
        return rotate_img


def extract_textbox(image: np.ndarray, settings: dict) -> np.ndarray:
    """이미지에서 글자가 모여있는 부분만 추출하는 함수

    Args:
        image (np.ndarray): 추출하고 싶은 이미지
        settings (dict): json파일에서 읽어온 setting

    Returns:
        np.ndarray: 글자부분만 있는 이미지
    """
    binary_thresh = settings["binarization"]["thresh"]
    binary_img = process.binarization(image, binary_thresh, do_invert=True)

    dilation_setting = settings["dilation"]
    erosion_setting = settings["erosion"]
    dilation_kernel_size = dilation_setting["kernel"]["toFindRect"]
    erosion_kernel_size = erosion_setting["kernel"]["toFindRect"]

    dilate_img = process.dilation(binary_img, dilation_kernel_size)
    erode_img = process.erosion(dilate_img, erosion_kernel_size)

    main_contour = data.get_main_contour(erode_img)
    [start_point, end_point] = data.get_rect_point(main_contour)

    textbox_img = image[start_point[1] : end_point[1], start_point[0] : end_point[0]]

    return textbox_img


def enhance_textbox(image: np.ndarray, settings: dict) -> np.ndarray:
    """텍스트박스 이미지를 개선시키는 함수

    Args:
        image (np.ndarray): 텍스트박스 이미지
        settings (dict): json파일에서 읽어온 setting

    Returns:
        np.ndarray: 노이즈 및 선명도가 개선된 반전된 텍스트박스 이미지 반환
    """
    invert_img = process.invert(image)

    denoise_settings = settings["denoise"]
    denoise_img = process.denoise(invert_img, **denoise_settings)

    contrast_settings = settings["contrast"]
    contrast_img = process.increase_contrast(denoise_img, **contrast_settings)

    return contrast_img


def get_char_info(image: np.ndarray, crop_settings: dict, mode: str) -> dict:
    """이미지에서 글자에 대한 정보를 반환하는 함수

    Args:
        image (np.ndarray): 텍스트박스 이미지
        crop_settings (dict): json파일에서 읽어온 setting
        mode (str): 어떤 방향으로 읽을건지 정하는 모드
            "h"면 글자, "v"면 줄 단위로 구분되는 지점을 반환한다

    Returns:
        dict: 글자에 대한 정보를 반환한다. 반환되는 객체의 구조는 아래와 같다.
            crop_points: 글자, 혹은 줄이 구분되는 지점을 ndarray형태로 반환한다.
            max_length: 글자, 혹은 줄의 최대 크기를 반환한다.
    """
    min_thresh = crop_settings["minThresh"]
    crop_top = crop_settings["cropTop"]
    crop_side = crop_settings["cropSide"]
    # TODO 만약 값이 낮아야 할 부분이 높다면 그걸로 사진의 오염을 판단하는 함수도 추후에 만들수도?

    # 이미지의 픽셀들을 한 방향으로 더한 다음 그 방향의 픽셀 개수로 나누어서
    # 픽셀 값들이 이미지의 높이나 넓이에 상관없이 일정한 비율을 유지하도록 함
    pixel_sum = None
    crop_img = None
    if mode == "h":
        pixel_sum = np.sum(image, axis=0) / image.shape[0]
        crop_img = image[:, crop_side : image.shape[1] - crop_side]
    elif mode == "v":
        pixel_sum = np.sum(image, axis=1) / image.shape[1]
        crop_img = image[crop_top : image.shape[0] - crop_top, :]

    low_thresh = np.min(pixel_sum) + min_thresh
    low_points = pixel_sum < low_thresh

    from matplotlib import pyplot as plt

    for is_low, value in zip(low_points, pixel_sum):
        pass


if __name__ == "__main__":
    passs
