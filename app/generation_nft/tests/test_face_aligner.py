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

File: app/generation_nft/tests/test_face_align.py
"""

from pathlib import Path
from typing import Union

import cv2 as open_cv
import numpy as np
import pytest

from app.generation_nft.libraries.face.face_aligner.face_aligner import FaceAligner
from app.generation_nft.libraries.face.face_landmarks.constants import (
    LEFT_EYE,
    RIGHT_EYE,
)
from app.generation_nft.libraries.face.face_landmarks.face_landmarks import (
    FaceLandmarks,
)
from app.generation_nft.libraries.face.face_styling.face_styling import FaceStyling
from app.settings import settings


@pytest.fixture
def image_path() -> Path:
    """Récupérer le chemin d'une image.

    Returns:
        Path: chemin de l'image.
    """
    return Path(f"{settings.GENERATION_NFT_PATH}/tests/pictures/1.jpg")


@pytest.fixture
def face_styling() -> FaceStyling:
    """Face styling instance.

    Returns:
        FaceStyling: face styling instance.
    """
    return FaceStyling()


@pytest.fixture
def face_landmarks() -> FaceLandmarks:
    """Face landmarks instance.

    Returns:
        FaceLandmarks: face landmarks instance.
    """
    return FaceLandmarks(min_detection_confidence=0.8)


@pytest.fixture
def image(image_path: Path) -> np.array:
    """Image.

    Args:
        image_path (Path): image path.

    Returns:
        np.array: image.
    """
    return open_cv.imread(f"{image_path.parent}/{image_path.name}")


@pytest.fixture
def landmarks(face_landmarks: FaceLandmarks, image: np.array) -> Union[list, None]:
    """Landmarks array.

    Args:
        face_landmarks (FaceLandmarks): face landmarks instance.
        image (np.array): image.

    Returns:
        Union[list, None]: landmarks array.
    """
    return face_landmarks.face_landmark(image).landmark


@pytest.fixture
def face_aligner() -> FaceAligner:
    """Face aligner instance.

    Returns:
        FaceAligner: face aligner instance.
    """
    return FaceAligner()


def test_image_path(image_path: Path):
    """Test le chemin de l'image.

    Args:
        image_path (Path): chemin de l'image.

    Raises:
        AssertionError: L'image est introuvable.
        AssertionError: Le nom de l'image n'est pas correcte.
    """
    if not image_path.is_file():
        raise AssertionError("L'image est introuvable.")

    if str(image_path.name) != "1.jpg":
        raise AssertionError("Le nom de l'image n'est pas correcte.")


def test_image(image: np.array):
    """Test la fonction imread d'open_cv.

    Args:
        image (np.array): image.

    Raises:
        AssertionError: L'image est introuvable.
        AssertionError: L'image n'est pas de la bonne taille.
    """
    if image is None:
        raise AssertionError("L'image est introuvable.")

    if image.shape[0] != 600 or image.shape[1] != 800:
        raise AssertionError("L'image n'est pas de la bonne taille.")


def test_face_align(
    face_styling: FaceStyling,
    image: np.array,
    landmarks: Union[list, None],
    face_aligner: FaceAligner,
):
    """Test le réalignement du visage.

    Args:
        face_styling (FaceStyling):  face styling instance.
        image (np.array): image.
        landmarks (Union[list, None]):  face landmarks array.
        face_aligner (FaceAligner): face aligner instance.

    Raises:
        AssertionError: Impossible d'aligner le visage. Aucun visage n'a été detecté.
    """
    left_eye_coordinates = face_styling.get_coordinates_from_list(
        image, landmarks, LEFT_EYE
    )

    right_eye_coordinates = face_styling.get_coordinates_from_list(
        image, landmarks, RIGHT_EYE
    )
    face_aligned = face_aligner.face_align(
        image, left_eye_coordinates, right_eye_coordinates
    )
    if face_aligned is None:
        raise AssertionError(
            "Impossible d'aligner le visage. Aucun visage n'a été detecté."
        )


def test_get_mass_center(
    face_styling: FaceStyling,
    image: np.array,
    landmarks: Union[list, None],
    face_aligner: FaceAligner,
):
    """Test la fonction get_mass_center.

    Args:
        face_styling (FaceStyling):  face styling instance.
        image (np.array): image.
        landmarks (Union[list, None]):  face landmarks array.
        face_aligner (FaceAligner): face aligner instance.

    Raises:
        AssertionError: La récupération du point centrale massique ne fonctionne pas.
    """
    left_eye_coordinates = face_styling.get_coordinates_from_list(
        image, landmarks, LEFT_EYE
    )
    left_eye_center = face_aligner.get_mass_center(left_eye_coordinates)
    if left_eye_center[0] != np.float16(292.8) or left_eye_center[1] != np.float16(
        221.5
    ):
        raise AssertionError(
            "La récupération du point centrale massique ne fonctionne pas."
        )
