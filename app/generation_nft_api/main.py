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

File: app/generation_nft_api/main.py
"""
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.generation_nft_api.routers import (
    clubs,
    countries,
    divisions,
    generation,
    login,
    names,
    nft_parts,
    players,
    positions,
    rarities,
    stats,
    users,
)
from app.settings import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(clubs.router)
app.include_router(countries.router)
app.include_router(divisions.router)
app.include_router(names.router)
app.include_router(nft_parts.router)
app.include_router(players.router)
app.include_router(positions.router)
app.include_router(stats.router)
app.include_router(login.router)
app.include_router(users.router)
app.include_router(rarities.router)
app.include_router(generation.router)


@app.get("/get_environment_variables")
def get_environment_variables() -> dict:
    """Test route API : get environment variables.

    Returns:
        dict: api port.
    """
    return settings.API_PORT


# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
