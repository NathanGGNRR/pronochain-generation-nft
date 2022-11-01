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

File: app/generation_nft/libraries/face/tilt_learning/tilt_learning.py
"""

import warnings
from pathlib import Path

import gdown
import requests
from joblib import load as load_model
from sklearn.feature_extraction import DictVectorizer

from app import logger
from app.exceptions import PronochainException
from app.generation_nft.libraries.face.tilt_learning.constants import (
    ADA_BOOST_CLASSIFIER,
    BAGGING_CLASSIFIER,
    GRADIENT_BOOSTING_CLASSIFIER,
    K_NEIGHBORS_CLASSIFIER,
    MLP_CLASSIFIER,
    PRE_TRAINED_MODELS,
    RANDOM_FOREST_CLASSIFIER,
    STACKING_CLASSIFIER,
    SVC_CLASSIFIER,
    VOTING_CLASSIFIER,
)
from app.generation_nft.libraries.face.tilt_learning.tilt_learning_data import (
    TiltLearningData,
)
from app.settings import settings

warnings.filterwarnings("ignore")


class TiltLearning(TiltLearningData):
    """Classe permettant de créer, entrainer et/ou utiliser le tilt learning model (vérification si la tête regarde en face)."""

    def __init__(self):
        """Initialise la classe pour vérifier la direction du visage."""
        TiltLearningData.__init__(self)

        self.model_folder_path = (
            f"{settings.GENERATION_NFT_PATH}/libraries/face/tilt_learning/pre_trained"
        )
        self.model_path = f"{self.model_folder_path}/tilt_learning"
        self.list_models = [
            {"model": ADA_BOOST_CLASSIFIER, "name": "abc"},
            {"model": BAGGING_CLASSIFIER, "name": "bc"},
            {"model": GRADIENT_BOOSTING_CLASSIFIER, "name": "gdc"},
            {"model": K_NEIGHBORS_CLASSIFIER, "name": "knc"},
            {"model": RANDOM_FOREST_CLASSIFIER, "name": "rfc"},
            {"model": SVC_CLASSIFIER, "name": "svc"},
            {"model": MLP_CLASSIFIER, "name": "mc"},
            {"model": STACKING_CLASSIFIER, "name": "sc"},
            {"model": VOTING_CLASSIFIER, "name": "vc"},
        ]
        self.download_missing_models()

    def is_looking_front(self, datasets: dict) -> bool:
        """Fonction pour déterminer si le visage regarde en face et non pas en haut/en bas/à droite ou à gauche.

        Args:
            datasets (dict): données.

        Returns:
            bool: regarde en face ?
        """
        predictions = []

        for dict_model in self.list_models:
            try:
                model = load_model(
                    f"{self.model_path}_{dict_model.get('name')}_model.pkl"
                )
                datasets_array = DictVectorizer().fit_transform(datasets).toarray()
                predictions.append(model.predict(datasets_array)[0])
            except (AttributeError, ModuleNotFoundError):
                continue
        prediction_result = max(set(predictions), key=predictions.count)

        return prediction_result == 2

    def download_missing_models(self):
        """Télécharge les modèles manquants.

        Raises:
            PronochainException: url du modèle invalide.
        """
        for pre_trained_model in PRE_TRAINED_MODELS:
            file = pre_trained_model.get("file")
            file_path = f"{self.model_folder_path}/{file}"
            if not Path(file_path).is_file():
                try:
                    gdown.download(pre_trained_model.get("url"), file_path)
                except requests.exceptions.MissingSchema:
                    error_message = f"Le modèle {file} n'a pas la bonne URL. Impossible de télécharger le modèle pré-entrainé."
                    logger.error(error_message)
                    raise PronochainException(error_message)
