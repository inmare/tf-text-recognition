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
    crop_setting = settings["crop"]
    crop_img = process.crop(image, **crop_setting)
    # crop_img = image

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


if __name__ == "__main__":
    passs
