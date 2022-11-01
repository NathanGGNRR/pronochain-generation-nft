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

File: app/generation_nft/utils.py
"""
import argparse
import math
from pathlib import Path
from typing import List, Optional, Tuple

import cv2 as open_cv
import numpy as np
from coloraide import Color
from mediapipe.python.solutions.drawing_utils import DrawingSpec
from scipy.interpolate import splev, splprep

from app.exceptions import PronochainException
from app.settings import settings


def setup_arguments() -> tuple:
    """Ajoutes les paramètres du script.

    Returns:
        tuple(Path, bool): chemin de l'image, lancé en mode test.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i",
        "--image",
        required=True,
        help="Nom de l'image. Le fichier doit se trouver dans le dossier tests/pictures.",
    )
    parser.add_argument(
        "-e",
        "--extension",
        required=True,
        choices={"png", "jpg", "jpeg"},
        help="Extension de l'image.",
    )
    parser.add_argument(
        "-o",
        "--onlyface",
        action="store_true",
        help="Récupère seulement le visage.",
    )
    parser.add_argument(
        "-t",
        "--test",
        action="store_true",
        help="Démarrer le script en mode test.",
    )

    args = parser.parse_args()
    file = Path(
        f"{settings.GENERATION_NFT_PATH}/tests/pictures/{args.image}.{args.extension}"
    )

    if not file.is_file():
        raise PronochainException("File does not found in tests/pictures !")
    else:
        return file, args.test, args.onlyface


def get_percentage(first_value: float, second_value: float) -> float:
    """Récupère le pourcentage entre deux valeurs.

    Args:
        first_value (float): première valeur.
        second_value (float): deuxième valeur.

    Returns:
        float: pourcentage.
    """
    return (
        second_value * 100 / first_value
        if first_value > second_value
        else first_value * 100 / second_value
    )


def get_mean(values: list) -> float:
    """Récupère la moyenne d'une liste.

    Args:
        values (list): liste de valeur.

    Returns:
        float: moyenne des valeurs dans la liste.
    """
    return sum(values) / len(values)


def set_positive(value: float) -> float:
    """Positive le nombre négatif souhaité.

    Args:
        value (float): valeur négative.

    Returns:
        float: valeur positive.
    """
    return math.sqrt(value**2)


def take_closest(value: int, collection: list) -> int:
    """Récupère la valeur de liste la plus proche de la valeur souhaitée.

    Args:
        num (int): valeur.
        collection (list): liste des valeurs.

    Returns:
        int: valeur la plus proche.
    """
    return min(collection, key=lambda x: abs(x - value))


def multiply_array(color: np.array, mask_colors: np.array) -> np.array:
    """Multiplie le masque et la couleur ensemble.

    Args:
        color (np.array): couleur.
        mask_colors (np.array): masque.

    Returns:
        np.array: masque et couleur multiplier
    """
    return np.asmatrix(mask_colors).T @ np.asmatrix(color)


def draw_contours(
    visual_mask_part: np.array,
    visual_mask_color_hsv: np.array,
    hsv_color: tuple,
    thickness_contour: int = 1,
    as_mask: bool = False,
    smooth: bool = False,
) -> tuple:
    """Dessine les contours.

    Args:
        visual_mask_part (np.array): visual mask part.
        visual_mask_color_hsv (np.array): visual mask color hsv.
        hsv_color (tuple): hsv color.
        thickness_contour (int, optional): épaisseur du contour. Défaut à 1.
        as_mask (bool, optional): en tant que mask ? Défaut à False.
        smooth (bool, optional): lissé ? Défaut à False.

    Returns:
        tuple: mask part et contour.
    """
    mask_color = open_cv.inRange(
        visual_mask_color_hsv, np.array(hsv_color), np.array(hsv_color)
    )

    contour, __builtins__ = open_cv.findContours(
        mask_color, open_cv.RETR_EXTERNAL, open_cv.CHAIN_APPROX_SIMPLE
    )

    if smooth:
        contour = smooth_contours(contour)

    default_color = 0 if as_mask else (255, 255, 255)
    mask_color = 1 if as_mask else (0, 0, 0)

    mask_part = np.full(
        (visual_mask_part.shape[0], visual_mask_part.shape[1], 1 if as_mask else 3),
        default_color,
        dtype=np.uint8,
    )
    open_cv.drawContours(mask_part, contour, -1, mask_color, thickness_contour)

    return mask_part, contour


