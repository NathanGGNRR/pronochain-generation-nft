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

File: app/generation_nft/libraries/storage/storage.py
"""
import argparse
import hashlib
from datetime import datetime
from io import BufferedReader, BytesIO
from typing import List, Union

import cv2 as open_cv
import multihash
import numpy as np
import requests
from pydantic import ValidationError
from requests_toolbelt import MultipartEncoder

from app import logger
from app.exceptions import PronochainException
from app.generation_nft.libraries.generation.constants import PictureChannel
from app.generation_nft.libraries.storage.models import ResponseStorage
from app.generation_nft.utils import show
from app.generation_nft_db.schemas.players import ResponseCarApi
from app.settings import settings


class Storage(object):
    """Classe pour gérer le stockage des images dans IPFS."""

    def __init__(self):
        """Initialise la classe de stockage des NFT."""
        self.url = settings.NFT_STORAGE_URL
        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {settings.NFT_STORAGE_API_KEY}",
        }

    def get(self, cid: str) -> ResponseStorage:
        """Récupère un élément stocké sur nft.storage.

        Args:
            cid (str): CID de l'élément.

        Raises:
            PronochainException: une erreur est survenue.
            PronochainException: la réponse renvoyé est dans un mauvais format.

        Returns:
            ResponseStorage: modèle ResponseStorage.
        """
        try:
            response = requests.get(f"{self.url}/{cid}", headers=self.headers)
            result = ResponseStorage.parse_obj(response.json())
            if response.status_code == 200:
                return result
            else:
                raise PronochainException(result.error.message)
        except ValidationError as e:
            logger.error(e)
            raise PronochainException("Get response wrong format")

    def list(
        self, before: datetime = datetime.now(), limit: int = 10
    ) -> ResponseStorage:
        """Récupère une liste d'éléments sotckés sur nft.storage.

        Args:
            before (datetime, optional): date avant. Défaut à datetime.now().
            limit (int, optional): nombre limite. Défaut à 10.

        Raises:
            PronochainException: une erreur est survenue.
            PronochainException: la réponse renvoyé est dans un mauvais format.

        Returns:
            ResponseStorage: modèle ResponseStorage.
        """
        try:
            response = requests.get(
                f"{self.url}/?before={before.strftime('%Y-%m-%dT%H:%M:%SZ')}&limit={limit}",
                headers=self.headers,
            )
            result = ResponseStorage.parse_obj(response.json())
            if response.status_code == 200:
                return result
            else:
                raise PronochainException(result.error.message)
        except ValidationError as e:
            logger.error(e)
            raise PronochainException("Get response wrong format")

    def check(self, cid: str) -> ResponseStorage:
        """Vérifie le statut d'un élément sotcké sur nft.storage.

        Args:
            cid (str): CID de l'élément.

        Raises:
            PronochainException: une erreur est survenue.
            PronochainException: la réponse renvoyé est dans un mauvais format.

        Returns:
            ResponseStorage: modèle ResponseStorage.
        """
        try:
            response = requests.get(f"{self.url}/check/{cid}", headers=self.headers)
            result = ResponseStorage.parse_obj(response.json())
            if response.status_code == 200:
                return result
            else:
                raise PronochainException(result.error.message)
        except ValidationError as e:
            logger.error(e)
            raise PronochainException("Check response wrong format")

    def add(
        self, file: Union[BufferedReader, bytes], is_bytes: bool = False
    ) -> ResponseStorage:
        """Ajouter un élément sur nft.storage.

        Args:
            file (Union[BufferedReader, bytes]): élément.
            is_bytes (bool, optional): est sous format bytes ? Défaut à False.

        Raises:
            PronochainException: une erreur est survenue.
            PronochainException: la réponse renvoyé est dans un mauvais format.

        Returns:
            ResponseStorage: modèle ResponseStorage.
        """
        try:
            headers = {**self.headers, "Content-Type": "image/*"}
            response = requests.post(
                f"{self.url}/upload",
                data=file if is_bytes else file.read(),
                headers=headers,
            )
            result = ResponseStorage.parse_obj(response.json())
            if response.status_code == 200:
                return result
            else:
                raise PronochainException(result.error.message)
        except ValidationError as e:
            logger.error(e)
            raise PronochainException("Add file response wrong format")

    def store(self, json: str) -> ResponseStorage:
        """Ajouter des metadatas sur nft.storage.

        Args:
            json (str): metadata.

        Raises:
            PronochainException: une erreur est survenue.
            PronochainException: la réponse renvoyé est dans un mauvais format.

        Returns:
            ResponseStorage: modèle ResponseStorage.
        """
        try:
            headers = {
                **self.headers,
                "Content-Type": 'multipart/form-data; boundary="abcd"',
            }
            response = requests.post(
                f"{self.url}/store",
                data=MultipartEncoder({"meta": json}, boundary="abcd").to_string(),
                headers=headers,
            )
            result = ResponseStorage.parse_obj(response.json())
            if response.status_code == 200:
                return result
            else:
                raise PronochainException(result.error.message)
        except ValidationError as e:
            logger.error(e)
            raise PronochainException("Add json response wrong format")

    def delete(self, cid: str) -> ResponseStorage:
        """Supprimer un élément sur nft.storage.

        Args:
            cid (str): CID de l'élément.

        Raises:
            PronochainException: une erreur est survenue.
            PronochainException: la réponse renvoyé est dans un mauvais format.

        Returns:
            ResponseStorage: modèle ResponseStorage.
        """
        try:
            response = requests.delete(f"{self.url}/{cid}", headers=self.headers)
            result = ResponseStorage.parse_obj(response.json())
            if response.status_code == 202:
                return result
            else:
                raise PronochainException(result.error.message)
        except ValidationError as e:
            logger.error(e)
            raise PronochainException("Delete response wrong format")

    def picture(
        self, cid: str, filename: str = None, channel: int = PictureChannel.RGBA.value
    ) -> np.array:
        """Récupérer une image sous format png depuis nft.storage.

        Args:
            cid (str): CID de l'image.
            filename (str, optional): nom de l'image. Défaut à None.
            channel (int, optional): dimension de la couleur. Défaut à PictureChannel.RGBA.value.

        Returns:
            np.array: image.
        """
        if filename is not None:
            picture_bytes = BytesIO(
                requests.get(
                    f"https://{cid}.{settings.NFT_STORAGE_GATEWAY}/?filename={filename}"
                ).content
            )
        else:
            picture_bytes = BytesIO(
                requests.get(f"https://{cid}.{settings.NFT_STORAGE_GATEWAY}").content
            )

        if channel == PictureChannel.RGBA.value:
            return open_cv.cvtColor(
                open_cv.imdecode(
                    np.frombuffer(picture_bytes.getbuffer().tobytes(), np.uint8),
                    open_cv.IMREAD_UNCHANGED,
                ),
                open_cv.COLOR_BGR2BGRA,
            )
        elif channel == PictureChannel.RGB.value:
            return open_cv.imdecode(
                np.frombuffer(picture_bytes.getbuffer().tobytes(), np.uint8),
                open_cv.IMREAD_COLOR,
            )

    def convert_to_base58(self, file_path: str) -> str:
        """Converti un fichier en base58.

        Args:
            file_path (str): chemin du fichier.

        Returns:
            str: fichier en base58.
        """
        with open(file_path, "rb") as file:
            sha_hash_digest = hashlib.sha256(file.read()).digest()
            mhash = multihash.encode(sha_hash_digest, "sha2-256")
            file.close()
            return multihash.to_b58_string(mhash)

    def get_cid(self, files: list) -> List[ResponseCarApi]:
        """Récupére le CID de plusieurs fichiers.

        Args:
            files (list): liste de fichiers.

        Returns:
            List[ResponseCarApi]: liste de ResponseCarApi.
        """
        headers = {"accept": "application/json", "Content-Type": "application/json"}
        response = requests.post(
            f"http://{settings.CAR_API_SERVER}/get-cid",
            json={"files": files},
            headers=headers,
        )
        return ResponseCarApi.parse_obj(response.json())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-ba",
        "--bulk_add",
        action="store_true",
        help="Test pour ajouter plusieurs images.",
    )
    parser.add_argument(
        "-a",
        "--add",
        action="store_true",
        help="Test pour ajouter une image.",
    )
    parser.add_argument(
        "-d",
        "--delete",
        action="store_true",
        help="Test pour supprimer une image.",
    )
    parser.add_argument(
        "-c",
        "--check",
        action="store_true",
        help="Test pour check une image.",
    )
    parser.add_argument(
        "-g",
        "--get",
        action="store_true",
        help="Test pour récupérer une image.",
    )
    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="Test pour récupérer la liste des images.",
    )
    parser.add_argument(
        "-p",
        "--picture",
        action="store_true",
        help="Test pour récupérer la liste des images.",
    )
    args = parser.parse_args()

    storage = Storage()
    filenames = [
        "final_draw_face_benzema.jpg.png",
        "final_draw_face_clement.jpg.png",
        "final_draw_face_kim.jpg.png",
    ]
    files = [
        open(
            f"{settings.GENERATION_NFT_PATH}/libraries/face/face_styling/styles/final_face/{filename}",
            "rb",
        )
        for filename in filenames
    ]
    if args.picture:
        picture = storage.picture(storage.add(files[0]).value.cid, filenames[0])
        show(picture)
    else:
        if args.bulk_add:
            response = storage.bulk_add(files)
        elif args.add:
            response = storage.add(files[0])
        elif args.delete:
            response = storage.delete(storage.add(files[0]).value.cid)
        elif args.check:
            response = storage.check(storage.add(files[0]).value.cid)
        elif args.get:
            response = storage.get(storage.add(files[0]).value.cid)
        elif args.list:
            response = storage.list()
        print(response)
