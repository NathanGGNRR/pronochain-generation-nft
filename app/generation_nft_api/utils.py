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

File: app/generation_nft_api/utils.py
"""

from typing import List, Optional

from app.generation_nft_db.models.players import Player
from app.generation_nft_db.schemas.players import PlayerNestedOut


def convert_players_names(players: List[Player]) -> List[PlayerNestedOut]:
    """Converti les noms des joueurs.

    Args:
        players (List[Player]): joueurs.

    Returns:
        List[PlayerNestedOut]: liste de joueurs.
    """
    return [
        PlayerNestedOut(
            id=player.id,
            first_name=player.first_name.value,
            last_name=player.last_name.value,
            code=player.code,
            age=player.age,
            birth=player.birth,
            club=player.club,
            height=player.height,
            weight=player.weight,
            countries=player.countries,
            positions=player.positions,
            stats=player.stats,
        )
        for player in players
    ]


def convert_player_names(player: Player) -> Optional[PlayerNestedOut]:
    """Converti le nom d'un joueur.

    Args:
        player (Player): joueur.

    Returns:
        Optional[PlayerNestedOut]: joueur.
    """
    if player is not None:
        return PlayerNestedOut(
            id=player.id,
            first_name=player.first_name.value,
            last_name=player.last_name.value,
            code=player.code,
            age=player.age,
            birth=player.birth,
            club=player.club,
            height=player.height,
            weight=player.weight,
            countries=player.countries,
            positions=player.positions,
            stats=player.stats,
        )
    return None