def smooth_contours(contours: list) -> list:
    """Lisse les contours.

    Args:
        contours (list): contours.
        number_contours (int): nombre de points souhaité.

    Returns:
        list: contours lissés.
    """
    smooth_contours = []
    for contour in contours:
        x, y = contour.T
        x, y = x.tolist()[0], y.tolist()[0]
        tick, u = splprep([x, y], u=None, s=1.0, per=1)
        number_contours = int(round(len(contour) / 3))
        u_new = np.linspace(u.min(), u.max(), number_contours)
        x_new, y_new = splev(u_new, tick, der=0)
        res_array = [[[int(i[0]), int(i[1])]] for i in zip(x_new, y_new)]
        smooth_contours.append(np.asarray(res_array, dtype=np.int32))
    return smooth_contours


def get_angle(
    first_point: np.array, second_point: np.array, third_point: np.array
) -> int:
    """Récupère l'angle.

    Args:
        first_point (np.array): premier point.
        second_point (np.array): deuxième point.
        third_point (np.array): troisième point.

    Returns:
        int: angle.
    """
    ang = math.degrees(
        math.atan2(third_point[1] - second_point[1], third_point[0] - second_point[0])
        - math.atan2(first_point[1] - second_point[1], first_point[0] - second_point[0])
    )
    return int(round(ang + 360 if ang < 0 else ang))


def normalize_values(face: np.array, landmarks: list, with_index: bool = False) -> list:
    """Normalise les points du visage.

    Args:
        face (np.array): visage.
        landmarks (list): points du visage.
        with_index (bool, optional): avec index ? Défaut à False.

    Returns:
        list: liste de points du visage normalisée.
    """
    normalized_landmarks = []
    (height, width, _) = face.shape
    list_z = sorted(
        [
            getattr(landmark.get("info") if with_index else landmark, "z")
            for landmark in landmarks
        ]
    )
    min_z = list_z[0]
    for landmark in landmarks:
        landmark_info = landmark.get("info") if with_index else landmark
        x = int(round(getattr(landmark_info, "x") * width))
        y = int(round(getattr(landmark_info, "y") * height))
        z = round(((getattr(landmark_info, "z") - min_z) * 10), 2)
        normalized_landmarks.append(
            {"index": landmark.get("index"), "info": {"x": x, "y": y, "z": z}}
        ) if with_index else normalized_landmarks.append({"x": x, "y": y, "z": z})
    return normalized_landmarks


def rgb_to_hex(rgb: np.array, convert_bgr_to_rgb: bool = False) -> str:
    """Converti le RGB en HEX.

    Args:
        rgb (np.array): rgb.
        convert_bgr_to_rgb (bool, optional): converti le bgr en rgb ? Défaut à False.

    Returns:
        str: hex.
    """
    if convert_bgr_to_rgb:
        rgb = np.array([int(rgb[2]), int(rgb[1]), int(rgb[0])])
    hex_color = "#"
    for channel in rgb:
        hexa = ("{:X}").format(channel)
        if channel < 10 or len(hexa) < 2:
            hexa = f"0{hexa}"
        hex_color += hexa
    return hex_color


