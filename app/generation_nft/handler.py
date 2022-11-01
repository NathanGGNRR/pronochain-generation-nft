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

File: app/generation_nft/handler.py
"""
from typing import List, Union

import numpy as np
from PIL import ImageColor
from pydantic import BaseModel

from app import logger
from app.exceptions import PronochainException
from app.generation_nft.libraries.card.card import CardStyling
from app.generation_nft.libraries.face.face_aligner.face_aligner import FaceAligner
from app.generation_nft.libraries.face.face_detect.face_detect import FaceDetect
from app.generation_nft.libraries.face.face_landmarks.constants import (
    LEFT_EYE,
    RIGHT_EYE,
)
from app.generation_nft.libraries.face.face_landmarks.face_landmarks import (
    FaceLandmarks,
)
from app.generation_nft.libraries.face.face_parsing.face_parsing import FaceParsing
from app.generation_nft.libraries.face.face_resizing.face_resizing import FaceResizing
from app.generation_nft.libraries.face.face_styling.face_styling import FaceStyling
from app.generation_nft.libraries.face.tilt_learning.tilt_learning import TiltLearning
from app.generation_nft.libraries.generation.constants import PartType
from app.generation_nft.libraries.shirt.shirt import ShirtStyling
from app.generation_nft.libraries.storage.storage import Storage
from app.generation_nft_db.schemas.generation import GenerationPart


class GenerateNFT(
    FaceDetect,
    FaceParsing,
    FaceStyling,
    FaceLandmarks,
    FaceAligner,
    FaceResizing,
    TiltLearning,
    ShirtStyling,
    CardStyling,
    Storage,
):
    """Classe pour générer le NFT.

    Args:
        FaceDetect (FaceDetect): modèle FaceDetect.
        FaceParsing (FaceParsing): modèle FaceParsing.
        FaceStyling (FaceStyling): modèle FaceStyling.
        FaceLandmarks (FaceLandmarks): modèle FaceLandmarks.
        FaceAligner (FaceAligner): modèle FaceAligner.
        FaceResizing (FaceResizing): modèle FaceResizing.
        TiltLearning (TiltLearning): modèle TiltLearning.
        ShirtStyling (ShirtStyling): modèle ShirtStyling.
        CardStyling (CardStyling): modèle CardStyling.
        Storage (Storage): modèle Storage.
    """

    def __init__(self, parts: List[GenerationPart]):
        """Initialise la classe pour générer le NFT.

        Args:
            parts (List[GenerationPart]): liste des parties du NFT.
        """
        for part in parts:
            if part.save_model:
                setattr(self, part.save_model_name, part.value)
            setattr(
                self, part.name, self.get_value(part.type, part.value, part.channel)
            )

        # Initalise data
        (self.height, self.width) = self.player_picture.shape[:2]
        self.min_detection_confidence = 0.8

        FaceDetect.__init__(self)
        FaceParsing.__init__(self)
        FaceStyling.__init__(self)
        FaceLandmarks.__init__(self)
        FaceAligner.__init__(self)
        FaceResizing.__init__(self)
        TiltLearning.__init__(self)
        ShirtStyling.__init__(self)
        CardStyling.__init__(self)
        Storage.__init__(self)

    def get_value(
        self, type: int, model: Union[BaseModel, str], channel: int
    ) -> Union[np.array, str, tuple]:
        """Récupère la valeur.

        Args:
            type (int): type de la partie.
            model (Union[BaseModel, str]): modèle.
            channel (int): dimension de la couleur.

        Raises:
            PronochainException: aucune image stocké sur nft.storage.
            PronochainException: impossible de récupérer l'image.

        Returns:
            Union[np.array, str, tuple]: valeur.
        """
        if type == PartType.COLOR.value:
            return (
                ImageColor.getcolor(model.hex, "RGB")[-1],
                ImageColor.getcolor(model.hex, "RGB")[1],
                ImageColor.getcolor(model.hex, "RGB")[0],
            )
        elif type == PartType.PICTURE.value:
            if model.cid is None:
                raise PronochainException("Aucune image liée à la partie du NFT.")
            try:
                return self.picture(model.cid, filename=model.filename, channel=channel)
            except Exception as err:
                raise PronochainException(
                    f"Erreur lors de la reprise de l'image {model.cid}.", err
                )
        elif type == PartType.TEXT.value:
            return model
        elif type == PartType.TEXT_VALUE.value:
            return model.value
        elif type == PartType.TEXT_COLOR.value:
            return (
                ImageColor.getcolor(model, "RGB")[-1],
                ImageColor.getcolor(model, "RGB")[1],
                ImageColor.getcolor(model, "RGB")[0],
            )

    def handler(self) -> bytes:
        """Génération du joueur.

        Raises:
            PronochainException: impossible de générer le joueur.

        Returns:
            bytes: joueur dessiné.
        """
        faces = self.face_detection()  # détection des visages

        for initial_face in faces:
            # récupère les landmarks du visage
            result_check_landmark_points = self.face_landmark(initial_face)
            if result_check_landmark_points is None:
                logger.info(
                    f"Aucun landmark détecté pour l'image du joueur {self.player.code}, arrêt du processus pour ce visage."
                )
                continue
            check_landmark_points = result_check_landmark_points.landmark

            # récupère les coordonnées de l'oeil gauche
            left_eye_coordinates = self.get_coordinates_from_list(
                initial_face, check_landmark_points, LEFT_EYE
            )

            # récupère les coordonnées de l'oeil droit
            right_eye_coordinates = self.get_coordinates_from_list(
                initial_face, check_landmark_points, RIGHT_EYE
            )

            # aligne la tête pour quelle soit la plus droite possible
            face = self.face_align(
                initial_face, left_eye_coordinates, right_eye_coordinates
            )

            face_resized = self.face_parsing_resizing(face)

            result_landmark_points, normalized_landmark_points = self.face_landmark(
                face_resized, check=False
            )

            if result_landmark_points is None:
                logger.info(
                    f"Aucun landmarks detecte pour l'image du joueur {self.player.code}, arret du processus pour ce visage."
                )
                continue

            try:
                (
                    face_resized,
                    result_landmark_points,
                    normalized_landmark_points,
                ) = self.face_landmark_resizing(face_resized)
            except Exception:
                continue

            self.drawing_face = self.face_parsing(
                face_resized, landmarks=normalized_landmark_points
            )

            if self.drawing_face is not None:
                self.drawing_shirt, self.drawing_crest = self.draw_shirt()
                self.drawing_card_bytes = self.draw_card()
                return self.drawing_card_bytes

        error_message = (
            f"Impossible de générer le NFT pour le joueur {self.player.code}."
        )
        logger.error(error_message)
        raise PronochainException(error_message)
