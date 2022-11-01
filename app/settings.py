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

File: app/settings.py
"""
import secrets
from typing import List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, Field, validator


class GlobalSettings(BaseSettings):
    """Global settings."""

    # Global constants
    BASE_DIR: str = "app"
    GENERATION_NFT_PATH: str = f"{BASE_DIR}/generation_nft"
    GENERATION_NFT_API_PATH: str = f"{BASE_DIR}/generation_nft_api"
    GENERATION_NFT_DB: str = f"{BASE_DIR}/generation_nft_db"

    # Environnement variables
    DEBUG: Optional[bool] = Field(None, env="DEBUG")
    API_IP: Optional[str] = Field(None, env="API_IP")
    API_PORT: Optional[int] = Field(None, env="API_PORT")
    STORE_NFT_PART: Optional[bool] = Field(None, env="STORE_NFT_PART")
    DOWNLOAD_DATA: Optional[bool] = Field(None, env="DOWNLOAD_DATA")
    CHECK_MIGRATIONS: Optional[bool] = Field(None, env="CHECK_MIGRATIONS")
    FROM_DOCKER: Optional[bool] = Field(None, env="FROM_DOCKER")
    LIMIT_PLAYER: Optional[bool] = Field(None, env="LIMIT_PLAYER")

    # DB
    POSTGRES_USER: Optional[str] = Field("postgres", env="POSTGRES_USER")
    POSTGRES_PASSWORD: Optional[str] = Field("postgres", env="POSTGRES_PASSWORD")
    POSTGRES_SERVER: Optional[str] = Field("localhost", env="POSTGRES_SERVER")
    POSTGRES_PORT: Optional[int] = Field("5436", env="POSTGRES_PORT")
    POSTGRES_DB: Optional[str] = Field("generation-nft", env="POSTGRES_DB")

    # Models
    DEPLOY_PROTOTXT_URL_ID: Optional[str] = Field(None, env="DEPLOY_PROTOTXT_URL_ID")
    CAFFEMODEL_URL_ID: Optional[str] = Field(None, env="CAFFEMODEL_URL_ID")
    ABC_MODEL_URL_ID: Optional[str] = Field(None, env="ABC_MODEL_URL_ID")
    BC_MODEL_URL_ID: Optional[str] = Field(None, env="BC_MODEL_URL_ID")
    GDC_MODEL_URL_ID: Optional[str] = Field(None, env="GDC_MODEL_URL_ID")
    KNC_MODEL_URL_ID: Optional[str] = Field(None, env="KNC_MODEL_URL_ID")
    MC_MODEL_URL_ID: Optional[str] = Field(None, env="MC_MODEL_URL_ID")
    RFC_MODEL_URL_ID: Optional[str] = Field(None, env="RFC_MODEL_URL_ID")
    SC_MODEL_URL_ID: Optional[str] = Field(None, env="SC_MODEL_URL_ID")
    SVC_MODEL_URL_ID: Optional[str] = Field(None, env="SVC_MODEL_URL_ID")
    VC_MODEL_URL_ID: Optional[str] = Field(None, env="VC_MODEL_URL_ID")
    FACE_PARTS_URL_ID: Optional[str] = Field(None, env="FACE_PARTS_URL_ID")
    RESNET_URL: Optional[str] = Field(None, env="RESNET_URL")

    # Fixtures
    FIXTURES_CLUBS_URL_ID: Optional[str] = Field(None, env="FIXTURES_CLUBS_URL_ID")
    FIXTURES_COUNTRIES_URL_ID: Optional[str] = Field(
        None, env="FIXTURES_COUNTRIES_URL_ID"
    )
    FIXTURES_DIVISIONS_URL_ID: Optional[str] = Field(
        None, env="FIXTURES_DIVISIONS_URL_ID"
    )
    FIXTURES_FIRST_NAMES_URL_ID: Optional[str] = Field(
        None, env="FIXTURES_FIRST_NAMES_URL_ID"
    )
    FIXTURES_LAST_NAMES_URL_ID: Optional[str] = Field(
        None, env="FIXTURES_LAST_NAMES_URL_ID"
    )
    FIXTURES_PLAYERS_URL_ID: Optional[str] = Field(None, env="FIXTURES_PLAYERS_URL_ID")
    FIXTURES_POSITIONS_URL_ID: Optional[str] = Field(
        None, env="FIXTURES_POSITIONS_URL_ID"
    )
    FIXTURES_STAT_TYPES_URL_ID: Optional[str] = Field(
        None, env="FIXTURES_STAT_TYPES_URL_ID"
    )
    FIXTURES_PICTURES_URL_ID: Optional[str] = Field(
        None, env="FIXTURES_PICTURES_URL_ID"
    )
    FIXTURES_COLORS_URL_ID: Optional[str] = Field(None, env="FIXTURES_COLORS_URL_ID")
    FIXTURES_ELEMENT_TYPES_URL_ID: Optional[str] = Field(
        None, env="FIXTURES_ELEMENT_TYPES_URL_ID"
    )
    FIXTURES_ELEMENTS_URL_ID: Optional[str] = Field(
        None, env="FIXTURES_ELEMENTS_URL_ID"
    )
    FIXTURES_FACE_PARTS_COLORS_URL_ID: Optional[str] = Field(
        None, env="FIXTURES_FACE_PARTS_COLORS_URL_ID"
    )
    FIXTURES_FACE_PARTS_URL_ID: Optional[str] = Field(
        None, env="FIXTURES_FACE_PARTS_URL_ID"
    )
    FIXTURES_NFT_PARTS_URL_ID: Optional[str] = Field(
        None, env="FIXTURES_NFT_PARTS_URL_ID"
    )
    FIXTURES_PLAYERS_ID: Optional[str] = Field(None, env="FIXTURES_PLAYERS_ID")
    FIXTURES_RARITIES_URL_ID: Optional[str] = Field(
        None, env="FIXTURES_RARITIES_URL_ID"
    )
    FIXTURES_CARD_FONT_ID: Optional[str] = Field(None, env="FIXTURES_CARD_FONT_ID")
    FIXTURE_FILES_PATH: str = f"{GENERATION_NFT_DB}/scripts/data"

    # Storage
    NFT_STORAGE_API_KEY: Optional[str] = Field(None, env="NFT_STORAGE_API_KEY")
    NFT_STORAGE_URL: Optional[str] = Field(None, env="NFT_STORAGE_URL")
    NFT_STORAGE_GATEWAY: Optional[str] = Field(None, env="NFT_STORAGE_GATEWAY")

    # FastAPI
    PROJECT_NAME: str = "Pronochain Generation NFT"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # CAR API
    CAR_API_SERVER: Optional[str] = Field(None, env="CAR_API_SERVER")

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        """Configure les CORS origins.

        Args:
            v (Union[str, List[str]]): v.

        Raises:
            ValueError: value error.

        Returns:
            Union[List[str], str]: v.
        """
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Authentication
    FIRST_SUPER_USER_LOGIN: Optional[str] = Field(None, env="FIRST_SUPER_USER_LOGIN")
    FIRST_SUPER_USER_PASSWORD: Optional[str] = Field(
        None, env="FIRST_SUPER_USER_PASSWORD"
    )
    SECURITY_ALGORITHM: str = "HS256"
    SECURITY_SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    AUTH_DISABLED: bool = False

    # Face parsing
    FACE_PARSING_MODEL_FILE: str = "face_parts.pth"
    RESNET_FILE: str = "resnet18.pth"
    FACE_PARSING_MODEL_PATH: str = (
        f"{GENERATION_NFT_PATH}/libraries/face/face_parsing/pre_trained"
    )

    # Face detect
    FACE_DETECT_MODELS_PATH: str = (
        f"{GENERATION_NFT_PATH}/libraries/face/face_detect/pre_trained"
    )
    FACE_DETECT_DEPLOY_FILE: str = "deploy.prototxt.txt"
    FACE_DETECT_CAFFE_FILE: str = "face_detect.caffemodel"

    # Tilt learning
    TILT_LEARNING_MODEL_FILES: List[str] = [
        "abc",
        "bc",
        "gdc",
        "knc",
        "mc",
        "rfc",
        "sc",
        "svc",
        "vc",
    ]
    TILT_LEARNING_MODELS_PATH: str = (
        f"{GENERATION_NFT_PATH}/libraries/face/tilt_learning/pre_trained"
    )

    # Migrations
    ALEMBIC_MIGRATION_PATH: str = "alembic/versions"
    ALEMBIC_CONFIG_PATH: str = "alembic.ini"

    class Config:
        """Charge le fichier environnement avec python-dotenv."""

        env_file: str = "app/.env"


class DevelopmentSettings(GlobalSettings):
    """Development settings."""

    class Config:
        """Charge le fichier environnement avec python-dotenv de développement."""

        env_prefix: str = "DEV_"


class ProductionSettings(GlobalSettings):
    """Production settings."""

    class Config:
        """Charge le fichier environnement avec python-dotenv de production."""

        env_prefix: str = "PROD_"


class FactorySettings:
    """Retourne une instance d'une classe Settings en fonction de la variable d'environnement DEBUG."""

    def __init__(self, debug: Optional[bool]):
        """Intilisation de la classe FactorySettings.

        Args:
            debug (Optional[bool]): détermine si l'application est lancée sur l'environnement de production ou l'environnement de développement
        """
        self.debug = debug

    def __call__(self) -> Union[DevelopmentSettings, ProductionSettings]:
        """Fonction appelée lorsque l'on utilise la classe.

        Returns:
            Union[DevelopmentSettings, ProductionSettings]: retourne les variables d'environnement.
        """
        return DevelopmentSettings() if self.debug else ProductionSettings()


settings = FactorySettings(GlobalSettings().DEBUG)()