def replace_color(
    mask_to_replace: np.array,
    color_to_replace: tuple,
    replace_color: np.array,
    channel: int = 3,
):
    """Remplace une couleur.

    Args:
        mask_to_replace (np.array): mask d'origine.
        color_to_replace (tuple): couleur à remplacée.
        replace_color (np.array): couleur remplacante.
        channel (int, optional): dimension de la couleur. Défaut à 3.
    """
    if channel == 3:
        mask_to_replace[
            np.all(
                [
                    mask_to_replace[:, :, 0] == int(color_to_replace[0]),
                    mask_to_replace[:, :, 1] == int(color_to_replace[1]),
                    mask_to_replace[:, :, 2] == int(color_to_replace[2]),
                ],
                axis=0,
            )
        ] = replace_color
    elif channel == 4:
        mask_to_replace[
            np.all(
                [
                    mask_to_replace[:, :, 0] == int(color_to_replace[0]),
                    mask_to_replace[:, :, 1] == int(color_to_replace[1]),
                    mask_to_replace[:, :, 2] == int(color_to_replace[2]),
                    mask_to_replace[:, :, 3] == int(color_to_replace[3]),
                ],
                axis=0,
            )
        ] = replace_color
    elif channel == 1:
        mask_to_replace[
            np.all([mask_to_replace[:, :] == int(color_to_replace[0])], axis=0)
        ] = replace_color[0]


def replace_range_color(
    mask_to_replace: np.array,
    under_range: np.array,
    replace_color: np.array,
    under: bool = True,
):
    """Remplace une palette de couleur.

    Args:
        mask_to_replace (np.array): mask d'origine.
        under_range (np.array): palette de couleur.
        replace_color (np.array): couleur remplacante.
        under (bool, optional): en dessous ? Défaut à True.
    """
    if under:
        mask_to_replace[
            np.all(
                [
                    mask_to_replace[:, :, 0] < under_range,
                    mask_to_replace[:, :, 1] < under_range,
                    mask_to_replace[:, :, 2] < under_range,
                ],
                axis=0,
            )
        ] = replace_color
    else:
        mask_to_replace[
            np.all(
                [
                    mask_to_replace[:, :, 0] > under_range,
                    mask_to_replace[:, :, 1] > under_range,
                    mask_to_replace[:, :, 2] > under_range,
                ],
                axis=0,
            )
        ] = replace_color


def replace_color_not_equal(
    mask_to_replace: np.array,
    color_to_replace: np.array,
    replace_color: np.array,
    channel: int = 3,
):
    """Remplacer les couleurs non égales.

    Args:
        mask_to_replace (np.array): mask d'origine.
        color_to_replace (tuple): couleur à remplacée.
        replace_color (np.array): couleur remplacante.
        channel (int, optional): dimension de la couleur. Défaut à 3.
    """
    if channel == 3:
        mask_to_replace[
            np.any(
                [
                    mask_to_replace[:, :, 0] != int(color_to_replace[0]),
                    mask_to_replace[:, :, 1] != int(color_to_replace[1]),
                    mask_to_replace[:, :, 2] != int(color_to_replace[2]),
                ],
                axis=0,
            )
        ] = replace_color
    elif channel == 1:
        mask_to_replace[
            np.any([mask_to_replace[:, :] != int(color_to_replace[0])], axis=0)
        ] = replace_color[0]


def get_unique_colors(
    mask_part: np.array, channel: int = 3, with_frequency_count: bool = False
) -> list:
    """Récupère toutes les couleurs de façon unique.

    Args:
        mask_part (np.array): mask d'origine.
        channel (int, optional): dimension de la couleur. Défaut à 3.
        with_frequency_count (bool, optional): avec le calcul de la fréquence. Défaut à False.

    Returns:
        list: liste des couleurs.
    """
    if channel != 1:
        unique_colors = np.unique(
            mask_part.reshape(-1, mask_part.shape[2]),
            axis=0,
            return_counts=with_frequency_count,
        )
        if with_frequency_count:
            unique_colors = list(zip(unique_colors[0][:-1], unique_colors[1][:-1]))
        colors = []
        for unique_color in unique_colors:
            if with_frequency_count:
                color = {
                    "sum": np.sum(unique_color[0]),
                    "color": unique_color[0],
                    "count": unique_color[-1],
                }
            else:
                color = {"sum": np.sum(unique_color), "color": unique_color}
            colors.append(color)
        return (
            sorted(colors, key=lambda item: item["count"], reverse=True)
            if with_frequency_count
            else sorted(colors, key=lambda item: item["sum"])
        )
    else:
        unique_colors = np.unique(mask_part, return_counts=with_frequency_count)
        if with_frequency_count:
            unique_colors = list(zip(unique_colors[0][:-1], unique_colors[1][:-1]))
        colors = []
        for unique_color in unique_colors:
            if with_frequency_count:
                color = {"color": unique_color[0], "count": unique_color[-1]}
            else:
                color = {"color": unique_color}
            colors.append(color)
        return (
            sorted(colors, key=lambda item: item["count"], reverse=True)
            if with_frequency_count
            else colors
        )


