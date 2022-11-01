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

File: app/generation_nft/tests/test_utils.py
"""

from app.generation_nft.utils import get_mean, get_percentage, set_positive


def test_get_mean():
    """Test la fonction pour récupérer la moyenne entre plusieurs valeurs.

    Raises:
        AssertionError: La fonction pour récupérer la moyenne entre deux nombres ne fonctionne pas.
    """
    list = [4, 8]
    if get_mean(list) != 6.0:
        raise AssertionError(
            "La fonction pour récupérer la moyenne entre deux nombres ne fonctionne pas."
        )


def test_get_percentage():
    """Test la fonction pour récupérer le pourcentage entre deux valeurs.

    Raises:
        AssertionError: La fonction pour récupérer le pourcentage entre un nombre et un autre nombre ne fonctionne pas.
    """
    first_value = 10.0
    second_value = 100.0
    if get_percentage(first_value, second_value) != 10.0:
        raise AssertionError(
            "La fonction pour récupérer le pourcentage entre un nombre et un autre nombre ne fonctionne pas."
        )


def test_set_positive():
    """Test la fonction pour rendre une valeur négative positive.

    Raises:
        AssertionError: La fonction pour rendre un nombre négatif positif ne fonctionne pas.
    """
    value = -10.0
    if set_positive(value) != 10.0:
        raise AssertionError(
            "La fonction pour rendre un nombre négatif positif ne fonctionne pas."
        )
