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

File: app/utils.py
"""
import io
import os
import re
import shutil
from pathlib import Path
from typing import Optional

import gdown
import requests
from jose import jwt

from alembic import command, config
from app import logger_api
from app.exceptions import PronochainException
from app.generation_nft.libraries.face.face_detect.constants import CAFFE_FILES
from app.generation_nft.libraries.face.face_parsing.constants import FACE_PARSING_MODELS
from app.generation_nft.libraries.face.tilt_learning.constants import PRE_TRAINED_MODELS
from app.generation_nft_db.constants import FIXTURES
from app.settings import settings


def check_files():
    """Vérifie si les fichiers constants sont présent."""
    files = CAFFE_FILES + FACE_PARSING_MODELS + PRE_TRAINED_MODELS + FIXTURES
    zip_path_files = []
    for file in files:
        file_name = file.get("file")
        folder_name = file.get("folder")
        zip_name = file.get("zip")
        if file_name is not None:
            file_path = f"{file.get('parent_path')}/{file_name}"
            if not Path(file_path).is_file():
                download_file(file.get("url"), file_name, file_path)
        elif folder_name is not None:
            folder_path = f"{file.get('parent_path')}/{folder_name}"
            if (
                not Path(folder_path).exists()
                or next(Path(folder_path).iterdir(), None) is None
            ):
                Path(folder_path).mkdir(parents=True, exist_ok=True)
                download_folder(file.get("url"), folder_name, folder_path)
        elif zip_name is not None:
            zip_path = f"{file.get('parent_path')}/{zip_name}"
            if (
                not Path(zip_path).is_file()
                and not Path(f"{file.get('parent_path')}/{zip_name[:-4]}").exists()
            ):
                download_file(file.get("url"), zip_name, zip_path)
                zip_path_files.append(zip_path)
    for zip_path_file in zip_path_files:
        if Path(zip_path_file).is_file():
            shutil.unpack_archive(zip_path_file, zip_path_file[:-3])
            os.remove(zip_path_file)


def download_file(url: str, filename: str, file_path: str):
    """Télécharge un fichier sur le drive de Google.

    Args:
        url (str): url du fichier (en ligne).
        filename (str): nom du fichier.
        file_path (str): chemin du fichier où l'enregistrer.

    Raises:
        PronochainException: le fichier est introuvable en ligne.
    """
    try:
        gdown.download(url, output=file_path)
    except requests.exceptions.MissingSchema:
        error_message = f"Le fichier {filename} n'a pas la bonne URL. Impossible de télécharger le fichier."
        logger_api.error(error_message)
        raise PronochainException(error_message)


def download_folder(url: str, folder_name: str, folder_path: str):
    """Télécharge un dossier sur le drive de Google.

    Args:
        url (str): url du dossier (en ligne).
        folder_name (str): nom du dossier.
        folder_path (str): chemin du dossier où l'enregistrer.

    Raises:
        PronochainException: le dossier est introuvable en ligne.
    """
    try:
        gdown.download_folder(url, output=folder_path)
    except requests.exceptions.MissingSchema:
        error_message = f"Le dossier {folder_name} n'a pas la bonne URL. Impossible de télécharger le dossier."
        logger_api.error(error_message)
        raise PronochainException(error_message)


def run_migrations():
    """Mettre à jour la base de donnée avec les nouvelles migrations."""
    output = io.StringIO()
    temp_alembic_config = config.Config(settings.ALEMBIC_CONFIG_PATH, stdout=output)

    command.history(temp_alembic_config)
    histories = re.findall(r"\->\s(.{12})", output.getvalue())
    output.truncate(0)

    command.current(temp_alembic_config)

    alembic_config = config.Config(settings.ALEMBIC_CONFIG_PATH)
    try:
        current = re.findall(r"[a-zA-Z0-9]{12}", output.getvalue())[0]
        new_migrations = histories[: histories.index(current)]
    except IndexError:
        new_migrations = histories
    output.truncate(0)

    new_migrations.reverse()
    for new_migration in new_migrations:
        command.upgrade(alembic_config, new_migration)


def verify_password_reset_token(token: str) -> Optional[str]:
    """Vérifie si le token d'authentification est à mettre à jour.

    Args:
        token (str): token d'authentification.

    Returns:
        Optional[str]: login du JWT token.
    """
    try:
        decoded_token = jwt.decode(
            token,
            settings.SECURITY_SECRET_KEY,
            algorithms=[settings.SECURITY_ALGORITHM],
        )
        return decoded_token["login"]
    except jwt.JWTError:
        return None


if __name__ == "__main__":
    check_files()
