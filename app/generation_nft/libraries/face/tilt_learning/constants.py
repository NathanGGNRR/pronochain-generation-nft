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

File: app/generation_nft/libraries/face/tilt_learning/constants.py
"""

from sklearn.ensemble import (
    AdaBoostClassifier,
    BaggingClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
    StackingClassifier,
    VotingClassifier,
)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from app.settings import settings

RANDOM_FOREST_CLASSIFIER = RandomForestClassifier(
    n_estimators=100, max_features="sqrt", criterion="gini", max_depth=8
)

ADA_BOOST_CLASSIFIER = AdaBoostClassifier(n_estimators=100)

BAGGING_CLASSIFIER = BaggingClassifier(
    DecisionTreeClassifier(max_depth=5),
    max_features=1.0,
    max_samples=0.1,
    n_estimators=100,
)

GRADIENT_BOOSTING_CLASSIFIER = GradientBoostingClassifier(
    n_estimators=100,
    criterion="friedman_mse",
    learning_rate=0.2,
    loss="exponential",
)

K_NEIGHBORS_CLASSIFIER = KNeighborsClassifier(
    leaf_size=2, n_neighbors=5, p=1, weights="distance"
)

SVC_CLASSIFIER = SVC(degree=1, gamma=1e-4, C=1000)

MLP_CLASSIFIER = MLPClassifier()

VOTING_CLASSIFIER = VotingClassifier(
    [
        (
            "RANDOM_FOREST_CLASSIFIER",
            RANDOM_FOREST_CLASSIFIER,
        ),
        ("ADA_BOOST_CLASSIFIER", ADA_BOOST_CLASSIFIER),
        (
            "BAGGING_CLASSIFIER",
            BAGGING_CLASSIFIER,
        ),
        (
            "GRADIENT_BOOSTING_CLASSIFIER",
            GRADIENT_BOOSTING_CLASSIFIER,
        ),
        ("K_NEIGHBORS_CLASSIFIER", K_NEIGHBORS_CLASSIFIER),
        ("SVC_CLASSIFIER", SVC_CLASSIFIER),
        ("MLP_CLASSIFIER", MLP_CLASSIFIER),
    ]
)

STACKING_CLASSIFIER = StackingClassifier(
    [
        (
            "RANDOM_FOREST_CLASSIFIER",
            RANDOM_FOREST_CLASSIFIER,
        ),
        ("ADA_BOOST_CLASSIFIER", ADA_BOOST_CLASSIFIER),
        (
            "BAGGING_CLASSIFIER",
            BAGGING_CLASSIFIER,
        ),
        (
            "GRADIENT_BOOSTING_CLASSIFIER",
            GRADIENT_BOOSTING_CLASSIFIER,
        ),
        ("K_NEIGHBORS_CLASSIFIER", K_NEIGHBORS_CLASSIFIER),
        ("SVC_CLASSIFIER", SVC_CLASSIFIER),
        ("MLP_CLASSIFIER", MLP_CLASSIFIER),
    ]
)

PRE_TRAINED_MODELS = [
    {
        "url": f"https://drive.google.com/u/1/uc?id={settings.ABC_MODEL_URL_ID}&export=download",
        "file": f"tilt_learning_{settings.TILT_LEARNING_MODEL_FILES[0]}_model.pkl",
        "parent_path": settings.TILT_LEARNING_MODELS_PATH,
    },
    {
        "url": f"https://drive.google.com/u/1/uc?id={settings.BC_MODEL_URL_ID}&export=download",
        "file": f"tilt_learning_{settings.TILT_LEARNING_MODEL_FILES[1]}_model.pkl",
        "parent_path": settings.TILT_LEARNING_MODELS_PATH,
    },
    {
        "url": f"https://drive.google.com/u/1/uc?id={settings.GDC_MODEL_URL_ID}&export=download",
        "file": f"tilt_learning_{settings.TILT_LEARNING_MODEL_FILES[2]}_model.pkl",
        "parent_path": settings.TILT_LEARNING_MODELS_PATH,
    },
    {
        "url": f"https://drive.google.com/u/1/uc?id={settings.KNC_MODEL_URL_ID}&export=download",
        "file": f"tilt_learning_{settings.TILT_LEARNING_MODEL_FILES[3]}_model.pkl",
        "parent_path": settings.TILT_LEARNING_MODELS_PATH,
    },
    {
        "url": f"https://drive.google.com/u/1/uc?id={settings.MC_MODEL_URL_ID}&export=download",
        "file": f"tilt_learning_{settings.TILT_LEARNING_MODEL_FILES[4]}_model.pkl",
        "parent_path": settings.TILT_LEARNING_MODELS_PATH,
    },
    {
        "url": f"https://drive.google.com/u/1/uc?id={settings.RFC_MODEL_URL_ID}&export=download",
        "file": f"tilt_learning_{settings.TILT_LEARNING_MODEL_FILES[5]}_model.pkl",
        "parent_path": settings.TILT_LEARNING_MODELS_PATH,
    },
    {
        "url": f"https://drive.google.com/u/1/uc?id={settings.SC_MODEL_URL_ID}&export=download",
        "file": f"tilt_learning_{settings.TILT_LEARNING_MODEL_FILES[6]}_model.pkl",
        "parent_path": settings.TILT_LEARNING_MODELS_PATH,
    },
    {
        "url": f"https://drive.google.com/u/1/uc?id={settings.SVC_MODEL_URL_ID}&export=download",
        "file": f"tilt_learning_{settings.TILT_LEARNING_MODEL_FILES[7]}_model.pkl",
        "parent_path": settings.TILT_LEARNING_MODELS_PATH,
    },
    {
        "url": f"https://drive.google.com/u/1/uc?id={settings.VC_MODEL_URL_ID}&export=download",
        "file": f"tilt_learning_{settings.TILT_LEARNING_MODEL_FILES[8]}_model.pkl",
        "parent_path": settings.TILT_LEARNING_MODELS_PATH,
    },
]
