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

File: app/generation_nft_db/scripts/fixtures.py
"""

import argparse
import re
import warnings
from typing import Union

import pandas as pd
from tqdm import tqdm

from app import logger_api
from app.exceptions import PronochainException
from app.generation_nft.libraries.storage.storage import Storage
from app.generation_nft_api.dependencies import get_db
from app.generation_nft_db.constants import FIXTURES_ORDER, NameTypeCode
from app.generation_nft_db.core.utils import (
    add_into_database,
    add_multiple_into_database,
)
from app.generation_nft_db.models import (
    Club,
    Country,
    Division,
    Name,
    NameType,
    Player,
    PlayerStat,
    Position,
    PositionType,
    Stat,
    StatType,
    User,
)
from app.generation_nft_db.models.nft_parts import (
    Color,
    Element,
    ElementType,
    FacePart,
    FacePartColor,
    NftPart,
)
from app.generation_nft_db.models.rarities import Rarity
from app.generation_nft_db.repositories.users import create_user
from app.generation_nft_db.schemas.users import UserCreate
from app.generation_nft_db.scripts.queries import (
    PLAYER_OTHERS_STATS_VALUES,
    PLAYER_POSITION_STATS_VALUES,
    PLAYER_POSITIONS,
)
from app.settings import settings
from app.utils import check_files

warnings.filterwarnings("ignore")


class Fixtures:
    """Classe pour appliquer les données fixes dans la base de données."""

    def __init__(self, reset: bool = False):
        """Initialise le classe Fixtures.

        Args:
            reset (bool, optional): supprime les données au lieu de les ajouter. Défaut à False.
        """
        self.db = next(get_db())
        self.reset = reset

    def csv_to_dict(
        self, filename: str, parse_dates: Union[list, bool] = False
    ) -> pd.DataFrame:
        """Converti un fichier CSV en dictionnaire python.

        Args:
            filename (str): nom du fichier csv.
            parse_dates (Union[list, bool], optional): liste des champs dates. Défaut à False.

        Raises:
            PronochainException: le fichier csv n'a pas été trouvé.

        Returns:
            pd.DataFrame: dictionnaire python avec les données.
        """
        try:
            return pd.read_csv(
                f"{settings.FIXTURE_FILES_PATH}/csv/{filename}.csv",
                delimiter=";",
                parse_dates=parse_dates,
                encoding="utf-8",
                keep_default_na=False,
            ).to_dict("record")
        except FileNotFoundError:
            error_message = f"Le fichier de fixture {filename} n'a pas été trouvé."
            logger_api.error(error_message)
            raise PronochainException(error_message)

    def add_stat_types(self, table: str, **_):
        """Ajouter les stat types.

        Args:
            table (str): nom de la table.
        """
        print("|-- START ADD STAT TYPES --|")
        data = self.csv_to_dict(table)

        stat_types_models = [
            StatType(code=stat_type.get("code"), value=stat_type.get("value"))
            for stat_type in data
            if not bool(stat_type.get("type"))
        ]
        add_multiple_into_database(self.db, stat_types_models)
        stats_models = []

        positions_models = self.db.query(Position).all()

        for stat in tqdm(data):
            if bool(types := stat.get("type")):
                stat_types = [
                    next(
                        stat_type_model
                        for stat_type_model in stat_types_models
                        if stat_type_model.code == int(type)
                    )
                    for type in types.split(",")
                ]
                stats_models.append(
                    Stat(
                        code=stat.get("code"), value=stat.get("value"), types=stat_types
                    )
                )

        add_multiple_into_database(self.db, stats_models)

        stats_positions = [
            stat_position
            for stat_position in data
            if bool(stat_position.get("positions_codes"))
        ]
        for stat_position in stats_positions:
            stat_model = next(
                stat_model
                for stat_model in stats_models
                if stat_model.code == stat_position.get("code")
            )
            position_models = [
                position_model
                for position_model in positions_models
                if str(position_model.code)
                in stat_position.get("positions_codes").split(",")
            ]
            stat_model.positions = position_models
            self.db.flush()

        print("|-- END ADD STAT TYPES --|")

    def add_positions(self, table: str, **_):
        """Ajouter les positions.

        Args:
            table (str): nom de la table.
        """
        print("|-- START ADD POSITIONS --|")
        data = self.csv_to_dict(table)

        elements_models = self.db.query(Element).all()
        position_types_models = []
        for position_type in data:
            if not bool(position_type.get("type")):
                try:
                    element = next(
                        element_model
                        for element_model in elements_models
                        if str(element_model.code) == position_type.get("element_code")
                    )
                except Exception:
                    element = None
                position_types_models.append(
                    PositionType(
                        code=position_type.get("code"),
                        abbreviation=position_type.get("abbreviation"),
                        value=position_type.get("value"),
                        element=element,
                    )
                )

        add_multiple_into_database(self.db, position_types_models)
        positions_models = []

        for position in tqdm(data):
            if bool(type := position.get("type")):
                position_type = next(
                    position_types_model
                    for position_types_model in position_types_models
                    if position_types_model.code == int(type)
                )
                positions_models.append(
                    Position(
                        code=position.get("code"),
                        abbreviation=position.get("abbreviation"),
                        value=position.get("value"),
                        type=position_type,
                    )
                )

        add_multiple_into_database(self.db, positions_models)
        print("|-- END ADD POSITIONS --|")

    def add_countries(self, table: str, nft_storage: Storage, **_):
        """Ajouter les pays.

        Args:
            table (str): nom de la table.
            nft_storage (Storage): classe pour stocker sur nft.storage.
        """
        print("|-- START ADD COUNTRIES --|")
        data = self.csv_to_dict(table)
        country_flag_path = f"{settings.FIXTURE_FILES_PATH}/pictures/flags"

        countries_models = []
        for country in tqdm(data):
            if settings.STORE_NFT_PART:
                with open(
                    f"{country_flag_path}/{country.get('code').lower()}.png", "rb"
                ) as country_flag_file:
                    response = nft_storage.add(country_flag_file)
                    countries_models.append(
                        Country(
                            code=country.get("code"),
                            value=country.get("value"),
                            cid=response.value.cid,
                            filename=f"{country.get('code').lower()}.png",
                        )
                    )

                    country_flag_file.close()
            else:
                countries_models.append(
                    Country(
                        code=country.get("code"),
                        value=country.get("value"),
                        cid=None,
                        filename=None,
                    )
                )

        add_multiple_into_database(self.db, countries_models)
        print("|-- END ADD COUNTRIES --|")

    def add_divisions(self, table: str, **_):
        """Ajouter les divisions.

        Args:
            table (str): nom de la table.
        """
        print("|-- START ADD DIVISIONS --|")
        data = self.csv_to_dict(table)

        countries_models = self.db.query(Country).all()
        divisions_models = []

        for division in tqdm(data):
            country = next(
                country_model
                for country_model in countries_models
                if re.sub("\s", "", country_model.value.lower())
                == re.sub("\s", "", division.get("country").lower())
            )
            divisions_models.append(
                Division(
                    code=division.get("code"),
                    name=division.get("name"),
                    country=country,
                )
            )

        add_multiple_into_database(self.db, divisions_models)
        print("|-- END ADD DIVISIONS --|")

    def add_rarities(self, table: str, **_):
        """Ajouter les raretés.

        Args:
            table (str): nom de la table.
        """
        print("|-- START ADD RARITIES --|")
        data = self.csv_to_dict(table)

        rarities_models = [
            Rarity(
                code=rarity.get("code"),
                name=rarity.get("name"),
                percentage=rarity.get("percentage"),
            )
            for rarity in tqdm(data)
        ]

        add_multiple_into_database(self.db, rarities_models)
        print("|-- END ADD RARITIES --|")

    def add_clubs(self, table: str, **_):
        """Ajouter les clubs.

        Args:
            table (str): nom de la table.
        """
        print("|-- START ADD CLUBS --|")
        data = self.csv_to_dict(table)

        countries_models = self.db.query(Country).all()
        divisions_models = self.db.query(Division).all()
        colors_models = self.db.query(Color).all()
        clubs_models = []

        for club in tqdm(data):
            try:
                country = next(
                    country_model
                    for country_model in countries_models
                    if re.sub("\s", "", country_model.value.lower())
                    == re.sub("\s", "", club.get("country").lower())
                )
            except Exception:
                country = None
            try:
                division = next(
                    division_model
                    for division_model in divisions_models
                    if division_model.code == int(club.get("division_code"))
                )
            except Exception:
                division = None

            club_first_color = club.get("first_color")
            if club_first_color != "":
                try:
                    first_color = next(
                        color_model
                        for color_model in colors_models
                        if color_model.hex == club_first_color
                    )
                except Exception:
                    first_color = Color(hex=club_first_color)
            else:
                first_color = Color(hex="#010101")

            add_into_database(self.db, first_color)
            colors_models.append(first_color)

            club_second_color = club.get("second_color")
            if club_second_color != "":
                try:
                    second_color = next(
                        color_model
                        for color_model in colors_models
                        if color_model.hex == club_second_color
                    )
                except Exception:
                    second_color = Color(hex=club_second_color)
            else:
                second_color = Color(hex="#FEFEFE")

            add_into_database(self.db, second_color)
            colors_models.append(second_color)

            clubs_models.append(
                Club(
                    code=club.get("code"),
                    name=club.get("name"),
                    country=country,
                    division=division,
                    first_color=first_color,
                    second_color=second_color,
                )
            )

        add_multiple_into_database(self.db, clubs_models)
        print("|-- END ADD CLUBS --|")

    def add_names(self, data: list):
        """Ajouter les noms.

        Args:
            data (list): liste des noms.
        """
        name_types_models = [
            NameType(code=name_type.get("code"), value=name_type.get("value"))
            for name_type in data
            if bool(name_type.get("code"))
        ]

        add_multiple_into_database(self.db, name_types_models)

        names_models = [
            Name(value=name.get("value"), type=name_types_models[0])
            for name in data
            if not bool(name.get("code"))
        ]

        add_multiple_into_database(self.db, names_models)

    def add_first_names(self, table: str, **_):
        """Ajout les prénoms.

        Args:
            table (str): nom de la table.
        """
        print("|-- START ADD FIRST NAMES --|")
        data = self.csv_to_dict(table)

        self.add_names(data)
        print("|-- END ADD FIRST NAMES --|")

    def add_last_names(self, table: str, **_):
        """Ajouter les nom de familles.

        Args:
            table (str): nom de la table.
        """
        print("|-- START ADD LAST NAMES --|")
        data = self.csv_to_dict(table)

        self.add_names(data)
        print("|-- END ADD LAST NAMES --|")

    def add_players(self, table: str, parse_dates: list, nft_storage: Storage, **_):
        """Ajouter les joueurs.

        Args:
            table (str): nom de la table.
            parse_dates (list): liste des colonnes de dates.
            nft_storage (Storage): classe pour stocker sur nft.storage.
        """
        print("|-- START ADD PLAYERS --|")
        data = self.csv_to_dict(table, parse_dates)
        if settings.LIMIT_PLAYER:
            data = data[:1000]

        print("|-- GENERATING BASE58 --|")
        players_code = [
            {
                "code": player.get("code"),
                "base58": nft_storage.convert_to_base58(
                    f"{settings.FIXTURE_FILES_PATH}/pictures/players/{player.get('code')}.png"
                ),
            }
            for player in tqdm(data)
        ]
        print("|-- BASE58 GENERATED --|")
        players_cid = nft_storage.get_cid(players_code)

        countries_models = self.db.query(Country).all()
        positions_models = self.db.query(Position).all()
        stats_models = self.db.query(Stat).all()

        first_names_models = (
            self.db.query(Name)
            .join(NameType)
            .filter(NameType.code == NameTypeCode.FIRST_NAME.value)
            .all()
        )
        last_names_models = (
            self.db.query(Name)
            .join(NameType)
            .filter(NameType.code == NameTypeCode.LAST_NAME.value)
            .all()
        )
        clubs_models = self.db.query(Club).all()

        for player in tqdm(data):
            try:
                cid_index = next(
                    index
                    for (index, player_cid) in enumerate(players_cid.files)
                    if player_cid.code == player.get("code")
                )
                cid = players_cid.files[cid_index].cid
                del players_cid.files[cid_index]
            except Exception:
                cid = None

            countries = [
                country_model
                for country_model in countries_models
                if re.sub("\s", "", country_model.value.lower())
                in re.sub("\s", "", player.get("country").lower()).split("/")
            ]
            positions = [
                position_model
                for position_model in positions_models
                if position_model.abbreviation.lower()
                in re.split(r"\/|,\s", player.get("position").lower())
            ]

            try:
                first_name_model = next(
                    first_name_model
                    for first_name_model in first_names_models
                    if re.sub("\s", "", first_name_model.value.lower())
                    == re.sub("\s", "", player.get("first_name").lower())
                )
            except Exception:
                first_name_model = None

            last_name_model = next(
                last_name_model
                for last_name_model in last_names_models
                if re.sub("\s", "", last_name_model.value.lower())
                == re.sub("\s", "", player.get("last_name").lower())
            )
            club_model = next(
                clubs_model
                for clubs_model in clubs_models
                if clubs_model.code == player.get("club_code")
            )

            player_model = Player(
                code=player.get("code"),
                first_name=first_name_model,
                last_name=last_name_model,
                age=player.get("age"),
                birth=player.get("birth"),
                height=player.get("height"),
                weight=player.get("weight"),
                club=club_model,
                countries=countries,
                positions=positions,
                cid=cid,
                filename=None,
            )

            add_into_database(self.db, player_model)

            player_stats_models = [
                PlayerStat(
                    stat=stat_model,
                    player=player_model,
                    value=player.get(str(stat_model.code)),
                )
                for stat_model in stats_models
            ]

            add_multiple_into_database(self.db, player_stats_models)

        print("|-- END ADD PLAYERS --|")

    def add_users(self, **_):
        """Ajouter les utilisateurs."""
        print("|-- START ADD USER --|")
        user = UserCreate(
            login=settings.FIRST_SUPER_USER_LOGIN,
            password=settings.FIRST_SUPER_USER_PASSWORD,
            is_superuser=True,
        )
        create_user(self.db, user=user, commit=False)
        print("|-- END ADD USER --|")

    def add_nft_parts(self, table: str, **_):
        """Ajouter les parties du NFT.

        Args:
            table (str): nom de la table.
        """
        print("|-- START ADD NFT PARTS --|")
        data = self.csv_to_dict(table)

        nft_parts_models = [
            NftPart(code=nft_part.get("code"), name=nft_part.get("name"))
            for nft_part in data
        ]

        add_multiple_into_database(self.db, nft_parts_models)

        print("|-- END ADD NFT PARTS --|")

    def add_face_parts(self, table: str, **_):
        """Ajouter les parties du visages.

        Args:
            table (str): nom de la table.
        """
        print("|-- START ADD FACE PARTS --|")
        data = self.csv_to_dict(table)

        face_parts_models = [
            FacePart(code=face_part.get("code"), name=face_part.get("name"))
            for face_part in data
        ]

        add_multiple_into_database(self.db, face_parts_models)

        print("|-- END ADD FACE PARTS --|")

    def add_element_types(self, table: str, **_):
        """Ajouter les types d'éléments.

        Args:
            table (str): nom de la table.
        """
        print("|-- START ADD ELEMENT TYPES --|")
        data = self.csv_to_dict(table)

        element_types_models = [
            ElementType(code=element_type.get("code"), name=element_type.get("name"))
            for element_type in data
        ]

        add_multiple_into_database(self.db, element_types_models)

        print("|-- END ADD ELEMENT TYPES --|")

    def add_elements(self, table: str, nft_storage: Storage, **_):
        """Ajouter les éléments.

        Args:
            table (str): nom de la table.
            nft_storage (Storage): classe pour stocker sur nft.storage.
        """
        print("|-- START ADD ELEMENTS --|")
        data = self.csv_to_dict(table)
        pictures_path = f"{settings.FIXTURE_FILES_PATH}/pictures"

        nft_parts_models = self.db.query(NftPart).all()
        element_types_models = self.db.query(ElementType).all()
        rarity_models = self.db.query(Rarity).all()
        elements_models = []

        elements_with_parent = [
            element for element in data if bool(element.get("parent_code"))
        ]

        for element in tqdm(data):
            nft_part = next(
                nft_part_model
                for nft_part_model in nft_parts_models
                if nft_part_model.code == element.get("nft_part_code")
            )
            element_type = next(
                element_type_model
                for element_type_model in element_types_models
                if element_type_model.code == element.get("element_type_code")
            )

            try:
                rarity = next(
                    rarity_model
                    for rarity_model in rarity_models
                    if rarity_model.code == int(element.get("rarity_code"))
                )
            except Exception:
                rarity = None

            if settings.STORE_NFT_PART:
                filename = element.get("name")
                paths = filename.split("_")[:-1]
                with open(
                    f"{pictures_path}/{'/'.join(paths)}/{filename}.png", "rb"
                ) as element_file:
                    response = nft_storage.add(element_file)
                    elements_models.append(
                        Element(
                            code=element.get("code"),
                            name=element.get("name"),
                            nft_part=nft_part,
                            type=element_type,
                            cid=response.value.cid,
                            filename=f"{filename}.png",
                            rarity=rarity,
                        )
                    )
                    element_file.close()
            else:
                elements_models.append(
                    Element(
                        code=element.get("code"),
                        name=element.get("name"),
                        nft_part=nft_part,
                        type=element_type,
                        cid=None,
                        filename=None,
                        rarity=rarity,
                    )
                )

        add_multiple_into_database(self.db, elements_models)

        for element in elements_with_parent:
            element_model = next(
                element_model
                for element_model in elements_models
                if element_model.code == int(element.get("code"))
            )
            element_parent_model = next(
                element_model
                for element_model in elements_models
                if element_model.code == int(element.get("parent_code"))
            )
            element_model.parent = element_parent_model
            self.db.flush()

        print("|-- END ADD ELEMENTS --|")

    def add_colors(self, table: str, **_):
        """Ajouter les couleurs.

        Args:
            table (str): nom de la table.
        """
        print("|-- START ADD COLORS --|")
        data = self.csv_to_dict(table)

        nft_parts_models = self.db.query(NftPart).all()
        rarity_models = self.db.query(Rarity).all()
        colors_models = []

        for color in tqdm(data):
            try:
                nft_part = next(
                    nft_part_model
                    for nft_part_model in nft_parts_models
                    if nft_part_model.code == int(color.get("nft_part_code"))
                )
            except Exception:
                nft_part = None

            try:
                rarity = next(
                    rarity_model
                    for rarity_model in rarity_models
                    if rarity_model.code == int(color.get("rarity_code"))
                )
            except Exception:
                rarity = None

            colors_models.append(
                Color(
                    id=color.get("id"),
                    hex=color.get("hex"),
                    nft_part=nft_part,
                    rarity=rarity,
                )
            )

        add_multiple_into_database(self.db, colors_models)

        print("|-- END ADD COLORS --|")

    def add_face_parts_colors(self, table: str, **_):
        """Ajouter les possibilités de couleurs pour les parties du visages.

        Args:
            table (str): nom de la table.
        """
        print("|-- START ADD FACE PARTS COLORS --|")
        data = self.csv_to_dict(table)

        face_parts_models = self.db.query(FacePart).all()
        colors_models = self.db.query(Color).all()
        face_parts_colors_models = []

        for face_part_color in tqdm(data):
            depend_face_parts_colors = face_part_color.get("depend_face_parts_colors")

            face_part = next(
                face_part_model
                for face_part_model in face_parts_models
                if face_part_model.code == face_part_color.get("face_part_code")
            )
            color = next(
                color_model
                for color_model in colors_models
                if color_model.id == face_part_color.get("color_id")
            )

            face_parts_colors_models.append(
                FacePartColor(
                    id=face_part_color.get("id"), face_part=face_part, color=color
                )
            )

        add_multiple_into_database(self.db, colors_models)

        depended_face_part_color = [
            face_part_color
            for face_part_color in data
            if bool(face_part_color.get("depend_face_parts_colors"))
        ]
        for face_part_color in depended_face_part_color:
            depended_face_part_color = next(
                face_part_color_model
                for face_part_color_model in face_parts_colors_models
                if face_part_color_model.id == face_part_color.get("id")
            )
            depend_face_parts_colors = [
                face_part_color_model
                for face_part_color_model in face_parts_colors_models
                if str(face_part_color_model.id)
                in face_part_color.get("depend_face_parts_colors").split(",")
            ]
            depended_face_part_color.depend_face_part_colors = depend_face_parts_colors
            self.db.flush()

        print("|-- END ADD FACE PARTS COLORS --|")

    def calcul_player_rarities(self):
        """Calculer la rareté d'un joueur."""
        rarities = self.db.query(Rarity).all()
        players = self.db.execute(PLAYER_POSITIONS)
        players_stats = []
        players_stats_sum_by_positions = []
        print("|-- START CALCUL PLAYER RARITIES --|")
        for player in tqdm(players.mappings()):
            position_code = player.get("position_codes")[0]
            position_stats_values = self.db.execute(
                PLAYER_POSITION_STATS_VALUES,
                {"position_code": position_code, "player_id": player.get("player_id")},
            ).mappings()
            others_stats_values = self.db.execute(
                PLAYER_OTHERS_STATS_VALUES, {"player_id": player.get("player_id")}
            ).mappings()
            player_stats_sum = sum(
                position_stats_values.all()[0].get("values")
                + others_stats_values.all()[0].get("values")
            )
            try:
                player_stat_sum_by_position = next(
                    players_stats_sum_by_position
                    for players_stats_sum_by_position in players_stats_sum_by_positions
                    if players_stats_sum_by_position.get("position_code")
                    == position_code
                )
                player_stat_sum_by_position = {
                    **player_stat_sum_by_position,
                    "values": player_stat_sum_by_position.get("values").append(
                        player_stats_sum
                    ),
                }
            except Exception:
                players_stats_sum_by_positions.append(
                    {"position_code": position_code, "values": [player_stats_sum]}
                )
            players_stats.append(
                {
                    "player_id": player.get("player_id"),
                    "position_code": position_code,
                    "stat": player_stats_sum,
                }
            )

        rarities_positions = []
        for players_stats_sum_by_position in tqdm(players_stats_sum_by_positions):
            values = players_stats_sum_by_position.get("values")
            minimum_value = min(values)
            values = [value - minimum_value for value in values]
            maximum_value = max(values)

            positions_rarities = []
            for rarity in rarities[:-1]:
                rarity_value = maximum_value - int(
                    (rarity.percentage * maximum_value) / 100
                )
                positions_rarities.append(
                    {
                        "rarity_id": rarity.id,
                        "value": rarity_value - 1
                        if rarity_value == maximum_value
                        else rarity_value,
                    }
                )
            positions_rarities.append(
                {"rarity_id": rarities[-1].id, "value": maximum_value}
            )

            rarities_positions.append(
                {
                    "position_code": players_stats_sum_by_position.get("position_code"),
                    "minimum_value": minimum_value,
                    "rarity_steps": positions_rarities,
                }
            )

        for player in tqdm(players_stats):
            player_id = player.get("player_id")
            position_code = player.get("position_code")
            rarity_position = next(
                rarities_position
                for rarities_position in rarities_positions
                if rarities_position.get("position_code") == position_code
            )
            player_stat = player.get("stat") - rarity_position.get("minimum_value")
            try:
                player_rarity_id = [
                    rarity_step.get("rarity_id")
                    for rarity_step in rarity_position.get("rarity_steps")
                    if rarity_step.get("value") <= player_stat
                ][-1]
            except IndexError:
                player_rarity_id = rarity_position.get("rarity_steps")[0].get(
                    "rarity_id"
                )
            self.db.query(Player).filter(Player.id == player_id).update(
                {"rarity_id": player_rarity_id}, synchronize_session=False
            )

        print("|-- END CALCUL PLAYER RARITIES --|")

    def set_fixtures(self):
        """Applique les fixtures ou les supprimes."""
        nft_storage = Storage()
        if self.reset:
            print("|-- START REMOVE DATA --|")
            with self.db.begin():
                # ORDER AS IMPORTANCE
                model_with_files = [
                    Player,
                    Country,
                    Element,
                ]
                if settings.STORE_NFT_PART:
                    for model_with_file in model_with_files:
                        model_results = (
                            self.db.query(model_with_file)
                            .filter(model_with_file.cid is not None)
                            .all()
                        )
                        for model_result in tqdm(model_results):
                            try:
                                nft_storage.delete(model_result.cid)
                            except Exception:
                                pass

                models = [
                    User,
                    model_with_files[0],
                    Name,
                    NameType,
                    Club,
                    Division,
                    model_with_files[1],
                    Position,
                    PositionType,
                    Stat,
                    StatType,
                    NftPart,
                    FacePart,
                    ElementType,
                    model_with_files[-1],
                    Color,
                    FacePartColor,
                    Rarity,
                ]
                for model in tqdm(models):
                    self.db.query(model).delete()
                self.db.commit()
            print("|-- END REMOVE DATA --|")
        else:
            if settings.DOWNLOAD_DATA:
                check_files()
            with self.db.begin():
                for fixture in FIXTURES_ORDER:
                    getattr(self, f"add_{fixture.get('table')}")(
                        **fixture, nft_storage=nft_storage
                    )
                self.calcul_player_rarities()
                self.db.commit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--delete",
        action="store_true",
        help="Supprime toutes les données.",
    )
    parser.add_argument(
        "-r",
        "--rarity",
        action="store_true",
        help="Supprime toutes les données.",
    )
    args = parser.parse_args()

    fixtures = Fixtures(reset=args.delete)
    if args.rarity:
        fixtures.calcul_player_rarities()
    else:
        fixtures.set_fixtures()
