from .sk_process import *
from .sk_data import *


def set_textbox_horizontally(image, settings):
    binary_thresh = settings["binarization"]["thresh"]
    binary_img = binarization(image, binary_thresh)

    rotate_kernel_size = settings["dilation"]["kernel"]["toRotate"]
    dilate_img = dilation(binary_img, rotate_kernel_size)

    main_contour = get_main_contour(dilate_img)

    rect_point = calc_min_area_rect(main_contour)
    [angle, center] = get_rotation_info(rect_point)

    rotate_img = rotate(image, -angle, center)

    return rotate_img


def extract_textbox(image, settings):
    pass


if __name__ == "__main__":
    pass
