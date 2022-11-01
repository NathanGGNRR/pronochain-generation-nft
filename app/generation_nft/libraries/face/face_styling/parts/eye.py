# -*- coding: utf-8 -*-
r"""
.-----------------------------------------------------.

______                           _           _
| ___ \                         | |         (_)
| |_/ / __ ___  _ __   ___   ___| |__   __ _ _ _ __
|  __/ '__/ _ \| '_ \ / _ \ / __| '_ \ / _` | | '_ \
| |  | | | (_) | | | | (_) | (__| | | | (_| | | | | |
\_|  |_|  \___/|_| |_|\___/ \___|_| |_|\__,_|_|_| |_|


.-----------------------------------------------------.

 _____                           _   _               _   _ ______ _____
|  __ \                         | | (_)             | \ | ||  ___|_   _|
| |  \/ ___ _ __   ___ _ __ __ _| |_ _  ___  _ __   |  \| || |_    | |
| | __ / _ \ '_ \ / _ \ '__/ _` | __| |/ _ \| '_ \  | . ` ||  _|   | |
| |_\ \  __/ | | |  __/ | | (_| | |_| | (_) | | | | | |\  || |     | |
 \____/\___|_| |_|\___|_|  \__,_|\__|_|\___/|_| |_| \_| \_/\_|     \_/


.------------------------------------------------------------------------.

File: app/generation_nft/libraries/face/face_styling/parts/eye.py
"""
import math
import warnings

import cv2 as open_cv
import numpy as np
from PIL import Image

from app.generation_nft.libraries.face.face_styling.constants import (
    IRIS_CENTER_POINT,
    IRIS_RADIAL,
)
from app.generation_nft.utils import (
    draw_contours,
    get_shade_color,
    replace_color,
    where,
)

warnings.filterwarnings("ignore")