def get_roi(part: np.array, color: tuple, is_equal: bool = True) -> tuple:
    """Récupère une zone.

    Args:
        part (np.array): mask d'origine.
        color (tuple): couleur.
        is_equal (bool, optional): est égale ? Défaut à True.

    Returns:
        tuple: x_left, x_top, y_right, y_bottom
    """
    if is_equal:
        points = np.where(
            np.all(
                [
                    part[:, :, 0] == color[0],
                    part[:, :, 1] == color[1],
                    part[:, :, 2] == color[2],
                ],
                axis=0,
            )
        )
    else:
        points = np.where(
            np.all(
                [
                    part[:, :, 0] != color[0],
                    part[:, :, 1] != color[1],
                    part[:, :, 2] != color[2],
                ],
                axis=0,
            )
        )
    y_list, x_list = np.sort(points[0]), np.sort(points[1])
    return y_list[0], y_list[-1], x_list[0], x_list[-1]


def show(image: np.array):
    """Montre une image.

    Args:
        image (np.array): image.
    """
    open_cv.imshow("show", image)
    open_cv.waitKey(0)


def save(path: str, image: np.array):
    """Enregistre une image.

    Args:
        path (str): chemin d'enregistrement.
        image (np.array): image.
    """
    open_cv.imwrite(path, image)


def get_coordinates(
    img: np.array, color: list, last_x: bool = False, last_y: bool = False
) -> tuple:
    """Récupère les coordonnées d'une couleur.

    Args:
        img (np.array): image.
        color (list): couleur.
        last_x (bool, optional): dernier x. Défaut à False.
        last_y (bool, optional): dernier y. Défaut à False.

    Returns:
        tuple: coordonnées de la couleur.
    """
    list_coordinates = np.where(
        np.all(
            [
                img[:, :, 0] == color[0],
                img[:, :, 1] == color[1],
                img[:, :, 2] == color[2],
            ],
            axis=0,
        )
    )
    coordinates = list(zip(list_coordinates[0], list_coordinates[1]))[0]
    if last_x:
        coordinates = [
            np.sort(list_coordinates[0])[0],
            np.sort(list_coordinates[1])[-1],
        ]
    if last_y:
        coordinates = [
            np.sort(list_coordinates[0])[-1],
            np.sort(list_coordinates[1])[-1],
        ]

    return coordinates


def get_dimension_to_append(height: int, width: int) -> tuple:
    """Récupère le nombre de pixel à rajouter.

    Args:
        new_height (int): hauteur de l'image.
        new_width (int): largeur de l'image.

    Returns:
        tuple: dimension a supprimer, largeur en moins, hauteur en moins.
    """
    is_height_higher = height > width
    difference_dimension = abs(height - width)
    less_width = False
    less_height = False

    if (dimension_to_substract := difference_dimension / 2) % 1:
        dimension_to_substract = (difference_dimension + 1) / 2
        if is_height_higher:
            less_width = True
        else:
            less_height = True

    return int(dimension_to_substract), less_width, less_height


