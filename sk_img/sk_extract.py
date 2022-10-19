from .sk_process import *
from .sk_data import *


def set_textbox_horizontally(image, settings):
    binary_thresh = settings["binarization"]["thresh"]
    binary_img = binarize(image, binary_thresh)

    rotate_kernel_size = settings["dilation"]["kernel"]["toRotate"]
    dilate_img = dilate(binary_img, rotate_kernel_size)

    main_contour = get_main_contour(dilate_img)

    rect_point = calc_min_area_rect(main_contour)
    [angle, center] = get_rotation_info(rect_point)

    rotate_img = rotate(image, -angle, center) * 255

    return rotate_img.astype(np.uint8)


def extract_textbox(image, settings):
    binary_thresh = settings["binarization"]["thresh"]
    binary_img = binarize(image, binary_thresh)

    dilate_kernel_size = settings["dilation"]["kernel"]["toFindRect"]
    dilate_img = dilate(binary_img, dilate_kernel_size)

    erode_kernel_size = settings["erosion"]["kernel"]["toFindRect"]
    erode_img = erode(dilate_img, erode_kernel_size)

    main_contour = get_main_contour(erode_img)

    [min_y, max_y, min_x, max_x] = get_bounding_box(main_contour)

    textbox = image[min_y:max_y, min_x:max_x]

    return textbox


def enhance_textbox(image, settings):
    bilateral_setting = settings["bilateral"]
    kernel_size = bilateral_setting["kernelSize"]
    sigma_color = bilateral_setting["sigmaColor"]
    sigma_space = bilateral_setting["sigmaSpace"]
    denoise_img = denoise(image, kernel_size, sigma_color, sigma_space)

    contrast_setting = settings["skContrast"]
    contrast_min = contrast_setting["min"]
    contrast_max = contrast_setting["max"]
    contrast_img = contrast(denoise_img, contrast_min, contrast_max)

    return contrast_img

    # from matplotlib import pyplot as plt

    # plt.figure(figsize=(5, 10))
    # plt.tight_layout()

    # plt.subplot(2, 1, 1)
    # plt.axis("off")
    # plt.imshow(denoise_img)
    # plt.title("denoise")
    # plt.subplot(2, 1, 2)
    # plt.axis("off")
    # plt.imshow(contrast_img)
    # plt.title("contrast")

    # cax = plt.axes([1.0, 0.1, 0.075, 0.8])
    # plt.colorbar(cax=cax)
    # plt.show()


if __name__ == "__main__":
    pass
