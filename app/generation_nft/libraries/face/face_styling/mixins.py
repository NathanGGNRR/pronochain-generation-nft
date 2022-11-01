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

File: app/generation_nft/libraries/face/face_styling/mixins.py
"""
import os
import warnings

import cv2 as open_cv
import numpy as np
from coloraide import Color
from PIL import Image
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg

from app import logger
from app.exceptions import PronochainException
from app.generation_nft.libraries.face.face_styling.constants import TEMP_PATH
from app.generation_nft.utils import (
    draw_contours,
    multiply_array,
    replace_color,
    replace_color_not_equal,
)

warnings.filterwarnings("ignore")


class DrawingMixin(object):
    """Classe des mixins pour dessiner."""

    def __init__(self):
        """Initialise la classe des mixins pour dessiner."""
        pass

    def convert_to_pil_with_transparent_background(
        self, part: np.array, convert: bool = True
    ) -> Image:
        """Converti une image en image pil avec un fond transparent.

        Args:
            part (np.array): partie à convertir.
            convert (bool, optional): converti le format de la couleur ? Défaut à True.

        Returns:
            Image: image pil.
        """
        part = open_cv.cvtColor(
            part, open_cv.COLOR_BGR2RGBA if convert else open_cv.COLOR_RGB2RGBA
        )
        part[
            np.all(
                [part[:, :, 0] == 255, part[:, :, 1] == 255, part[:, :, 2] == 255],
                axis=0,
            )
        ] = np.array([255, 255, 255, 0])
        return Image.fromarray(part.astype("uint8"), "RGBA")

    def get_coordinates_from_list(
        self,
        image: np.array,
        landmarks: list,
        face_part: list,
        scale: bool = True,
        is_dict: bool = False,
    ) -> np.array:
        """Récupère les coordonnées d'une partie du visage souhaitée.

        Args:
            image (np.array): image.
            landmarks (list): liste des landmarks de la partie du visage.
            face_part (list): liste des points correspondant à la partie souhaitée.
            scale (bool, optional): détermine si l'on souhaite la coordonnées remise à l'échelle par rapport à l'image. Défaut à True.
            is_dict (bool, optional): est un dictionnaire ? Défaut à False.

        Returns:
            np.array: liste des coordonnées [[x, y]].
        """
        shape = image.shape
        points = np.zeros((len(face_part), 2), dtype="int")
        for index, landmark in enumerate([landmarks[i] for i in face_part]):
            landmark_x = landmark.get("x") if is_dict else landmark.x
            landmark_y = landmark.get("y") if is_dict else landmark.y
            x = round(landmark_x * shape[1]) if scale else int(landmark_x)
            y = round(landmark_y * shape[0]) if scale else int(landmark_y)
            points[index] = (x, y)
        return points

    def get_coordinate_from_point(
        self,
        landmarks: list,
        point: int,
        coordinate: str,
        scale_value: int = None,
    ) -> float:
        """Récupère la coordonnée "coordinate" (x, y ou z) d'un point.

        Args:
            landmarks (list): liste des landmarks de la partie du visage.
            point (int): index correspondant au point souhaité.
            coordinate (str): la coordonnée que l'on souhaite.
            scale_value (int, optional): image pour remettre à l'échelle. Défaut à None.

        Returns:
            float: "coordinate" (x, y ou z) coordonnée.
        """
        return (
            round(getattr(landmarks[point], coordinate) * scale_value)
            if scale_value is not None
            else getattr(landmarks[point], coordinate)
        )

    def get_coordinates_from_points(
        self,
        landmarks: list,
        points: list,
        coordinates: list,
        scale: bool = True,
        image: np.array = None,
        inverted_y: bool = False,
    ) -> np.array:
        """Récupère la/les coordonnées d'un ou plusieurs points (x, y et/ou z).

        Args:

            landmarks (list): liste des landmarks de la partie du visage.
            points (list): index correspondant aux points souhaités.
            coordinates (list): la/les coordonnées que l'on souhaite (x, y et/ou z).
            scale (bool, optional): détermine si l'on souhaite la coordonnées remise à l'échelle par rapport à l'image. Défaut à True.
            image (np.array, optional): image pour remettre à l'échelle. Défaut à None.
            inverted_y (bool): inverse la valeur de y (en pixel le haut est plus faible que le bas). Défaut à False.

        Returns:
            np.array: liste de coordonnées des points souhaitées.
        """
        coordinates_points = []
        for point in points:
            landmark = landmarks[point]
            landmark_coordinates = []
            for coordinate in coordinates:
                coordinate_value = getattr(landmark, coordinate)
                if coordinate == "x":
                    coordinate_value = (
                        round(coordinate_value * image.shape[1])
                        if scale
                        else coordinate_value
                    )
                elif coordinate == "y":
                    if scale:
                        coordinate_value = round(coordinate_value * image.shape[0])
                    elif inverted_y:
                        coordinate_value = -coordinate_value

                landmark_coordinates.append(coordinate_value)
            coordinates_points.append(landmark_coordinates)
        return np.array(coordinates_points)

    def clean_to_skin_color(
        self,
        visual_mask_part: np.array,
        contour: list,
        cleaned_face: np.array,
        offset_y: int,
        coordinates: tuple,
        face_shape: tuple,
        **_,
    ) -> np.array:
        """Supprime les couleurs de peau sur une partie du visage.

        Args:
            visual_mask_part (np.array): mask.
            contour (list): contour.
            cleaned_face (np.array): visage nettoyé.
            offset_y (int): coordonné y.
            coordinates (tuple): coordonnées.
            face_shape (tuple): forme du visage.

        Returns:
            np.array: mask nettoyé.
        """
        visual_mask_part_copy = visual_mask_part.copy()
        replace_color(
            visual_mask_part_copy, np.array([0, 0, 0]), np.array([254, 254, 254])
        )

        if offset_y is not None:
            (
                y_top,
                y_bottom,
                x_left,
                x_right,
            ) = coordinates
            visual_mask_part_copy = self.resize_natif(
                visual_mask_part_copy, face_shape, x_left, y_top
            )
            open_cv.drawContours(
                visual_mask_part_copy, contour, -1, (254, 254, 254), offset_y
            )
            visual_mask_part_copy = visual_mask_part_copy[
                y_top:y_bottom, x_left:x_right
            ]

        mask_pil = self.convert_to_pil_with_transparent_background(
            visual_mask_part_copy
        )
        mask_part_pil = Image.fromarray(
            open_cv.cvtColor(cleaned_face, open_cv.COLOR_BGR2RGBA).astype("uint8"),
            "RGBA",
        )
        mask_part_pil.paste(mask_pil, (0, 0), mask_pil)
        return open_cv.cvtColor(np.array(mask_part_pil), open_cv.COLOR_RGBA2BGR)

    def resize_natif(
        self, mask_part: np.array, face_shape: tuple, x_left: int, y_top: int
    ) -> np.array:
        """Redimensionne le visage.

        Args:
            mask_part (np.array): mask.
            face_shape (tuple): forme du visage.
            x_left (int): coordonné x.
            y_top (int): coordonné y.

        Returns:
            np.array: visage redimensionné.
        """
        virgin_mask_part = np.full(
            (face_shape[0], face_shape[1], 3),
            255,
            dtype=np.uint8,
        )
        mask_pil = self.convert_to_pil_with_transparent_background(mask_part)
        mask_part_pil = Image.fromarray(
            open_cv.cvtColor(virgin_mask_part, open_cv.COLOR_BGR2RGBA).astype("uint8"),
            "RGBA",
        )
        mask_part_pil.paste(mask_pil, (x_left, y_top), mask_pil)
        return open_cv.cvtColor(np.array(mask_part_pil), open_cv.COLOR_RGBA2BGR)

    def draw_line_contours(
        self,
        name: str,
        mask_part: np.array,
        parts: list,
        landmarks: list,
        close: bool = True,
    ) -> tuple:
        """Dessine la ligne de contour.

        Args:
            name (str): nom.
            mask_part (np.array): mask.
            parts (list): partie du visage.
            landmarks (list): coordonnées des parties du visage.
            close (bool, optional): contour fermé ? Défaut à True.

        Returns:
            tuple: mask part et contour.
        """
        start = f'<svg xmlns="http://www.w3.org/2000/svg" width="{mask_part.shape[1]}" height="{mask_part.shape[0]}"><path fill="#FFFFFF" d="M0 0 H{mask_part.shape[1]} V{mask_part.shape[0]} H 0 Z"/>'
        end = "</svg>"
        drawing_path = ""

        for index, part in enumerate(parts):
            first_point_y, first_point_x = landmarks[part].get("y"), landmarks[
                part
            ].get("x")
            if index == 0:
                drawing_path += f"M {first_point_x} {first_point_y} "
            else:
                drawing_path += f"L {first_point_x} {first_point_y} "
        if close:
            drawing_path += "Z"
        path = f'<path fill="transparent" stroke="#000000" stroke-linecap="round" stroke-linejoin="round" d="{drawing_path}"/>'

        svg_content = f"{start}{path}{end}"
        temp_svg_path = f"{TEMP_PATH}/svg/{name}.svg"
        temp_png_path = f"{TEMP_PATH}/png/{name}.png"
        with open(temp_svg_path, "w") as f:
            f.write(svg_content)

        drawing = svg2rlg(temp_svg_path)
        renderPM.drawToFile(drawing, temp_png_path, fmt="PNG")
        new_mask_part = open_cv.imread(temp_png_path, open_cv.IMREAD_UNCHANGED)
        replace_color_not_equal(
            new_mask_part, np.array([255, 255, 255]), np.array([0, 0, 0])
        )

        os.remove(temp_svg_path)
        os.remove(temp_png_path)

        return draw_contours(
            new_mask_part, new_mask_part, self.real_black_color, thickness_contour=1
        )

    def line_intersection(self, first_line: list, second_line: list) -> tuple:
        """Recupère les coordonnées du point d'intersection de deux lignes.

        Args:
            first_line (list): première ligne.
            second_line (list): deuxième ligne.

        Raises:
            PronochainException: les lignes ne se croisent pas.

        Returns:
            tuple: coordonnées x et y du point d'intersection.
        """
        xdiff = (
            first_line[0][0] - first_line[1][0],
            second_line[0][0] - second_line[1][0],
        )
        ydiff = (
            first_line[0][1] - first_line[1][1],
            second_line[0][1] - second_line[1][1],
        )

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
            raise PronochainException("Les deux lignes ne se croisent pas.")

        d = (det(*first_line), det(*second_line))
        x, y = det(d, xdiff) / div, det(d, ydiff) / div
        return int(round(x)), int(round(y))

    def add_color(self, landmark: dict, color: np.array):
        """Ajout de la propriété color pour une coordonnée d'un point du visage.

        Args:
            landmark (dict): coordonnées des parties du visage.
            color (np.array): couleur.
        """
        landmark["color"] = color

    def get_longest_contour(
        self, contours: np.array, return_indices: bool = False
    ) -> np.array:
        """Récupère le plus long contour.

        Args:
            contours (np.array): liste de contours.
            return_indices (bool, optional): retourne les coordonnées ? Défaut à False.

        Returns:
            np.array: contours.
        """
        length_contours = [len(contour) for contour in contours]
        length_longest = max(length_contours)
        indices = np.where(np.array(length_contours) == length_longest)
        return (
            indices
            if return_indices
            else np.array(
                [contour for index, contour in enumerate(contours) if index in indices]
            )
        )

    def remove_lowest_contour(self, contours: np.array, length_min: int) -> np.array:
        """Supprime le plus petit contour.

        Args:
            contours (np.array): liste de contours.
            length_min (int): taille minimum du contour.

        Returns:
            np.array: contours.
        """
        length_contours = np.array([len(contour) for contour in contours])
        indices = np.where(length_contours > length_min)
        return np.array(
            [contour for index, contour in enumerate(contours) if index in indices[0]]
        )

    def superpose_parts(
        self, mask_part_pil: Image, parts: list, mask_part_name: str
    ) -> Image:
        """Superpose les parties du visage.

        Args:
            mask_part_pil (Image): mask.
            parts (list): parties du visage.
            mask_part_name (str): mask name.

        Returns:
            Image: image superposée.
        """
        for part in parts:
            part = part.get(mask_part_name)
            part = self.convert_to_pil_with_transparent_background(part)
            mask_part_pil.paste(part, (0, 0), part)
        return mask_part_pil

    def exclude_extern_pixel(
        self, mask_part: np.array, exclude_color: np.array, contour: list
    ) -> np.array:
        """Supprime les couleurs en dehos des contours.

        Args:
            mask_part (np.array): mask.
            exclude_color (np.array): couleur à supprimer.
            contour (list): contour.

        Returns:
            np.array: mask.
        """
        indices = np.where(
            np.all(
                [
                    mask_part[:, :, 0] != exclude_color[0],
                    mask_part[:, :, 1] != exclude_color[1],
                    mask_part[:, :, 2] != exclude_color[2],
                ],
                axis=0,
            )
        )
        points = zip(indices[0], indices[1])
        for point in points:
            if (
                open_cv.pointPolygonTest(
                    contour[0], (int(point[1]), int(point[0])), True
                )
                < 0
            ):
                mask_part[point[0], point[1]] = np.array([255, 255, 255])
        return mask_part

    def fill_missing_pixels(
        self, mask_part: np.array, missing_color: tuple
    ) -> np.array:
        """Rempli les pixels avec les couleurs proches.

        Args:
            mask_part (np.array): mask.
            missing_color (tuple): couleur à remplacer.

        Returns:
            np.array: mask rempli.
        """
        points = np.where(
            np.all(
                [
                    mask_part[:, :, 0] == missing_color[0],
                    mask_part[:, :, 1] == missing_color[1],
                    mask_part[:, :, 2] == missing_color[2],
                ],
                axis=0,
            )
        )
        missing_points = list(zip(points[0], points[1]))
        missing_points = [missing_points, missing_points[::-1]]
        for points in missing_points:
            for point in points:
                y, x = point[0], point[1]
                mean_b, mean_g, mean_r, pixel_nomber = 0, 0, 0, 0

                new_x = x - 1
                new_x_b, new_x_g, new_x_r = (
                    mask_part[y, new_x][0],
                    mask_part[y, new_x][1],
                    mask_part[y, new_x][2],
                )
                if (
                    new_x > 0
                    and (
                        new_x_b != missing_color[0]
                        or new_x_g != missing_color[1]
                        or new_x_r != missing_color[2]
                    )
                    and (new_x_b != 255 or new_x_g != 255 or new_x_r != 255)
                ):
                    mean_b += mask_part[y, new_x][0]
                    mean_g += mask_part[y, new_x][1]
                    mean_r += mask_part[y, new_x][2]
                    pixel_nomber += 1

                new_x = x + 1
                new_x_b, new_x_g, new_x_r = (
                    mask_part[y, new_x][0],
                    mask_part[y, new_x][1],
                    mask_part[y, new_x][2],
                )
                if (
                    new_x < mask_part.shape[1] - 1
                    and (
                        new_x_b != missing_color[0]
                        or new_x_g != missing_color[1]
                        or new_x_r != missing_color[2]
                    )
                    and (new_x_b != 255 or new_x_g != 255 or new_x_r != 255)
                ):
                    mean_b += mask_part[y, new_x][0]
                    mean_g += mask_part[y, new_x][1]
                    mean_r += mask_part[y, new_x][2]
                    pixel_nomber += 1

                new_y = y - 1
                new_y_b, new_y_g, new_y_r = (
                    mask_part[new_y, x][0],
                    mask_part[new_y, x][1],
                    mask_part[new_y, x][2],
                )
                if (
                    new_y > 0
                    and (
                        new_y_b != missing_color[0]
                        or new_y_g != missing_color[1]
                        or new_y_r != missing_color[2]
                    )
                    and (new_y_b != 255 or new_y_g != 255 or new_y_r != 255)
                ):
                    mean_b += mask_part[new_y, x][0]
                    mean_g += mask_part[new_y, x][1]
                    mean_r += mask_part[new_y, x][2]
                    pixel_nomber += 1

                new_y = y + 1
                new_y_b, new_y_g, new_y_r = (
                    mask_part[new_y, x][0],
                    mask_part[new_y, x][1],
                    mask_part[new_y, x][2],
                )
                if (
                    new_y < mask_part.shape[0] - 1
                    and (
                        new_y_b != missing_color[0]
                        or new_y_g != missing_color[1]
                        or new_y_r != missing_color[2]
                    )
                    and (new_y_b != 255 or new_y_g != 255 or new_y_r != 255)
                ):
                    mean_b += mask_part[new_y, x][0]
                    mean_g += mask_part[new_y, x][1]
                    mean_r += mask_part[new_y, x][2]
                    pixel_nomber += 1

                if pixel_nomber:
                    mask_part[y, x] = np.array(
                        [
                            int(round(mean_b / pixel_nomber)),
                            int(round(mean_g / pixel_nomber)),
                            int(round(mean_r / pixel_nomber)),
                        ]
                    )
        return mask_part

    def keep_inside(self, part: np.array, contours: list):
        """Supprime les couleurs en dehors de la zone souhaitée.

        Args:
            part (np.array): image entière.
            contours (list): contours.
        """
        for y in range(part.shape[0]):
            for x in range(part.shape[1]):
                if not np.all(part[y, x] == 255) and all(
                    open_cv.pointPolygonTest(contour[0], (x, y), True) < 0
                    for contour in contours
                ):
                    part[y, x] = np.array([255, 255, 255])

    def keep_inside_contour(
        self, part: np.array, contour: list, replace_white_color: np.array = None
    ) -> np.array:
        """Supprime les couleurs en dehors de la zone souhaitée.

        Args:
            part (np.array): image entière.
            contours (list): contours.
            replace_white_color (np.array, optional): remplace par du blanc ? Défaut à None.

        Returns:
            np.array: image.
        """
        for y in range(part.shape[0]):
            for x in range(part.shape[1]):
                if (
                    not np.all(part[y, x] == 255)
                    and open_cv.pointPolygonTest(contour, (x, y), True) < 0
                ):
                    if not np.all(part[y, x] == 255):
                        part[y, x] = np.array([255, 255, 255])
                elif (
                    replace_white_color is not None
                    and np.all(part[y, x] == 255)
                    and open_cv.pointPolygonTest(contour, (x, y), True) > 0
                ):
                    part[y, x] = replace_white_color

        return part

    def keep_precision_inside(
        self,
        part: np.array,
        x_left: int,
        x_right: int,
        y_top: int,
        y_bottom: int,
        contour: np.array,
    ) -> np.array:
        """Supprime les couleurs en dehors de la zone souhaitée.

        Args:
            part (np.array): image entière.
            x_left (int): x gauche.
            x_right (int): x droite.
            y_top (int): y haut.
            y_bottom (int): y bas.
            contour (np.array): contour.

        Returns:
            np.array: image.
        """
        for y in range(y_top - 10, y_bottom + 10):
            for x in range(x_left - 10, x_right + 10):
                if (
                    not np.all(part[y, x] == 255)
                    and open_cv.pointPolygonTest(contour, (x, y), True) < 0
                ):
                    part[y, x] = np.array([255, 255, 255])
        return part

    def set_colors(
        self,
        landmarks_points: list,
        lighter_color: str,
        darker_color: str,
        with_index: bool = False,
        progress: float = 1.0,
    ) -> tuple:
        """Ajoute les couleurs.

        Args:
            landmarks_points (list): coordonnées des parties du visages.
            lighter_color (str): couleur claire.
            darker_color (str): couleur sombre.
            with_index (bool, optional): avec index ? Défaut à False.
            progress (float, optional): progressif ? Défaut à 1.0.

        Returns:
            tuple: coordonnées des parties du visages, couleur sombre et claire.
        """
        z_values = sorted(
            list(
                set(
                    list(
                        map(
                            lambda landmark: landmark.get("info").get("z")
                            if with_index
                            else landmark.get("z"),
                            landmarks_points,
                        )
                    )
                )
            )
        )
        z_values_length = len(z_values)

        gradients_colors = Color(lighter_color).steps(
            Color(darker_color), steps=z_values_length, progress=lambda t: t * progress
        )

        rgb_colors = []
        for gradients_color in gradients_colors:
            colors = (
                gradients_color.to_string(precision=0)
                .replace("rgb(", "")
                .replace(")", "")
                .split(" ")
            )
            rgb_colors.append(
                np.array([int(colors[2]), int(colors[1]), int(colors[0])]).astype(
                    np.uint8
                )
            )

        for landmark_points in landmarks_points:
            get_index_z_value = z_values.index(
                landmark_points.get("info").get("z")
                if with_index
                else landmark_points.get("z")
            )
            if with_index:
                landmark_points["info"]["color"] = rgb_colors[get_index_z_value]
            else:
                landmark_points["color"] = rgb_colors[get_index_z_value]
        return landmarks_points, rgb_colors[0], rgb_colors[-1]

    def draw_gradient_triangle(
        self,
        mask_part: np.array,
        landmarks: dict,
        points: list,
        check_contour: dict = None,
        with_index: bool = False,
    ) -> np.array:
        """Dessine un dégradé.

        Args:
            mask_part (np.array): mask.
            landmarks (dict): coordonnées des parties du visage.
            points (list): points du visages.
            check_contour (dict, optional): vérifie les contours ? Défaut à None.
            with_index (bool, optional): avec index ? Défaut à False.

        Returns:
            np.array: mask avec le dégradé.
        """
        for point in points:
            if with_index:
                try:
                    first_landmark = next(
                        landmark.get("info")
                        for landmark in landmarks
                        if landmark.get("index") == point[0]
                    )
                    second_landmark = next(
                        landmark.get("info")
                        for landmark in landmarks
                        if landmark.get("index") == point[1]
                    )
                    third_landmark = next(
                        landmark.get("info")
                        for landmark in landmarks
                        if landmark.get("index") == point[2]
                    )
                except IndexError:
                    logger.error(
                        f"L'un des index est trop élévé : {point[0]} {point[1]} {point[2]}"
                    )
            else:
                try:
                    first_landmark, second_landmark, third_landmark = (
                        landmarks[point[0]],
                        landmarks[point[1]],
                        landmarks[point[2]],
                    )
                except IndexError:
                    logger.error(
                        f"L'un des index est trop élévé : {point[0]} {point[1]} {point[2]}"
                    )
            first_point_x, first_point_y = first_landmark.get("x"), first_landmark.get(
                "y"
            )
            second_point_x, second_point_y = second_landmark.get(
                "x"
            ), second_landmark.get("y")
            third_point_x, third_point_y = third_landmark.get("x"), third_landmark.get(
                "y"
            )
            first_point, first_color = (
                first_point_x,
                first_point_y,
            ), first_landmark.get("color")
            second_point, second_color = (
                second_point_x,
                second_point_y,
            ), second_landmark.get("color")
            third_point, third_color = (
                third_point_x,
                third_point_y,
            ), third_landmark.get("color")

            triangle_array = np.asarray(
                [
                    first_point[0],
                    second_point[0],
                    third_point[0],
                    first_point[1],
                    second_point[1],
                    third_point[1],
                    1,
                    1,
                    1,
                ]
            ).reshape((3, 3))

            x_left, x_right = min(first_point[0], second_point[0], third_point[0]), max(
                first_point[0], second_point[0], third_point[0]
            )
            y_top, y_bottom = min(first_point[1], second_point[1], third_point[1]), max(
                first_point[1], second_point[1], third_point[1]
            )

            x_range, y_range = range(x_left, x_right), range(y_top, y_bottom)
            xv, yv = np.meshgrid(x_range, y_range)
            xv, yv = xv.flatten(), yv.flatten()

            alphas, betas, gammas = np.linalg.lstsq(
                triangle_array, np.array([xv, yv, [1] * len(xv)]), rcond=-1
            )[0]

            mask = (alphas > 0) & (betas > 0) & (gammas > 0)
            alphas_m, betas_m, gammas_m = alphas[mask], betas[mask], gammas[mask]
            xv_m, yv_m = xv[mask], yv[mask]

            try:
                colors = (
                    multiply_array(first_color, alphas_m)
                    + multiply_array(second_color, betas_m)
                    + multiply_array(third_color, gammas_m)
                )
                mask_part[yv_m, xv_m] = colors
            except TypeError:
                logger.error(
                    f"La couleur d'un des trois points n'est pas défini. Premier point {point[0]} : {first_color}, Deuxième point {point[1]} : {second_color}, Troisième point {point[2]} : {third_color}"
                )
            except IndexError:
                logger.error(
                    f"Un problème est survenue pour l'affectation du dégradé des ces trois points : {point[0]} {point[1]} {point[2]}"
                )

            if check_contour is not None and (
                open_cv.pointPolygonTest(
                    check_contour, (np.float32(x_left), np.float32(y_top)), True
                )
                < 0
                or open_cv.pointPolygonTest(
                    check_contour, (np.float32(x_right), np.float32(y_bottom)), True
                )
                < 0
            ):
                for y in range(y_top, y_bottom):
                    for x in range(x_left, x_right):
                        if open_cv.pointPolygonTest(check_contour, (x, y), True) < 0:
                            mask_part[y, x] = np.array([255, 255, 255])

        return mask_part
