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

File: app/generation_nft/libraries/face/face_styling/face_styling.py
"""
import warnings

import numpy as np

from app.generation_nft.libraries.face.face_parsing.constants import PartName
from app.generation_nft.libraries.face.face_styling.parts import (
    BeardDrawing,
    BrowDrawing,
    DrawingMixin,
    EyeDrawing,
    HairDrawing,
    MouthDrawing,
    NeckDrawing,
    NoseDrawing,
    SkinDrawing,
)
from app.generation_nft.libraries.face.face_styling.parts.ear import EarDrawing

warnings.filterwarnings("ignore")


class FaceStyling(
    NeckDrawing,
    DrawingMixin,
    NoseDrawing,
    HairDrawing,
    MouthDrawing,
    BrowDrawing,
    EyeDrawing,
    SkinDrawing,
    BeardDrawing,
    EarDrawing,
):
    """Classe pour styliser les zones du visages identifiées."""

    def __init__(self):
        """Initialise la classe d'intéraction des landamarks."""
        self.real_black_color = (0, 0, 0)
        self.black_color = (1, 1, 1)
        self.white_color = (255, 255, 255)
        self.temp_white_color = (254, 254, 254)

        self.darker_eyes_color = None

        self.no_hair = False
        self.drawing_hair = None
        self.drawing_beard = None
        self.real_hair_mask = None
        self.real_brow_mask = None
        self.pilosity_color = None
        self.neck_params = None
        self.neck_color = None

    def draw_face(
        self,
        face: np.array,
        visual_black_color: np.array,
        landmarks: list,
        part_contours: list,
        coordinates: tuple,
        face_shape: tuple,
        face_entire_mask: np.array,
        face_entire_contours: list,
    ) -> np.array:
        """Dessine le visage.

        Args:
            face (np.array): photo du visage.
            visual_black_color (np.array): mask noir du visage.
            landmarks (list): coordonnées du visage.
            part_contours (list): contour des parties.
            coordinates (tuple): coordonnées.
            face_shape (tuple): forme du visage.
            face_entire_mask (np.array): mask entier du visage.
            face_entire_contours (list): contour entier du visage.

        Returns:
            np.array: visage dessiné.
        """
        new_face = face.copy()
        return self.draw_parts(
            visual_black_color,
            new_face,
            landmarks,
            part_contours,
            coordinates,
            face_shape,
            face_entire_mask,
            face_entire_contours,
        )

    def draw_parts(
        self,
        new_face_minimize: np.array,
        new_face: np.array,
        landmarks: list,
        part_contours: list,
        coordinates: tuple,
        face_shape: tuple,
        face_entire_mask: np.array,
        face_entire_contours: list,
    ) -> np.array:
        """Dessine les parties du visage.

        Args:
            new_face_minimize (np.array): visage dupliqué minimisé.
            new_face (np.array): visage dupliqué.
            landmarks (list): coordonnées du visage.
            part_contours (list): contour des parties.
            coordinates (tuple): coordonnées.
            face_shape (tuple): forme du visage.
            face_entire_mask (np.array): mask entier du visage.
            face_entire_contours (list): contour entier du visage.

        Returns:
            np.array: visage dessiné.
        """
        cleaned_face = new_face_minimize.copy()

        for part_contour in part_contours:
            name = part_contour.get("name")
            draw_func = part_contour.get("draw_func")
            clean_func = part_contour.get("clean_func")
            mask_part = part_contour.get("mask_part")
            visual_mask_part = part_contour.get("visual_mask_part")
            visual_contour = part_contour.get("visual_contour")
            depend_on = part_contour.get("depend_on")
            parts = part_contour.get("parts")
            offset_y = part_contour.get("offset_y")

            params = {
                "name": name,
                "face": new_face,
                "mask_part": mask_part,
                "visual_mask_part": visual_mask_part,
                "new_face_minimize": new_face_minimize,
                "contour": visual_contour,
                "landmarks": landmarks,
                "coordinates": coordinates,
                "face_shape": face_shape,
                "parts": parts,
                "face_entire_mask": face_entire_mask,
                "cleaned_face": cleaned_face,
                "offset_y": offset_y,
            }

            if depend_on is not None:
                contour_depend = next(
                    part_depend_on_contour
                    for part_depend_on_contour in part_contours
                    if part_depend_on_contour.get("name") == depend_on
                )
                params["contour_depend_mask"] = contour_depend.get("mask_part")
                params["contour_depend_on"] = contour_depend.get("visual_contour")
                params["contour_depend_visual_mask"] = contour_depend.get(
                    "visual_mask_part"
                )
                params["contour_points"] = contour_depend.get("points")

            if clean_func is not None:
                cleaned_face = getattr(self, f"clean_{clean_func}")(**params)

            if draw_func is not None:
                if name == PartName.HAIR.value:
                    new_face_minimize, self.drawing_hair, self.real_hair_mask = getattr(
                        self, f"draw_{draw_func}"
                    )(**params)
                elif name == PartName.NECK.value:
                    new_face_minimize, self.neck_params = getattr(
                        self, f"draw_{draw_func}"
                    )(**params)
                else:
                    new_face_minimize = getattr(self, f"draw_{draw_func}")(**params)

        return new_face_minimize
