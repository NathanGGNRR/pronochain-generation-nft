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

File: app/generation_nft/libraries/storage/models.py
"""
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel


class Pin(BaseModel):
    """Pin modèle.

    Args:
        BaseModel (BaseModel): modèle pydantic.
    """

    cid: Optional[str]
    name: Optional[str]
    meta: Optional[Dict[str, Any]]
    status: Optional[str]
    created: Optional[str]
    size: Optional[int]


class File(BaseModel):
    """File modèle.

    Args:
        BaseModel (BaseModel): modèle pydantic.
    """

    name: Optional[str]
    type: Optional[str]


class Deal(BaseModel):
    """Deal modèle.

    Args:
        BaseModel (BaseModel): modèle pydantic.
    """

    batchRootCid: Optional[str]
    lastChange: Optional[str]
    miner: Optional[str]
    network: Optional[str]
    pieceCid: Optional[str]
    status: Optional[str]
    statusText: Optional[str]
    chainDealID: Optional[int]
    dealActivation: Optional[str]
    dealExpiration: Optional[str]


class Value(BaseModel):
    """Value modèle.

    Args:
        BaseModel (BaseModel): modèle pydantic.
    """

    cid: Optional[str]
    size: Optional[int]
    created: Optional[str]
    type: Optional[str]
    scope: Optional[str]
    pin: Optional[Pin]
    files: Optional[List[File]]
    deals: Optional[List[Deal]]
    ipnft: Optional[str]
    url: Optional[str]
    data: Optional[dict]


class Error(BaseModel):
    """Error modèle.

    Args:
        BaseModel (BaseModel): modèle pydantic.
    """

    name: Optional[str]
    message: Optional[str]


class ResponseStorage(BaseModel):
    """ResponseStorage modèle.

    Args:
        BaseModel (BaseModel): modèle pydantic.
    """

    ok: Optional[bool]
    value: Optional[Union[List[Value], Value]]
    error: Optional[Error]
