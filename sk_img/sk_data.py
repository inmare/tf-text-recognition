from skimage import measure
from scipy import spatial
import numpy as np
import math


def get_main_contour(image: np.ndarray):
    contours = measure.find_contours(image)
    main_contour = max(contours, key=len)

    return main_contour


def calc_convex_hull(contour):
    hull_points = spatial.ConvexHull(contour)

    return hull_points


# 코드 출처: https://stackoverflow.com/questions/13542855/algorithm-to-find-the-minimum-area-rectangle-for-given-points-in-order-to-comput
def calc_min_area_rect(contour):
    # get the convex hull for the points
    hull = calc_convex_hull(contour)
    hull_points = contour[hull.vertices]
    pi2 = np.pi / 2

    # calculate edge angles
    edges = np.zeros((len(hull_points) - 1, 2))
    edges = hull_points[1:] - hull_points[:-1]

    angles = np.zeros((len(edges)))
    angles = np.arctan2(edges[:, 1], edges[:, 0])

    angles = np.abs(np.mod(angles, pi2))
    angles = np.unique(angles)

    # find rotation matrices
    # XXX both work
    rotations = np.vstack(
        [np.cos(angles), np.cos(angles - pi2), np.cos(angles + pi2), np.cos(angles)]
    ).T
    #     rotations = np.vstack([
    #         np.cos(angles),
    #         -np.sin(angles),
    #         np.sin(angles),
    #         np.cos(angles)]).T
    rotations = rotations.reshape((-1, 2, 2))

    # apply rotations to the hull
    rot_points = np.dot(rotations, hull_points.T)

    # find the bounding points
    min_x = np.nanmin(rot_points[:, 0], axis=1)
    max_x = np.nanmax(rot_points[:, 0], axis=1)
    min_y = np.nanmin(rot_points[:, 1], axis=1)
    max_y = np.nanmax(rot_points[:, 1], axis=1)

    # find the box with the best area
    areas = (max_x - min_x) * (max_y - min_y)
    best_idx = np.argmin(areas)

    # return the best box
    x1 = max_x[best_idx]
    x2 = min_x[best_idx]
    y1 = max_y[best_idx]
    y2 = min_y[best_idx]
    r = rotations[best_idx]

    rval = np.zeros((4, 2))
    rval[0] = np.dot([x1, y2], r)
    rval[1] = np.dot([x2, y2], r)
    rval[2] = np.dot([x2, y1], r)
    rval[3] = np.dot([x1, y1], r)

    return rval


def get_rotation_info(rect_point):
    sorted_box = []
    for point in rect_point:
        sorted_box.append(list(point))

    sorted_box.sort()

    top_left = np.array(sorted_box[0])
    top_right = np.array(sorted_box[2])
    bottom_right = np.array(sorted_box[3])
    vertex = np.array([top_right[0], top_left[1]])

    diag_len = np.linalg.norm(top_right - top_left)
    hori_len = np.linalg.norm(vertex - top_left)
    angle = np.rad2deg(math.acos(hori_len / diag_len))

    center = np.round_((top_left + bottom_right) / 2)
    center = [int(center[0]), int(center[1])]

    return angle, center


def get_bounding_box(contour):
    min_y = round(np.min(contour[:, 0]))
    max_y = round(np.max(contour[:, 0]))
    min_x = round(np.min(contour[:, 1]))
    max_x = round(np.max(contour[:, 1]))

    return [min_y, max_y, min_x, max_x]


if __name__ == "__main__":
    pass
