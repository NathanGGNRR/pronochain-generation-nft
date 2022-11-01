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

File: app/generation_nft/libraries/face/face_detect/face_detect.py
"""

from pathlib import Path

import cv2 as open_cv
import gdown
import numpy as np
import requests

from app import logger
from app.exceptions import PronochainException
from app.generation_nft.libraries.face.face_detect.constants import CAFFE_FILES
from app.generation_nft.utils import get_dimension_to_append, resize_parsing
from app.settings import settings


class FaceDetect(object):
    """Classe permettant d'intéragir avec la détection du visage."""

    def __init__(
        self,
        upscale_detection: float = 0.2,
        player_picture: np.array = None,
        player_name: str = None,
        min_detection_confidence: float = None,
    ):
        """Initialise la classe permettant de détecter les visages avec la méthode du modèle pré-entrainé caffe.

        Args:
            upscale_detection (float, optional): augmenter en pourcentage de la détection du visage. Si la valeur est à 0.1,
                cela signifie que je vais agrandir la détection de 10% de la hauteur et de la largeur. Par défaut à 0.05.
            player_picture (np.array, optional): image des tests.
            player_name (str, optional): nom de l'image pour les tests.
            min_detection_confidence (float, optional): la valeur minimum de confiance de la détection d'un visage. Par défaut à 0.8 (80%).
        """
        self.upscale_detection = upscale_detection

        self.caffe_folder_path = (
            f"{settings.GENERATION_NFT_PATH}/libraries/face/face_detect/pre_trained"
        )
        self.download_missing_files()
        self.caffe_prototxt_path = f"{self.caffe_folder_path}/deploy.prototxt.txt"
        self.caffe_model_path = f"{self.caffe_folder_path}/face_detect.caffemodel"

        if (
            player_picture is not None
            and player_name is not None
            and min_detection_confidence is not None
        ):
            self.player_picture = player_picture
            self.player_code = player_name
            self.min_detection_confidence = min_detection_confidence
            self.height, self.width = (
                self.player_picture.shape[0],
                self.player_picture.shape[1],
            )
        else:
            self.player_code = self.player.code

    def face_detection(self) -> list:
        """Fonction qui permet de détecter un visage et de retourner uniquement ce visage.

        Raises:
            convert_blob_error: erreur lors pour convertir image en blob.
            detection_error: erreur lors de la détection du visage.

        Returns:
            list: liste des visages détectés avec plus de 80% de confiance.
        """
        detector = open_cv.dnn.readNetFromCaffe(
            self.caffe_prototxt_path, self.caffe_model_path
        )

        try:
            blob_image = open_cv.dnn.blobFromImage(
                open_cv.resize(self.player_picture, (self.width, self.height)),
                1.0,
                (self.width, self.height),
                (104.0, 177.0, 123.0),
            )
        except Exception as convert_blob_error:
            logger.error(
                f"Impossible de convertir l'image du joueur {self.player_code} en blob.",
                convert_blob_error,
            )
            raise convert_blob_error

        try:
            detector.setInput(blob_image)
            face_detections = detector.forward()
        except Exception as detection_error:
            logger.error(
                f"La détection du visage du joueur {self.player_code} a rencontrée une erreur.",
                detection_error,
            )
            raise detection_error

        return self.get_only_face(face_detections)

    def get_only_face(self, face_detections: np.array) -> list:
        """Fonction pour récupérer seulement le visage sur l'image.

        Args:
            face_detections (np.array): liste des visages détectés

        Returns:
            list: visage découpé.
        """
        margin_height = int(np.ceil(self.height * self.upscale_detection))
        margin_width = int(np.ceil(self.width * self.upscale_detection))
        faces = []
        unique_box_size = []
        for index in range(0, face_detections.shape[2]):
            confidence = face_detections[0, 0, index, 2]
            if confidence > self.min_detection_confidence:
                box = face_detections[0, 0, index, 3:7] * np.array(
                    [self.width, self.height, self.width, self.height]
                )
                (left, top, right, bottom) = box.astype("int")

                self.margin_top = self.apply_margin(
                    top, margin_height, False, self.height, 0
                )
                self.margin_left = self.apply_margin(
                    left, margin_width, False, self.width, 0
                )
                self.margin_bottom = self.apply_margin(
                    bottom, margin_height, True, self.height, self.height
                )
                self.margin_right = self.apply_margin(
                    right, margin_width, True, self.width, self.width
                )

                if (
                    box_size := f"{self.margin_top} {self.margin_bottom} {self.margin_left} {self.margin_right}"
                ) in unique_box_size:
                    continue
                unique_box_size.append(box_size)

                dimension_to_substract = None
                if (original_height := self.margin_bottom - self.margin_top) != (
                    original_width := self.margin_right - self.margin_left
                ):
                    (
                        dimension_to_substract,
                        less_width,
                        less_height,
                    ) = get_dimension_to_append(original_height, original_width)

                    if less_width:
                        self.margin_right -= 1

                    if less_height:
                        self.margin_bottom -= 1

                crop_face = self.player_picture[
                    self.margin_top : self.margin_bottom,
                    self.margin_left : self.margin_right,
                ]

                if dimension_to_substract is not None:
                    crop_face = resize_parsing(crop_face, dimension_to_substract)

                faces.append(crop_face)

        sorted_faces = []
        for face in faces:
            if (
                len(sorted_faces) > 0
                and face.shape[0] <= self.height
                and sorted_faces[0].shape[0] < face.shape[0]
            ):
                sorted_faces.insert(0, face)
                continue
            sorted_faces.append(face)
        return sorted_faces

    def download_missing_files(self):
        """Télécharge les fichiers manquants.

        Raises:
            PronochainException: url du fichier invalide.
        """
        for caffe_file in CAFFE_FILES:
            file = caffe_file.get("file")
            file_path = f"{self.caffe_folder_path}/{file}"
            if not Path(file_path).is_file():
                try:
                    gdown.download(caffe_file.get("url"), file_path)
                except requests.exceptions.MissingSchema:
                    error_message = f"Le fichier {file} n'a pas la bonne URL. Impossible de télécharger le fichier caffe."
                    logger.error(error_message)
                    raise PronochainException(error_message)

    def apply_margin(
        self,
        coordinate_value: int,
        margin: int,
        add_margin: bool,
        check_value: int,
        limit_value: int,
    ) -> int:
        """Applique la margin à la détection du visage pour prendre en compte les cheveux, les oreilles et le cou.

        Args:
            coordinate_value (int): correspond au top/bottom/left/right.
            margin (int): margin de la hauteur ou de la largeur.
            add_margin (bool): ajoute si True, soustrait si False.
            check_value (int): valeur limite, si la margin est inférieure à 0 ou à la hauteur ou largeur de l'image.
            limit_value (int): valeur si limite dépassée.

        Returns:
            int: nouvelle coordonnée de la surface du visage avec la margin.
        """
        limit_margin = (
            coordinate_value + margin if add_margin else coordinate_value - margin
        )
        if limit_margin > check_value or limit_margin < 0:
            limit_margin = limit_value
        return limit_margin
