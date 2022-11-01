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

File: app/generation_nft/libraries/face/face_parsing/face_parsing.py
"""
import warnings
from pathlib import Path

import cv2 as open_cv
import gdown
import numpy as np
import requests
import torch
from torch.nn import functional as F
from torchvision import transforms

from app import logger
from app.exceptions import PronochainException
from app.generation_nft.libraries.face.face_parsing.constants import (
    FACE_PARSING_MODELS,
    Config,
    PartName,
)
from app.generation_nft.utils import draw_contours, get_roi, replace_color, where

warnings.filterwarnings("ignore")


class FaceParsing(object):
    """Classe pour récupérer des zones correspondant à des parties du visages identifiées."""

    def __init__(self):
        """Initialise la classe d'intéraction des landmarks."""
        self.config = Config("cpu")
        self.download_missing_files()

        self.face_bottom_y = None
        self.face_contours = None

    def face_parsing(
        self, face: np.array, landmarks: list = [], to_resize: bool = False
    ):
        """Fonction pour récupèrer les différentes parties du visage souhaitées.

        Args:
            face (np.array): visage à segmenter.
            landmarks (list): points du visage.

        Returns:
            list: différents contours des parties du visage voulues.
        """
        face_shape = face.shape
        model = self.config.MODEL
        pretrained_model_path = self.config.PRETRAINED_MODEL_PATH
        device = self.config.DEVICE
        input_size = self.config.INPUT_IMAGE_SIZE

        model.to(device)
        model.load_state_dict(
            torch.load(
                f"{pretrained_model_path.parent}/{pretrained_model_path.name}",
                map_location=device,
            )
        )
        model.eval()

        with torch.no_grad():
            infer_transforms = transforms.Compose(
                [
                    transforms.ToTensor(),
                    transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
                ]
            )

            initial_h, initial_w, _ = face.shape

            resized_face = face.copy()
            if initial_h != input_size or initial_w != input_size:
                resized_face = open_cv.resize(
                    face, (input_size, input_size), interpolation=open_cv.INTER_NEAREST
                )  # redimensionne le visage

            face_tensor = infer_transforms(resized_face).unsqueeze(0).to(device)
            prediction = model(face_tensor)[0]

            prediction = F.interpolate(
                prediction,
                size=(initial_w, initial_h),
                mode="bilinear",
                align_corners=True,
            )

            prediction = prediction.squeeze(0).cpu().numpy().argmax(0)

            black_color = np.array([0, 0, 0])

            visual_mask_color = self.clean_mask(
                prediction, landmarks, to_resize, all=True
            )
            visual_face_mask_color = self.clean_mask(prediction, landmarks, to_resize)

            black_mask_color = visual_mask_color.copy()
            replace_color(black_mask_color, self.config.SKIN_COLOR, black_color)
            replace_color(black_mask_color, self.config.BROW_COLOR, black_color)
            replace_color(black_mask_color, self.config.HAIR_COLOR, black_color)
            replace_color(black_mask_color, self.config.EAR_COLOR, black_color)
            replace_color(black_mask_color, self.config.NOSE_COLOR, black_color)

            face_mask_color = visual_face_mask_color.copy()
            replace_color(face_mask_color, self.config.SKIN_COLOR, black_color)
            replace_color(face_mask_color, self.config.BROW_COLOR, black_color)
            replace_color(face_mask_color, self.config.EAR_COLOR, black_color)
            replace_color(face_mask_color, self.config.NOSE_COLOR, black_color)

            y_top, self.face_bottom_y, x_left, x_right = get_roi(
                black_mask_color, black_color
            )
            coordinates = (
                y_top,
                self.face_bottom_y,
                x_left,
                x_right,
            )

            new_face = face.copy()
            new_face = new_face[y_top : self.face_bottom_y, x_left:x_right]

            if to_resize:
                return new_face

            landmarks_contours = self.get_landmarks_contours(
                visual_mask_color, landmarks, coordinates
            )

            visual_mask_color = visual_mask_color[
                y_top : self.face_bottom_y, x_left:x_right
            ]
            visual_black_color = black_mask_color[
                y_top : self.face_bottom_y, x_left:x_right
            ]

            face_entire_mask, face_entire_contours = draw_contours(
                visual_black_color,
                open_cv.cvtColor(visual_black_color, open_cv.COLOR_BGR2HSV),
                (0, 0, 0),
                open_cv.FILLED,
                as_mask=True,
            )
            self.face_contours = np.full(
                (face_entire_mask.shape[0], face_entire_mask.shape[1], 3),
                255,
                dtype=np.uint8,
            )
            open_cv.drawContours(
                self.face_contours, face_entire_contours, -1, (0, 0, 0), 2
            )

            parsing_contours = self.get_parsing_contours(visual_mask_color)

            contours = landmarks_contours + parsing_contours

            return self.draw_face(
                new_face,
                visual_black_color,
                landmarks,
                contours,
                coordinates,
                face_shape,
                face_entire_mask,
                face_entire_contours,
            )

    def get_landmarks_contours(
        self, visual_mask_color: np.array, landmarks: list, coordinates: tuple
    ) -> list:
        """Récupère les contours des différentes parties du visages.

        Args:
            visual_mask_color (np.array): prédiction des parties du visage.
            landmarks (list): coordonnées landmarks.
            coordinates (tuple): coordonnées

        Returns:
            list: liste des contours.
        """
        contours = []
        for landmark_selected_part in self.config.LANDMARK_SELECTED_PARTS:
            points = landmark_selected_part.get("points")

            landmark_contour = []
            for point in points:
                try:
                    landmark_contour.append(
                        np.array(
                            [
                                int(landmarks[point].get("x")),
                                int(landmarks[point].get("y")),
                            ]
                        )
                    )
                except IndexError:
                    continue

            landmark_contour = np.array([np.array(landmark_contour)])

            virgin_contour = np.full(
                (visual_mask_color.shape[0], visual_mask_color.shape[1], 1),
                0,
                dtype=np.uint8,
            )
            if np.any(landmark_contour):
                open_cv.drawContours(
                    virgin_contour, landmark_contour, -1, 1, open_cv.FILLED
                )
            new_virgin_contour = virgin_contour[
                coordinates[0] : coordinates[1], coordinates[2] : coordinates[3]
            ]

            new_visual_mask_part = new_virgin_contour.copy()
            new_visual_mask_part = open_cv.cvtColor(
                new_visual_mask_part, open_cv.COLOR_GRAY2BGR
            )
            replace_color(new_visual_mask_part, (0, 0, 0), np.array([255, 255, 255]))
            replace_color(new_visual_mask_part, (1, 1, 1), np.array([0, 0, 0]))

            contours.append(
                {
                    "name": landmark_selected_part.get("name"),
                    "draw_func": landmark_selected_part.get("draw_func"),
                    "clean_func": landmark_selected_part.get("clean_func"),
                    "visual_contour": landmark_contour,
                    "mask_part": new_virgin_contour,
                    "visual_mask_part": new_visual_mask_part,
                    "points": points,
                    "offset_y": landmark_selected_part.get("offset_y"),
                }
            )
        return contours

    def clean_mask(
        self, prediction: np.array, landmarks: list, to_resize: bool, all: bool = False
    ) -> np.array:
        """Récupère seulement les parties souhaitées en supprimant les autres parties.

        Args:
            prediction (np.array): prediction.
            landmarks (list): _description_
            to_resize (bool): _description_
            all (bool, optional): _description_. Defaults to False.

        Returns:
            np.array: prediction sans les couleurs non souhaitées.
        """
        visual_one_hot_encoded_mask = prediction.copy().astype(np.uint8)
        visual_mask_color = np.full(
            (
                visual_one_hot_encoded_mask.shape[0],
                visual_one_hot_encoded_mask.shape[1],
                3,
            ),
            255,
            dtype=np.uint8,
        )

        if all:
            clean_parts = self.config.CLEAN_FACE_PARTS
            clean_parts.append(self.config.CLEAN_HAIR_PARTS[-1])
        else:
            clean_parts = self.config.CLEAN_FACE_PARTS

        for clean_part in clean_parts:
            part_color = np.array(clean_part.get("clean_color"))
            part_name = clean_part.get("name")
            for part in clean_part.get("parts"):
                indices = np.where(visual_one_hot_encoded_mask == part)
                visual_mask_color[indices[0], indices[1], :] = part_color
                if not to_resize and part_name == PartName.HAIR.value:
                    visual_mask_color = self.clean_hair(visual_mask_color, landmarks)

        if not all:
            _, coordinates_y, _ = where(
                visual_mask_color, self.config.FACE_PART_COLORS[1]
            )
            visual_mask_color[max(coordinates_y) :, :] = np.array([255, 255, 255])
        return visual_mask_color.astype(np.uint8)

    def clean_hair(self, visual_mask_color: np.array, landmarks: list) -> np.array:
        """Nettoie les cheveux.

        Args:
            visual_mask_color (np.array): prédiction des parties du visage.
            landmarks (list): coordonnées landmarks.

        Returns:
            np.array: cheveux nettoyés.
        """
        _, hair_contours = draw_contours(
            visual_mask_color,
            open_cv.cvtColor(visual_mask_color, open_cv.COLOR_BGR2HSV),
            self.config.HAIR_HSV_COLOR,
            1,
        )
        for hair_contour in hair_contours:
            virgin_hair_contour = np.full(
                (visual_mask_color.shape[0], visual_mask_color.shape[1], 3),
                255,
                dtype=np.uint8,
            )
            open_cv.drawContours(
                virgin_hair_contour,
                np.array([hair_contour]),
                -1,
                (0, 0, 0),
                open_cv.FILLED,
            )
            hair_count, coordinates_y, _ = where(
                virgin_hair_contour, (0, 0, 0), equal=True, count=True
            )
            try:
                if min(coordinates_y) > int(landmarks[self.config.EAR_POINT].get("y")):
                    open_cv.drawContours(
                        visual_mask_color,
                        np.array([hair_contour]),
                        -1,
                        (255, 255, 255),
                        open_cv.FILLED,
                    )
                elif hair_count < 15000:
                    _, skin_coordinates_y, _ = where(
                        visual_mask_color, self.config.SKIN_COLOR
                    )
                    if min(coordinates_y) > min(skin_coordinates_y):
                        open_cv.drawContours(
                            visual_mask_color,
                            np.array([hair_contour]),
                            -1,
                            self.config.SKIN_COLOR,
                            open_cv.FILLED,
                        )
                    else:
                        open_cv.drawContours(
                            visual_mask_color,
                            np.array([hair_contour]),
                            -1,
                            (255, 255, 255),
                            open_cv.FILLED,
                        )
            except IndexError:
                continue
        return visual_mask_color

    def get_parsing_contours(self, visual_mask_color: np.array) -> list:
        """Récupère les contours de parties prédites du visage.

        Args:
            visual_mask_color (np.array): visage avec zones prédites colorées.

        Returns:
            list: liste des contours.
        """
        visual_mask_color_hsv = open_cv.cvtColor(
            visual_mask_color, open_cv.COLOR_BGR2HSV
        )
        contours = []
        for selected_part in self.config.SELECTED_PARTS:
            params = {
                "name": selected_part.get("name"),
                "draw_func": selected_part.get("draw_func"),
                "clean_func": selected_part.get("clean_func"),
                "depend_on": selected_part.get("depend_on"),
                "parts": selected_part.get("parts"),
            }

            hsv_color = selected_part.get("hsv_color")
            if hsv_color is not None:
                visual_selected_part_color, contour = draw_contours(
                    visual_mask_color,
                    visual_mask_color_hsv,
                    hsv_color,
                    open_cv.FILLED,
                    as_mask=True,
                )

                new_visual_mask_part = visual_selected_part_color.copy()
                new_visual_mask_part = open_cv.cvtColor(
                    new_visual_mask_part, open_cv.COLOR_GRAY2BGR
                )
                replace_color(
                    new_visual_mask_part, (0, 0, 0), np.array([255, 255, 255])
                )
                replace_color(new_visual_mask_part, (1, 1, 1), np.array([0, 0, 0]))

                params["visual_contour"] = contour
                params["mask_part"] = visual_selected_part_color
                params["visual_mask_part"] = new_visual_mask_part
            contours.append(params)
        return contours

    def download_missing_files(self):
        """Télécharge les fichiers manquants.

        Raises:
            PronochainException: url du fichier invalide.
        """
        for face_parsing_model in FACE_PARSING_MODELS:
            file = face_parsing_model.get("file")
            file_path = f"{self.config.PRETRAINED_PATH}/{file}"
            if not Path(file_path).is_file():
                try:
                    gdown.download(face_parsing_model.get("url"), file_path)
                except requests.exceptions.MissingSchema:
                    error_message = f"Le fichier {file} n'a pas la bonne URL. Impossible de télécharger le modèle face parsing."
                    logger.error(error_message)
                    raise PronochainException(error_message)