class EyeDrawing(object):
    """Classe pour styliser les yeux."""

    def __init__(self):
        """Initialise la classe du style pour les yeux."""
        pass

    def set_iris(
        self, new_contour_depend_mask: np.array, landmarks: list, iris_landmarks: list
    ) -> tuple:
        """Dessine le style de l'iris des yeux.

        Args:
            new_contour_depend_mask (np.array): mask de la partie dont dépend les iris.
            landmarks (list): coordonnées des parties du visage.
            iris_landmarks (list): coordonnées des points des iris.

        Returns:
            tuple: iris et coordonnée du centre le l'iris.
        """
        iris_mask = np.full(
            (new_contour_depend_mask.shape[0], new_contour_depend_mask.shape[1], 3),
            255,
            dtype=np.uint8,
        )
        virgin_iris_mask = np.full(
            (new_contour_depend_mask.shape[0], new_contour_depend_mask.shape[1], 1),
            0,
            dtype=np.uint8,
        )

        first_landmark, second_landmark, third_landmark, fourth_landmark = (
            landmarks[iris_landmarks[0]],
            landmarks[iris_landmarks[1]],
            landmarks[iris_landmarks[2]],
            landmarks[iris_landmarks[3]],
        )
        first_point, second_point, third_point, fourth_point = (
            (first_landmark.get("x"), first_landmark.get("y")),
            (second_landmark.get("x"), second_landmark.get("y")),
            (third_landmark.get("x"), third_landmark.get("y")),
            (fourth_landmark.get("x"), fourth_landmark.get("y")),
        )
        iris_center = self.line_intersection(
            [first_point, third_point], [second_point, fourth_point]
        )
        iris_radial = int(
            round(
                math.sqrt(
                    (third_point[0] - first_point[0]) ** 2
                    + (third_point[1] - first_point[1]) ** 2
                )
            )
            / 2
        )
        iris_radial_color = iris_radial - int((iris_radial * 0.5))
        open_cv.circle(
            virgin_iris_mask, iris_center, iris_radial_color, 1, open_cv.FILLED
        )

        if self.darker_eyes_color is None:
            self.darker_eyes_color = get_shade_color(self.eyes_color, 10)

        virgin_iris_mask = np.full(
            (new_contour_depend_mask.shape[0], new_contour_depend_mask.shape[1], 1),
            0,
            dtype=np.uint8,
        )

        open_cv.circle(virgin_iris_mask, iris_center, iris_radial, 1, open_cv.FILLED)

        percentage_radial = int(iris_radial * 0.5)
        gradient_center = (
            iris_center[0] + percentage_radial,
            iris_center[1] + percentage_radial,
        )

        self.add_color(first_landmark, self.eyes_color)
        self.add_color(second_landmark, self.darker_eyes_color)
        self.add_color(third_landmark, self.darker_eyes_color)
        self.add_color(fourth_landmark, self.eyes_color)

        gradient_landmarks = {
            "x": gradient_center[0],
            "y": gradient_center[1],
            "color": self.eyes_color,
        }

        iris_landmarks_points = [
            first_landmark,
            second_landmark,
            third_landmark,
            fourth_landmark,
            gradient_landmarks,
            {
                "x": first_landmark.get("x"),
                "y": second_landmark.get("y"),
                "color": self.darker_eyes_color,
            },
            {
                "x": third_landmark.get("x"),
                "y": second_landmark.get("y"),
                "color": self.darker_eyes_color,
            },
            {
                "x": third_landmark.get("x"),
                "y": fourth_landmark.get("y"),
                "color": self.darker_eyes_color,
            },
            {
                "x": first_landmark.get("x"),
                "y": fourth_landmark.get("y"),
                "color": self.eyes_color,
            },
        ]

        iris_points = [
            [0, 5, 1],
            [0, 4, 1],
            [1, 6, 2],
            [1, 4, 2],
            [2, 4, 3],
            [2, 3, 7],
            [3, 4, 8],
            [4, 8, 0],
        ]

        open_cv.circle(
            iris_mask, iris_center, iris_radial, self.black_color, open_cv.FILLED
        )

        iris_mask = self.draw_gradient_triangle(
            iris_mask, iris_landmarks_points, iris_points
        )
        iris_mask = self.fill_missing_pixels(iris_mask, self.black_color)
        iris_mask_part = open_cv.bitwise_and(
            iris_mask, iris_mask, mask=virgin_iris_mask
        )
        replace_color(iris_mask_part, self.real_black_color, self.white_color)

        open_cv.circle(
            iris_mask_part,
            iris_center,
            iris_radial,
            self.black_color,
            1,
            open_cv.LINE_AA,
        )

        iris_pil = Image.fromarray(self.iris_picture.astype("uint8"), "RGBA")

        iris_img_radial = IRIS_RADIAL
        iris_img_center_point = IRIS_CENTER_POINT
        iris_width_radial = iris_radial * 0.5
        percentage_downscale = iris_width_radial * 100 / iris_img_radial

        iris_center_point = (
            int(math.ceil(percentage_downscale * iris_img_center_point[1] / 100)),
            int(math.ceil(percentage_downscale * iris_img_center_point[0] / 100)),
        )

        width = int(math.ceil(percentage_downscale * self.iris_picture.shape[1] / 100))
        height = int(math.ceil(percentage_downscale * self.iris_picture.shape[0] / 100))

        iris_pil = iris_pil.resize((width, height))

        y_less, x_less = height - iris_center_point[0], width - iris_center_point[1]
        iris_x, iris_y = iris_center[0] - x_less, iris_center[1] - y_less

        iris_mask_part = open_cv.cvtColor(iris_mask_part, open_cv.COLOR_BGR2RGBA)
        mask_part_pil = Image.fromarray(iris_mask_part.astype("uint8"), "RGBA")
        mask_part_pil.paste(iris_pil, (iris_x, iris_y), iris_pil)

        return (
            open_cv.cvtColor(np.array(mask_part_pil), open_cv.COLOR_RGBA2BGR),
            iris_center,
        )

    def draw_iris(
        self,
        new_contour_depend_mask: np.array,
        landmarks: list,
        iris_landmarks: list,
        new_face_minimize: np.array,
        contour_depend_on: list,
        middle_eye_x: int,
        middle_eye_y: int,
    ) -> np.array:
        """Dessine les iris sur les yeux.

        Args:
            new_contour_depend_mask (np.array): mask de la partie dont dépend les iris.
            landmarks (list): coordonnées des parties du visage.
            iris_landmarks (list): coordonnées des points des iris.
            new_face_minimize (np.array): visage.
            contour_depend_on (list): contour de la partie dont dépend les iris.
            middle_eye_x (int): coordonnée du center x.
            middle_eye_y (int): coordonnée du center y.

        Returns:
            np.array: iris.
        """
        iris_mask_part, iris_center = self.set_iris(
            new_contour_depend_mask, landmarks, iris_landmarks
        )
        translation_x = np.float32([[1, 0, middle_eye_x - iris_center[0]], [0, 1, 0]])
        translation_y = np.float32([[1, 0, 0], [0, 1, middle_eye_y - iris_center[1]]])
        iris_mask_translation = open_cv.warpAffine(
            iris_mask_part,
            translation_x,
            (iris_mask_part.shape[0], iris_mask_part.shape[1]),
        )
        iris_mask_translation = open_cv.warpAffine(
            iris_mask_translation,
            translation_y,
            (iris_mask_part.shape[0], iris_mask_part.shape[1]),
        )
        iris_mask_part = self.exclude_extern_pixel(
            iris_mask_translation, np.array([255, 255, 255]), contour_depend_on
        )

        mask_pil = self.convert_to_pil_with_transparent_background(iris_mask_part)
        mask_part_pil = Image.fromarray(
            open_cv.cvtColor(new_face_minimize, open_cv.COLOR_BGR2RGBA).astype("uint8"),
            "RGBA",
        )
        mask_part_pil.paste(mask_pil, (0, 0), mask_pil)

        return open_cv.cvtColor(np.array(mask_part_pil), open_cv.COLOR_RGBA2BGR)

    def draw_eye(
        self,
        name: str,
        new_face_minimize: np.array,
        landmarks: list,
        contour_depend_mask: np.array,
        contour_depend_on: list,
        parts: list,
        coordinates: tuple,
        face_shape: tuple,
        **_
    ) -> np.array:
        """Dessine les yeux.

        Args:
            name (str): name.
            new_face_minimize (np.array): visage.
            landmarks (list): coordonnées des parties du visage.
            contour_depend_mask (np.array): mask de la partie dont dépend les yeux.
            contour_depend_on (list): contour de la partie dont dépend les yeux.
            parts (list): parties du visage.
            coordinates (tuple): coordonnées.
            face_shape (tuple): forme du visage.

        Returns:
            np.array: un oeil.
        """
        new_contour_depend_mask = contour_depend_mask.copy()
        copy_face_minimize = new_face_minimize.copy()

        eye_landmarks = list(landmarks).copy()

        middle_eye_x = eye_landmarks[parts[4]].get("x") + int(
            (eye_landmarks[parts[-1]].get("x") - eye_landmarks[parts[4]].get("x")) / 2
        )

        virgin_mask_part = np.full(
            (face_shape[0], face_shape[1], 3),
            255,
            dtype=np.uint8,
        )
        virgin_eyelid_part = virgin_mask_part.copy()

        (
            y_top,
            y_bottom,
            x_left,
            x_right,
        ) = coordinates
        copy_face_minimize = self.resize_natif(
            copy_face_minimize, face_shape, x_left, y_top
        )
        mask_part = self.resize_natif(
            new_contour_depend_mask, face_shape, x_left, y_top
        )

        _, eyelid_contours = self.draw_line_contours(
            name, virgin_eyelid_part, parts[3], eye_landmarks
        )
        open_cv.drawContours(
            copy_face_minimize,
            eyelid_contours,
            -1,
            (int(self.skin_color[0]), int(self.skin_color[1]), int(self.skin_color[2])),
            open_cv.FILLED,
        )

        virgin_up_eye_part = np.full(
            (face_shape[0], face_shape[1], 3),
            255,
            dtype=np.uint8,
        )
        eye_up_points_length = len(parts[1])
        for i in range(eye_up_points_length):
            next_i = i + 1
            if next_i > eye_up_points_length - 1:
                break
            first_point_x, first_point_y = eye_landmarks[parts[1][i]].get(
                "x"
            ), eye_landmarks[parts[1][i]].get("y")
            second_point_x, second_point_y = eye_landmarks[parts[1][next_i]].get(
                "x"
            ), eye_landmarks[parts[1][next_i]].get("y")
            open_cv.line(
                virgin_up_eye_part,
                (first_point_x, first_point_y),
                (second_point_x, second_point_y),
                self.black_color,
                1,
            )

        _, eye_up_contours = draw_contours(
            virgin_up_eye_part,
            virgin_up_eye_part,
            [self.black_color[0], self.black_color[1], self.black_color[2]],
            open_cv.FILLED,
        )
        open_cv.drawContours(
            copy_face_minimize, eye_up_contours, -1, self.black_color, 3, offset=(0, -3)
        )

        eyelid_up_contours = []
        for point in parts[2]:
            eyelid_up_contours.append(
                np.array([eye_landmarks[point].get("x"), eye_landmarks[point].get("y")])
            )

        eyelid_clean_contours = np.array(eyelid_up_contours).reshape((-1, 1, 2))
        open_cv.polylines(
            copy_face_minimize,
            [eyelid_clean_contours],
            False,
            self.black_color,
            1,
            open_cv.LINE_AA,
        )

        open_cv.drawContours(
            copy_face_minimize, contour_depend_on, -1, (253, 253, 253), open_cv.FILLED
        )
        _, coordinates_y, _ = where(copy_face_minimize, (253, 253, 253))
        min_y, max_y = min(coordinates_y), max(coordinates_y)
        middle_eye_y = min_y + int((max_y - min_y) / 2)
        replace_color(copy_face_minimize, (253, 253, 253), np.array([254, 254, 254]))

        iris_points = parts[0]
        copy_face_minimize = self.draw_iris(
            mask_part,
            eye_landmarks,
            iris_points,
            copy_face_minimize,
            contour_depend_on,
            middle_eye_x,
            middle_eye_y,
        )

        open_cv.drawContours(
            copy_face_minimize,
            contour_depend_on,
            -1,
            self.black_color,
            1,
            open_cv.LINE_AA,
        )

        return copy_face_minimize[y_top:y_bottom, x_left:x_right]
