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

File: app/generation_nft/libraries/generation/generation.py
"""
import argparse
import random
from statistics import mean
from typing import List, Union

from sqlalchemy import func

from app.exceptions import PronochainException
from app.generation_nft.handler import GenerateNFT
from app.generation_nft.libraries.generation.constants import (
    CONSTANT_PARTS,
    RANDOM_PARTS,
    RARITIES_PARTS,
    PartName,
    PartType,
    PictureChannel,
    ValueType,
)
from app.generation_nft.libraries.generation.json_schema import JsonSchema
from app.generation_nft.libraries.storage.storage import Storage
from app.generation_nft_api.dependencies import get_db
from app.generation_nft_db.constants import NameTypeCode, StatTypeCode
from app.generation_nft_db.models import rarities as model_rarities
from app.generation_nft_db.models.clubs import Club
from app.generation_nft_db.models.countries import Country
from app.generation_nft_db.models.generation import Combination
from app.generation_nft_db.models.names import Name, NameType
from app.generation_nft_db.models.nft_parts import (
    Color,
    Element,
    ElementType,
    FacePart,
    FacePartColor,
    NftPart,
)
from app.generation_nft_db.models.players import Player
from app.generation_nft_db.schemas import rarities as schema_rarities
from app.generation_nft_db.schemas.generation import CreateGeneration, GenerationPart
from app.generation_nft_db.scripts.queries import (
    FILTER_NAMES,
    MOUTH_COLOR_VALUE,
    STAT_BY_POSITIONS,
    STAT_BY_TYPES,
)
from app.settings import settings


class Generation:
    """Classe pour gérer la génération du NFT."""

    def __init__(self, rating: float = 1.0):
        """Initiliase la classe pour générer le NFT.

        Args:
            rating (float, optional): côte d'un match. Défaut à 1.0.
        """
        self.rating = rating
        self.db = next(get_db())
        self.storage = Storage()
        self.json_schema = JsonSchema()

    def adjust_rarities_percentage(
        self, rarities: List[model_rarities.Rarity]
    ) -> List[schema_rarities.Rarity]:
        """Modifie les pourcentages de raretées en fonction de la côte.

        Args:
            rarities (List[model_rarities.Rarity]): liste des raretées avec leur pourcentage.

        Returns:
            List[schema_rarities.Rarity]: liste des raretées avec leur nouveau spourcentage.
        """
        global_percentage = sum([rarity.percentage for rarity in rarities])
        final_rating = self.rating - 1
        temp_rarities = [
            schema_rarities.Rarity(
                code=rarity.code, name=rarity.name, percentage=rarity.percentage
            )
            for rarity in rarities
        ]

        if global_percentage != 100.0:
            for temp_rarity in temp_rarities:
                temp_rarity.percentage = (
                    temp_rarity.percentage * 100 / global_percentage
                )

        inversed_temp_rarities = list(reversed(temp_rarities))
        final_rarities = []
        for index, temp_rarity in enumerate(temp_rarities):
            inversed_percentage = (
                temp_rarity.percentage - inversed_temp_rarities[index].percentage
            )

            ratio = 0
            if inversed_percentage != 0:
                ratio = (1 / inversed_percentage) * final_rating
            final_rarities.append(
                schema_rarities.Rarity(
                    code=temp_rarity.code,
                    name=temp_rarity.name,
                    percentage=temp_rarity.percentage - ratio,
                )
            )

        return final_rarities

    def choose_rarity(
        self, rarities: List[schema_rarities.Rarity]
    ) -> schema_rarities.Rarity:
        """Sélectionne la rareté.

        Args:
            rarities (List[schema_rarities.Rarity]): liste des raretées avec leur pourcentage.

        Returns:
            schema_rarities.Rarity: rareté sélectionnée.
        """
        weights = [rarity.percentage for rarity in rarities]
        return random.choices(rarities, weights)[0]

    def choose_parts(self) -> List[GenerationPart]:
        """Choisi les parties du NFT.

        Returns:
            List[GenerationPart]: parties du NFT.
        """
        generation_parts = []
        for rarity_part in RARITIES_PARTS:
            query = self.db.query(rarity_part.get("model")).join(model_rarities.Rarity)

            if (element_type_code := rarity_part.get("element_type_code")) is not None:
                query = query.join(ElementType).filter(
                    ElementType.code == element_type_code
                )

            if (nft_part_code := rarity_part.get("nft_part_code")) is not None:
                query = query.join(NftPart).filter(NftPart.code == nft_part_code)

            if (with_parent := rarity_part.get("with_parent")) is not None:
                parent = next(
                    generation_part.value
                    for generation_part in generation_parts
                    if generation_part.name == with_parent
                )
                query = query.filter(rarity_part.get("model").parent_id == parent.id)

            query_rarities = query.with_entities(model_rarities.Rarity).distinct()
            rarities = sorted(
                [item for item in query_rarities.all()], key=lambda rarity: rarity.code
            )
            final_rarities = self.adjust_rarities_percentage(rarities)
            rarity = self.choose_rarity(final_rarities)

            items = query.filter(model_rarities.Rarity.code == rarity.code)
            element = items.order_by(func.random()).first()

            generation_parts.append(
                GenerationPart(
                    name=rarity_part.get("name"),
                    type=rarity_part.get("type"),
                    value=element,
                    value_type=rarity_part.get("value_type"),
                    save_model=rarity_part.get("save_model"),
                    save_model_name=rarity_part.get("save_model_name"),
                    channel=rarity_part.get("channel"),
                    add_to_combination=rarity_part.get("add_to_combination"),
                    rarity_length=len(rarities),
                    rarity=rarity,
                )
            )
            if rarity_part.get("save_model_name") == PartName.PLAYER.value:
                generation_parts = self.add_player_depending_parts(
                    generation_parts, element
                )

        for random_part in RANDOM_PARTS:
            query = self.db.query(random_part.get("model"))

            if (name_type_code := random_part.get("name_type_code")) is not None:
                query = query.join(NameType).filter(NameType.code == name_type_code)

            if (face_part_code := random_part.get("face_part_code")) is not None:
                query = (
                    query.join(FacePartColor)
                    .join(FacePart)
                    .filter(FacePart.code == face_part_code)
                )

            if random_part.get("depend_face_part_color"):
                mouth_hex = self.db.execute(
                    MOUTH_COLOR_VALUE, {"skin_color_id": generation_parts[-1].value.id}
                ).scalar()
                query = self.db.query(Color).filter(Color.hex == mouth_hex)

            generation_parts.append(
                GenerationPart(
                    name=random_part.get("name"),
                    type=random_part.get("type"),
                    value=random.choice(query.all()),
                    value_type=random_part.get("value_type"),
                    channel=random_part.get("channel"),
                    add_to_combination=random_part.get("add_to_combination"),
                )
            )

        generation_parts = self.add_constant_parts(generation_parts)

        return generation_parts

    def add_player_depending_parts(
        self, generation_parts: List[GenerationPart], player: Player
    ) -> List[GenerationPart]:
        """Ajout des informations dépendant du joueur.

        Args:
            generation_parts (List[GenerationPart]): parties du NFT.
            player (Player): joueur.

        Returns:
            List[GenerationPart]: parties du NFT.
        """
        player_position = player.positions[0]
        generation_parts.append(
            GenerationPart(
                name=PartName.CLUB.value,
                type=PartType.TEXT.value,
                value=player.club.name,
                value_type=ValueType.TEXT.value,
            )
        )
        generation_parts.append(
            GenerationPart(
                name=PartName.POSITION.value,
                type=PartType.PICTURE.value,
                value=player_position.type.element,
                channel=PictureChannel.RGBA.value,
            )
        )
        mental_note, physical_note, position_note = self.calcul_stats(
            player.id, player_position.code
        )

        generation_parts.append(
            GenerationPart(
                name=PartName.MENTAL_NOTE.value,
                type=PartType.TEXT.value,
                value=mental_note,
                note=True,
                value_type=ValueType.TEXT.value,
            )
        )
        generation_parts.append(
            GenerationPart(
                name=PartName.PHYSICAL_NOTE.value,
                type=PartType.TEXT.value,
                value=physical_note,
                note=True,
                value_type=ValueType.TEXT.value,
            )
        )
        generation_parts.append(
            GenerationPart(
                name=PartName.POSITION_NOTE.value,
                type=PartType.TEXT.value,
                value=position_note,
                note=True,
                value_type=ValueType.TEXT.value,
            )
        )
        return generation_parts

    def add_constant_parts(
        self, generation_parts: List[GenerationPart]
    ) -> List[GenerationPart]:
        """Ajout des informations constantes pour le NFT.

        Args:
            generation_parts (List[GenerationPart]): parties du NFT.

        Returns:
            List[GenerationPart]: parties du NFT.
        """
        for constant_part in CONSTANT_PARTS:
            query = self.db.query(constant_part.get("model"))

            if (element_code := constant_part.get("element_code")) is not None:
                query = query.filter(Element.code == element_code)

            if constant_part.get("name") in [
                PartName.FIRST_COLOR.value,
                PartName.SECOND_COLOR.value,
            ]:
                player = next(
                    generation_part.value
                    for generation_part in generation_parts
                    if generation_part.save_model_name == PartName.PLAYER.value
                )
                query = (
                    query.join(getattr(Club, constant_part.get("name")))
                    .join(Player)
                    .filter(Player.code == player.code)
                )

            generation_parts.append(
                GenerationPart(
                    name=constant_part.get("name"),
                    type=constant_part.get("type"),
                    value=query.first(),
                    channel=constant_part.get("channel"),
                )
            )
        return generation_parts

    def check_params(self, params: CreateGeneration):
        """Vérifie la cohérence des parties du NFT.

        Args:
            params (CreateGeneration): paramètre choisi lors de la création d'un NFT.

        Raises:
            PronochainException: le fond de l'écusson doit correspondre à la forme de l'écusson.
        """
        if params.shirt_crest_shape_code.value != str(
            self.db.query(Element)
            .filter(Element.code == int(params.shirt_crest_content_code.value))
            .first()
            .parent.code
        ):
            raise PronochainException(
                "Le fond de l'écusson doit correspondre à la forme de l'écusson"
            )

    def generate_nft(
        self, params: CreateGeneration = None, get_picture: bool = False
    ) -> Union[str, bytes]:
        """Génère le NFT.

        Args:
            params (CreateGeneration, optional): paramètre choisi lors de la création d'un NFT. Défaut à None.
            get_picture (bool, optional): récupère l'image png ? Défaut à False.

        Raises:
            PronochainException: le joueur n'existe pas.

        Returns:
            Union[str, bytes]: image ou metadata.
        """
        if params is not None:
            self.check_params(params)
            first_name_type = (
                self.db.query(NameType)
                .filter(NameType.code == NameTypeCode.FIRST_NAME.value)
                .first()
            )
            last_name_type = (
                self.db.query(NameType)
                .filter(NameType.code == NameTypeCode.LAST_NAME.value)
                .first()
            )

            try:
                first_name_id = (
                    self.db.execute(
                        FILTER_NAMES,
                        {
                            "type_code": NameTypeCode.FIRST_NAME.value,
                            "name": params.player_first_name.lower(),
                        },
                    )
                    .mappings()
                    .first()
                )
                first_name = self.db.query(Name).get(first_name_id.get("id"))
            except Exception:
                db_name = Name(value=params.player_first_name, type=first_name_type)
                self.db.add(db_name)
                self.db.commit()
                first_name = db_name

            try:
                last_name_id = (
                    self.db.execute(
                        FILTER_NAMES,
                        {
                            "type_code": NameTypeCode.LAST_NAME.value,
                            "name": params.player_last_name.lower(),
                        },
                    )
                    .mappings()
                    .first()
                )
                last_name = self.db.query(Name).get(last_name_id.get("id"))
            except Exception:
                db_name = Name(value=params.player_last_name, type=last_name_type)
                self.db.add(db_name)
                self.db.commit()
                last_name = db_name

            try:
                player = (
                    self.db.query(Player)
                    .filter(Player.code == params.player_code)
                    .first()
                )
            except Exception:
                raise PronochainException(
                    f"Le joueur avec le code {params.player_code} n'existe pas."
                )

            card_shape = (
                self.db.query(Element)
                .filter(Element.code == int(params.card_shape_code.value))
                .first()
            )
            card_pattern = (
                self.db.query(Element)
                .filter(Element.code == int(params.card_pattern_code.value))
                .first()
            )
            card_color = (
                self.db.query(Color)
                .filter(Color.hex == params.card_color.value)
                .first()
            )
            shirt_pattern = (
                self.db.query(Element)
                .filter(Element.code == int(params.shirt_pattern_code.value))
                .first()
            )
            crest_shape = (
                self.db.query(Element)
                .filter(Element.code == int(params.shirt_crest_shape_code.value))
                .first()
            )
            crest_pattern = (
                self.db.query(Element)
                .filter(Element.code == int(params.shirt_crest_pattern_code.value))
                .first()
            )
            crest_content = (
                self.db.query(Element)
                .filter(Element.code == int(params.shirt_crest_content_code.value))
                .first()
            )

            card_shape_rarities = (
                self.db.query(model_rarities.Rarity)
                .join(Element)
                .join(NftPart)
                .join(ElementType)
                .filter(
                    ElementType.code == card_shape.type.code,
                    NftPart.code == card_shape.nft_part.code,
                )
                .all()
            )
            card_pattern_rarities = (
                self.db.query(model_rarities.Rarity)
                .join(Element)
                .join(NftPart)
                .join(ElementType)
                .filter(
                    ElementType.code == card_pattern.type.code,
                    NftPart.code == card_pattern.nft_part.code,
                )
                .all()
            )
            card_color_rarities = self.db.query(model_rarities.Rarity).join(Color).all()
            shirt_pattern_rarities = (
                self.db.query(model_rarities.Rarity)
                .join(Element)
                .join(NftPart)
                .join(ElementType)
                .filter(
                    ElementType.code == shirt_pattern.type.code,
                    NftPart.code == shirt_pattern.nft_part.code,
                )
                .all()
            )
            crest_shape_rarities = (
                self.db.query(model_rarities.Rarity)
                .join(Element)
                .join(NftPart)
                .join(ElementType)
                .filter(
                    ElementType.code == crest_shape.type.code,
                    NftPart.code == crest_shape.nft_part.code,
                )
                .all()
            )
            crest_pattern_rarities = (
                self.db.query(model_rarities.Rarity)
                .join(Element)
                .join(NftPart)
                .join(ElementType)
                .filter(
                    ElementType.code == crest_pattern.type.code,
                    NftPart.code == crest_pattern.nft_part.code,
                )
                .all()
            )
            crest_content_rarities = (
                self.db.query(model_rarities.Rarity)
                .join(Element)
                .join(NftPart)
                .join(ElementType)
                .filter(
                    ElementType.code == crest_content.type.code,
                    NftPart.code == crest_content.nft_part.code,
                )
                .all()
            )
            player_rarities = self.db.query(model_rarities.Rarity).all()

            generation_parts = [
                GenerationPart(
                    name=PartName.CARD_SHAPE.value,
                    type=PartType.PICTURE.value,
                    value=card_shape,
                    value_type=ValueType.ELEMENT.value,
                    channel=PictureChannel.RGBA.value,
                    add_to_combination=True,
                    rarity_length=len(card_shape_rarities),
                    rarity=card_shape.rarity,
                ),
                GenerationPart(
                    name=PartName.CARD_PATTERN.value,
                    type=PartType.PICTURE.value,
                    value=card_pattern,
                    value_type=ValueType.ELEMENT.value,
                    channel=PictureChannel.RGBA.value,
                    add_to_combination=True,
                    rarity_length=len(card_pattern_rarities),
                    rarity=card_pattern.rarity,
                ),
                GenerationPart(
                    name=PartName.CARD_COLOR.value,
                    type=PartType.COLOR.value,
                    value=card_color,
                    value_type=ValueType.COLOR.value,
                    add_to_combination=True,
                    rarity_length=len(card_color_rarities),
                    rarity=card_color.rarity,
                ),
                GenerationPart(
                    name=PartName.SHIRT_PATTERN.value,
                    type=PartType.PICTURE.value,
                    value=shirt_pattern,
                    value_type=ValueType.ELEMENT.value,
                    channel=PictureChannel.RGBA.value,
                    add_to_combination=True,
                    rarity_length=len(shirt_pattern_rarities),
                    rarity=shirt_pattern.rarity,
                ),
                GenerationPart(
                    name=PartName.CREST_SHAPE.value,
                    type=PartType.PICTURE.value,
                    value=crest_shape,
                    value_type=ValueType.ELEMENT.value,
                    channel=PictureChannel.RGB.value,
                    add_to_combination=True,
                    rarity_length=len(crest_shape_rarities),
                    rarity=crest_shape.rarity,
                ),
                GenerationPart(
                    name=PartName.CREST_PATTERN.value,
                    type=PartType.PICTURE.value,
                    value=crest_pattern,
                    value_type=ValueType.ELEMENT.value,
                    channel=PictureChannel.RGB.value,
                    add_to_combination=True,
                    rarity_length=len(crest_pattern_rarities),
                    rarity=crest_pattern.rarity,
                ),
                GenerationPart(
                    name=PartName.CREST_CONTENT.value,
                    type=PartType.PICTURE.value,
                    value=crest_content,
                    value_type=ValueType.ELEMENT.value,
                    channel=PictureChannel.RGB.value,
                    add_to_combination=True,
                    rarity_length=len(crest_content_rarities),
                    rarity=crest_content.rarity,
                ),
                GenerationPart(
                    name=PartName.PLAYER_PICTURE.value,
                    type=PartType.PICTURE.value,
                    value=player,
                    value_type=ValueType.PLAYER.value,
                    channel=PictureChannel.RGB.value,
                    save_model=True,
                    save_model_name=PartName.PLAYER.value,
                    add_to_combination=True,
                    rarity_length=len(player_rarities),
                    rarity=player.rarity,
                ),
                GenerationPart(
                    name=PartName.FIRST_NAME.value,
                    type=PartType.TEXT_VALUE.value,
                    value_type=ValueType.NAME.value,
                    value=first_name,
                    add_to_combination=True,
                ),
                GenerationPart(
                    name=PartName.LAST_NAME.value,
                    type=PartType.TEXT_VALUE.value,
                    value_type=ValueType.NAME.value,
                    value=last_name,
                    add_to_combination=True,
                ),
                GenerationPart(
                    name=PartName.COUNTRY_FLAG.value,
                    type=PartType.PICTURE.value,
                    value_type=ValueType.COUNTRY.value,
                    value=self.db.query(Country)
                    .filter(Country.code == params.country_code.value)
                    .first(),
                    channel=PictureChannel.RGBA.value,
                    add_to_combination=True,
                ),
                GenerationPart(
                    name=PartName.HAIR_COLOR.value,
                    type=PartType.COLOR.value,
                    value_type=ValueType.COLOR.value,
                    value=self.db.query(Color)
                    .filter(Color.hex == params.player_hair_color.value)
                    .first(),
                    add_to_combination=True,
                ),
                GenerationPart(
                    name=PartName.EYES_COLOR.value,
                    type=PartType.COLOR.value,
                    value_type=ValueType.COLOR.value,
                    value=self.db.query(Color)
                    .filter(Color.hex == params.player_eyes_color.value)
                    .first(),
                    add_to_combination=True,
                ),
                GenerationPart(
                    name=PartName.SKIN_COLOR.value,
                    type=PartType.COLOR.value,
                    value_type=ValueType.COLOR.value,
                    value=self.db.query(Color)
                    .filter(Color.hex == params.player_skin_color.value)
                    .first(),
                    add_to_combination=True,
                ),
            ]

            mouth_color_value = self.db.execute(
                MOUTH_COLOR_VALUE, {"skin_color_id": generation_parts[-1].value.id}
            ).scalar()
            generation_parts.append(
                GenerationPart(
                    name=PartName.MOUTH_COLOR.value,
                    type=PartType.COLOR.value,
                    value=self.db.query(Color)
                    .filter(Color.hex == mouth_color_value)
                    .first(),
                    value_type=ValueType.COLOR.value,
                    add_to_combination=True,
                )
            )
            generation_parts = self.add_player_depending_parts(generation_parts, player)
            generation_parts = self.add_constant_parts(generation_parts)
        else:
            generation_parts = self.choose_parts()

        generation_parts = self.save_combinations(generation_parts)
        generation_parts = self.calcul_global_note(generation_parts)

        generate_nft = GenerateNFT(generation_parts)
        nft_picture = generate_nft.handler()
        if get_picture:
            return nft_picture

        json = self.retrieve_json_metadata(nft_picture, generation_parts)
        return f"https://{self.storage.store(json).value.ipnft}.{settings.NFT_STORAGE_GATEWAY}/metadata.json"

    def calcul_stats(self, player_id: int, position_code: int) -> tuple:
        """Calcul les notes du joueurs.

        Args:
            player_id (int): id player.
            position_code (int): code position.

        Returns:
            tuple: note mental, note physique et note de la position
        """
        mental_notes = [
            stat.get("value")
            for stat in self.db.execute(
                STAT_BY_TYPES,
                {"type_code": StatTypeCode.MENTAL.value, "player_id": player_id},
            ).mappings()
        ]
        physical_notes = [
            stat.get("value")
            for stat in self.db.execute(
                STAT_BY_TYPES,
                {"type_code": StatTypeCode.PHYSICAL.value, "player_id": player_id},
            ).mappings()
        ]
        position_notes = [
            stat.get("value")
            for stat in self.db.execute(
                STAT_BY_POSITIONS,
                {"position_code": position_code, "player_id": player_id},
            ).mappings()
        ]

        return (
            str(round(mean(mental_notes))),
            str(round(mean(physical_notes))),
            str(round(mean(position_notes))),
        )

    def calcul_global_note(
        self, generation_parts: List[GenerationPart]
    ) -> List[GenerationPart]:
        """Calcul de la note global du joueur.

        Args:
            generation_parts (List[GenerationPart]): parties du NFT.

        Returns:
            List[GenerationPart]: parties du NFT.
        """
        global_note = round(
            mean(
                [
                    int(generation_part.value)
                    for generation_part in generation_parts
                    if generation_part.note
                ]
            )
        )
        generation_part_rarities = [
            generation_part
            for generation_part in generation_parts
            if generation_part.rarity is not None
        ]

        for generation_part_rarity in generation_part_rarities:
            rarity_point = 10 / generation_part_rarity.rarity_length
            global_note += round(rarity_point * generation_part_rarity.rarity.code)

        generation_parts.append(
            GenerationPart(
                name=PartName.GLOBAL_NOTE.value,
                type=PartType.TEXT.value,
                value=str(global_note),
                value_type=ValueType.TEXT.value,
            )
        )
        return generation_parts

    def save_combinations(
        self, generation_parts: List[GenerationPart]
    ) -> List[GenerationPart]:
        """Enregistre la combinaison du NFT en base de donnée.

        Args:
            generation_parts (List[GenerationPart]): parties du NFT.

        Returns:
            List[GenerationPart]: parties du NFT.
        """
        params = {
            f"{generation_part.name}_id": generation_part.value.id
            for generation_part in generation_parts
            if generation_part.add_to_combination
        }
        generation_parts.append(
            GenerationPart(
                name=PartName.NFT_COUNT.value,
                type=PartType.TEXT.value,
                value=str(self.get_or_create(params)),
                value_type=ValueType.TEXT.value,
            )
        )
        return generation_parts

    def get_or_create(self, params: dict) -> int:
        """Récupère ou créer la combinaison et récupère le nombre de fois que celle-ci est apparue.

        Args:
            params (list): parties du NFT.

        Returns:
            int: nombre de fois où la combinaison est apparu.
        """
        combination = self.db.query(Combination).filter_by(**params)
        if combination.one_or_none() is not None:
            count = combination.one_or_none().count + 1
            combination.update({"count": count}, synchronize_session=False)
            self.db.commit()
            self.db.refresh(combination.one_or_none())
        else:
            count = 1
            self.db.add(Combination(**params, count=count))
            self.db.commit()
        return count

    def retrieve_json_metadata(
        self, nft_picture: bytes, generation_parts: List[GenerationPart]
    ) -> str:
        """Récupère le schéma JSON metadata.

        Args:
            nft_picture (bytes): nft.
            generation_parts (List[GenerationPart]): parties du NFT.

        Returns:
            str: schéma JSON metadata.
        """
        nft_cid = self.storage.add(nft_picture, is_bytes=True).value.cid
        return self.json_schema.create_schema(nft_cid, generation_parts)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l",
        "--less",
        action="store_true",
        help="Test avec uniquement quelques raretés.",
    )
    parser.add_argument(
        "-g",
        "--generate",
        action="store_true",
        help="Test l'intégralité d'une génération.",
    )
    args = parser.parse_args()

    rating = 2.0
    generation = Generation(rating)
    if args.generate:
        generation.generate_nft()
    else:
        if args.less:
            rarities = (
                generation.db.query(model_rarities.Rarity)
                .order_by(model_rarities.Rarity.code)
                .filter(model_rarities.Rarity.code.in_([1, 4, 7, 9]))
            )
        else:
            rarities = (
                generation.db.query(model_rarities.Rarity)
                .order_by(model_rarities.Rarity.code)
                .all()
            )

        final_rarities = generation.adjust_rarities_percentage(rarities)
        choosen_rarity = generation.choose_rarity(final_rarities)
