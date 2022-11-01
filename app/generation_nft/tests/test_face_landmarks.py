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

File: app/generation_nft/tests/test_face_landmarks.py
"""
from pathlib import Path
from typing import Union

import cv2 as open_cv
import numpy as np
import pytest

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
def faceStyling() -> FaceStyling:
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
    file_path = f"{image_path.parent}/{image_path.name}"
    return open_cv.imread(file_path)


@pytest.fixture
def landmarks_not_check(
    face_landmarks: FaceLandmarks, image: np.array
) -> Union[list, None]:
    """Landmarks array.

    Args:
        face_landmarks (FaceLandmarks): face landmarks instance.
        image (np.array): image.

    Returns:
        Union[list, None]: landmarks array.
    """
    return face_landmarks.face_landmark(image, check=False)


@pytest.fixture
def landmarks_check(
    face_landmarks: FaceLandmarks, image: np.array
) -> Union[list, None]:
    """Landmarks array.

    Args:
        face_landmarks (FaceLandmarks): face landmarks instance.
        image (np.array): image.

    Returns:
        Union[list, None]: landmarks array.
    """
    return face_landmarks.face_landmark(image).landmark


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


def test_face_landmark_not_check(landmarks_not_check: Union[list, None]):
    """Test la création des landmarks.

    Args:
        landmarks_not_check (Union[list, None]):  face landmarks array.

    Raises:
        AssertionError: La librairie face_landmark n'a détectée aucun visage ou ne fonctionne pas correctement.
    """
    if landmarks_not_check[0] is None or len(landmarks_not_check[1]) == 0:
        raise AssertionError(
            "La librairie face_landmark n'a détectée aucun visage ou ne fonctionne pas correctement."
        )


def test_face_landmark_check(landmarks_check: Union[list, None]):
    """Test la création des landmarks.

    Args:
        landmarks_check (Union[list, None]):  face landmarks array.

    Raises:
        AssertionError: La librairie face_landmark n'a détectée aucun visage ou ne fonctionne pas correctement.
    """
    if landmarks_check is None:
        raise AssertionError(
            "La librairie face_landmark n'a détectée aucun visage ou ne fonctionne pas correctement."
        )
