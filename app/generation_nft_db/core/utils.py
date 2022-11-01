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

File: app/generation_nft_db/core/utils.py
"""
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import logger_api


def add_multiple_into_database(db: Session, models: list):
    """Ajouter plusieurs informations dans la base de donnée.

    Args:
        db (Session): session de la base de donnée.
        models (list): informations.

    Raises:
        e: impossible d'ajouter les informations.
    """
    try:
        db.add_all(models)
        db.flush()
    except IntegrityError as e:
        logger_api.error(e)
        raise e


def add_into_database(db: Session, model: object):
    """Ajouter une information dans la base de donnée.

    Args:
        db (Session): session de la base de donnée.
        model (object): information.

    Raises:
        e: impossible d'ajouter l'information.
    """
    try:
        db.add(model)
        db.flush()
    except IntegrityError as e:
        logger_api.error(e)
        raise e
