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

File: app/generation_nft/tests/test_face_parsing.py
"""
from pathlib import Path

import cv2 as open_cv
import numpy as np
import pytest

from app.generation_nft.libraries.face.face_parsing.face_parsing import FaceParsing
from app.generation_nft.libraries.face.face_styling.face_styling import FaceStyling
from app.settings import settings


@pytest.fixture
def image_path() -> Path:
    """Récupérer le chemin d'une image.

    Returns:
        Path: chemin de l'image.
    """
    return Path(f"{settings.GENERATION_NFT_PATH}/tests/pictures/test_one.jpg")


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
def face(image_path: Path) -> np.array:
    """Face.

    Args:
        image_path (Path): face path.

    Returns:
        np.array: face.
    """
    file_path = f"{image_path.parent}/{image_path.name}"
    return open_cv.imread(file_path)


@pytest.fixture
def face_styling() -> FaceStyling:
    """Face styling instance.

    Returns:
        FaceStyling: face styling instance.
    """
    return FaceStyling()


@pytest.fixture
def face_parsing() -> FaceParsing:
    """Face parsing instance.

    Returns:
        FaceParsing: face parsing instance.
    """
    return FaceParsing()


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

    if str(image_path.name) != "test_one.jpg":
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

    if image.shape[0] != 1388 or image.shape[1] != 1200:
        raise AssertionError("L'image n'est pas de la bonne taille.")
