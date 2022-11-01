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

File: app/generation_nft/libraries/generation/json_schema.py
"""
import json
from typing import List

from app.generation_nft.libraries.generation.constants import PartName, ValueType
from app.generation_nft_db.schemas.generation import GenerationPart
from app.settings import settings


class JsonSchema:
    """Classe pour créer le schéma JSON de metadata."""

    def __init__(self):
        """Initialise la classe pour créer le schéma JSON de metadata."""
        pass

    def create_schema(
        self, nft_cid: str, generation_parts: List[GenerationPart]
    ) -> str:
        """Crée le schéma JSON de metadata.

        Args:
            nft_cid (str): CID du NFT stocké sur nft.storage.
            generation_parts (List[GenerationPart]): liste des parties du NFT.

        Returns:
            str: schéma JSON metadata.
        """
        self.set_generation_part_variables(generation_parts)
        position = self.player_picture.positions[0].type.value
        json_dict = {
            "name": f"{getattr(self, PartName.FIRST_NAME.value).value} {getattr(self, PartName.LAST_NAME.value).value} - from {getattr(self, PartName.COUNTRY_FLAG.value).value}, at {getattr(self, PartName.CLUB.value)}, {position} position, {self.player_picture.age} years old, {self.player_picture.height} centimeters, {self.player_picture.weight} kilos | #{getattr(self, PartName.NFT_COUNT.value)}",
            "description": f"I present to you {getattr(self, PartName.FIRST_NAME.value).value} {getattr(self, PartName.LAST_NAME.value).value}, a footballer from {getattr(self, PartName.COUNTRY_FLAG.value).value} currently playing at {getattr(self, PartName.CLUB.value)} to the position of {position}. He is {self.player_picture.age} years old. He is {self.player_picture.height} centimeters tall and weights {self.player_picture.weight} kilos. His skin color is {getattr(self, PartName.SKIN_COLOR.value).hex}, hair color is {getattr(self, PartName.HAIR_COLOR.value).hex}, eyes color is {getattr(self, PartName.EYES_COLOR.value).hex} and mouth color is {getattr(self, PartName.MOUTH_COLOR.value).hex}. His score is {getattr(self, PartName.GLOBAL_NOTE.value)} with {getattr(self, PartName.POSITION_NOTE.value)} in position note, {getattr(self, PartName.MENTAL_NOTE.value)} in mental note and {getattr(self, PartName.PHYSICAL_NOTE.value)} in physical note.",
            "image": f"https://{nft_cid}.{settings.NFT_STORAGE_GATEWAY}/?filename={nft_cid}.png",
            "properties": self.get_properties(
                generation_parts,
                position,
                self.player_picture.age,
                self.player_picture.height,
                self.player_picture.weight,
            ),
        }
        return json.dumps(json_dict, indent=4)

    def set_generation_part_variables(self, generation_parts: List[GenerationPart]):
        """Initialise les variables dans la classe.

        Args:
            generation_parts (List[GenerationPart]): liste des parties du NFT.
        """
        for generation_part in generation_parts:
            setattr(self, generation_part.name, generation_part.value)

    def get_properties(
        self,
        generation_parts: List[GenerationPart],
        position: str,
        age: int,
        height: int,
        weight: int,
    ) -> list:
        """Crée les propriétées du NFT.

        Args:
            generation_parts (List[GenerationPart]): liste des parties du NFT.
            position (str): position du joueur.
            age (int): age du joueur.
            height (int): taille du joueur.
            weight (int): poids du joueur.

        Returns:
            list: propriétées du NFT.
        """
        properties = []
        property_parts = [
            generation_part
            for generation_part in generation_parts
            if generation_part.value_type is not None
        ]
        for property_part in property_parts:
            value = property_part.value
            if property_part.value_type == ValueType.ELEMENT.value:
                value = property_part.value.name.capitalize().replace("_", " ")
            elif property_part.value_type == ValueType.COLOR.value:
                value = property_part.value.hex
            elif property_part.value_type in [
                ValueType.COUNTRY.value,
                ValueType.NAME.value,
            ]:
                value = property_part.value.value
            elif property_part.value_type == ValueType.PLAYER.value:
                value = property_part.value.code

            properties.append(
                {
                    "trait_type": property_part.name.capitalize().replace("_", " "),
                    "value": value,
                }
            )
        properties = properties + [
            {"trait_type": "Position", "value": position},
            {"trait_type": "Age", "value": age},
            {"trait_type": "Height", "value": height},
            {"trait_type": "Weight", "value": weight},
        ]
        return properties
