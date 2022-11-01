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

File: app/launch.py
"""
import argparse

import uvicorn

from app.settings import settings
from app.utils import check_files, run_migrations


def uvicorn_configuration(is_dev: bool) -> dict:
    """Initialise la configuration du serveur uvicorn.

    Args:
        is_dev (bool): correspond à l'environnement de développement

    Raises:
        FileNotFoundError: DEBUG est égale à False alors que la solution est démarrée sur l'environnement de développement
        FileNotFoundError: DEBUG est égale à True alors que la solution est démarrée sur l'environnement de production

    Returns:
        dict: uvicorn paramètres
    """
    uvicorn_params = {"app": "app.generation_nft_api.main:app", "host": settings.API_IP}
    if is_dev:
        uvicorn_dev_params = {
            "port": 8000,
            "debug": True,
            "reload": True,
            "log_level": "debug",
        }

        if not settings.DEBUG:
            raise FileNotFoundError(
                "En mode développement, vous devez activer la variable d'environnement DEBUG (fichier .env). Redémarrer le conteneur Docker pour prendre en compte le changement."
            )

        uvicorn_params.update(uvicorn_dev_params)
    else:
        if settings.DEBUG:
            raise FileNotFoundError(
                "En mode production, vous devez désactiver la variable d'environnement DEBUG (fichier .env). Redémarrer le conteneur Docker pour prendre en compte le changement."
            )
    return uvicorn_params


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--dev",
        action="store_true",
        help="Démarrer le serveur en version développement.",
    )
    args = parser.parse_args()

    if settings.DOWNLOAD_DATA:
        check_files()

    if settings.CHECK_MIGRATIONS:
        run_migrations()

    uvicorn_params = uvicorn_configuration(args.dev)

    uvicorn.run(**uvicorn_params)