def resize_parsing(crop_face: np.array, dimension_to_substract: int) -> np.array:
    """Redimensionne la prédiction des parties du visage.

    Args:
        crop_face (np.array): visage redimensionné.
        dimension_to_substract (int): dimension à enlever.

    Returns:
        np.array: prédiction du visage redimensionnée.
    """
    (original_height, original_width, _) = crop_face.shape
    is_height_higher = original_height > original_width
    if original_height != original_width:
        axis = 1 if is_height_higher else 0
        append_dimensions = (
            (original_height, dimension_to_substract, 3)
            if is_height_higher
            else (dimension_to_substract, original_width, 3)
        )

        first_append_face = np.full(append_dimensions, (255, 255, 255), np.uint8)
        second_append_face = np.append(first_append_face, crop_face, axis)
        crop_face = np.append(second_append_face, first_append_face, axis)
        return crop_face


def draw_landmarks(
    image: np.array,
    landmark_list: list,
    connection_drawing_spec: DrawingSpec,
    connections: Optional[List[Tuple[int, int]]] = None,
):
    """Dessiner les lignes du visages.

    Args:
        image (np.array): image.
        landmark_list (list): liste des coordonnées.
        connection_drawing_spec (DrawingSpec): connection drawing spec.
        connections (Optional[List[Tuple[int, int]]], optional): connections. Défaut à None.
    """
    for connection in connections:
        start_idx = connection[0]
        end_idx = connection[1]
        open_cv.line(
            image,
            (landmark_list[start_idx].get("x"), landmark_list[start_idx].get("y")),
            (landmark_list[end_idx].get("x"), landmark_list[end_idx].get("y")),
            connection_drawing_spec.color,
            connection_drawing_spec.thickness,
            open_cv.LINE_AA,
        )


def where(
    mask: np.array, color: tuple, equal: bool = True, count: bool = False
) -> tuple:
    """Récupérer la liste des coordonnées d'une couleur.

    Args:
        mask (np.array): mask d'origine.
        color (tuple): couleur.
        equal (bool, optional): égale ? Défaut à True.
        count (bool, optional): comptage ? Défaut à False.

    Returns:
        tuple: coordonnées, coordonnées y et coordonnées x
    """
    if equal:
        coordinates = np.where(
            np.all(
                [
                    mask[:, :, 0] == color[0],
                    mask[:, :, 1] == color[1],
                    mask[:, :, 2] == color[2],
                ],
                axis=0,
            )
        )
    else:
        coordinates = np.where(
            np.all(
                [
                    mask[:, :, 0] != color[0],
                    mask[:, :, 1] != color[1],
                    mask[:, :, 2] != color[2],
                ],
                axis=0,
            )
        )
    indices = list(zip(coordinates[0], coordinates[1]))
    if count:
        return len(indices), coordinates[0], coordinates[1]
    return indices, coordinates[0], coordinates[1]


def get_shade_color(
    color: list, value: int, darker: bool = True, bgr: bool = True
) -> list:
    """Récupère la nuance d'une couleur.

    Args:
        color (list): couleur.
        value (int): valuer.
        darker (bool, optional): rendre plus sombre ? Défaut à True.
        bgr (bool, optional): est sous format BGR ? Défaut à True.

    Returns:
        list: _description_
    """
    color_hex = rgb_to_hex(color, convert_bgr_to_rgb=bgr)

    color_hsl = (
        Color(color_hex)
        .convert("hsl")
        .to_string(precision=0)
        .replace("hsl(", "")
        .replace(")", "")
        .split(" ")
    )

    if darker:
        new_color_percent = (
            new_value
            if (new_value := int(color_hsl[2].replace("%", "")) - value) > 0
            else 0
        )
    else:
        new_color_percent = (
            new_value
            if (new_value := int(color_hsl[2].replace("%", "")) + value) < 100
            else 100
        )

    new_color_hsl = " ".join([color_hsl[0], color_hsl[1], f"{new_color_percent}%"])
    new_color_srgb = (
        Color(f"hsl({new_color_hsl})")
        .convert("srgb")
        .to_string(precision=0)
        .replace("rgb(", "")
        .replace(")", "")
        .split(" ")
    )
    return [int(new_color_srgb[2]), int(new_color_srgb[1]), int(new_color_srgb[0])]
