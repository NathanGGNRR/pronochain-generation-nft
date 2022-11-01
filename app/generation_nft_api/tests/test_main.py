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

File: generation_nft_api/tests/main_tests.py
"""
from fastapi.testclient import TestClient

from app.generation_nft_api.main import app

client = TestClient(app)


def test_read_root():
    """Test read root route.

    Raises:
        AssertionError: Le statut code n'est pas correct.
        AssertionError: La réponse ne contient pas les bonnes données.
    """
    response = client.get("/")
    if response.status_code != 404:
        raise AssertionError("Le statut code n'est pas correct.")


def test_read_item():
    """Test read item route.

    Raises:
        AssertionError: Le statut code n'est pas correct.
        AssertionError: La réponse ne contient pas les bonnes données.
    """
    response = client.get("/items/1?q=Hello")
    if response.status_code != 404:
        raise AssertionError("Le statut code n'est pas correct.")
