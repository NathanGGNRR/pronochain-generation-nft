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

File: app/generation_nft/tests/test_face_detect.py
"""
from pathlib import Path

import cv2 as open_cv
import numpy as np
import pytest

from app.generation_nft.libraries.face.face_detect.face_detect import FaceDetect
from app.settings import settings


@pytest.fixture
def image_path() -> Path:
    """Récupérer le chemin d'une image.

    Returns:
        Path: chemin de l'image.
    """
    return Path(f"{settings.GENERATION_NFT_PATH}/tests/pictures/5.jpg")


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
def face_detect(image_path: Path, image: np.array) -> FaceDetect:
    """Face detect instance.

    Args:
        image_path (Path): image path.
        image (np.array): image.

    Returns:
        FaceDetect: face detect instance.
    """
    return FaceDetect(
        player_picture=image, player_name=image_path.name, min_detection_confidence=0.8
    )


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

    if str(image_path.name) != "5.jpg":
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

    if image.shape[0] != 380 or image.shape[1] != 570:
        raise AssertionError("L'image n'est pas de la bonne taille.")


def test_face_detection(face_detect: FaceDetect) -> FaceDetect:
    """Test la détection des visages.

    Args:
        face_detect (FaceDetect): face detect instance.

    Raises:
        AssertionError: La détection du visage n'a pas détecté le bon nombre de bisage pour l'image 5.jpg.
    """
    faces = face_detect.face_detection()
    if len(faces) != 5:
        raise AssertionError(
            "La détection du visage n'a pas détecté le bon nombre de visage pour l'image 5.jpg."
        )


def test_apply_margin(face_detect: FaceDetect) -> FaceDetect:
    """Test la fonction pour rajouter une margin à la détection du visage.

    Args:
        face_detect (FaceDetect): face detect instance.

    Raises:
        AssertionError: Lorsque la margin ne dépasse pas la hauteur de l'image ou n'est pas inférieur à 0, la margin doit avoir une coordonnée précise.
        AssertionError: Lorsque la margin est inférieur à 0, la coordonnée doit être de 0.
        AssertionError: Lorsque la margin est supérieur à la hauteur de l'image, la coordonnée doit être égale à la hauteur de l'image.
    """
    first_margin = face_detect.apply_margin(200, 50, False, 500, 0)
    if first_margin != 150:
        raise AssertionError(
            "Lorsque la margin ne dépasse pas la hauteur de l'image ou n'est pas inférieur à 0, la coordonnée doit avoir une valeur précise."
        )
    second_margin = face_detect.apply_margin(200, 250, False, 2500, 0)
    if second_margin != 0:
        raise AssertionError(
            "Lorsque la margin est inférieur à 0, la coordonnée doit être de 0."
        )
    third_margin = face_detect.apply_margin(200, 350, True, 500, 500)
    if third_margin != 500:
        raise AssertionError(
            "Lorsque la margin est supérieur à la hauteur de l'image, la coordonnée doit être égale à la hauteur de l'image."
        )
