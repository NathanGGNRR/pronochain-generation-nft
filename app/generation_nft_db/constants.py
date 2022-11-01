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

File: app/generation_nft_db/constants.py
"""
from enum import Enum

from app.settings import settings


class FixtureEnum(Enum):
    """Fixture name liste.

    Args:
        Enum (enum): enumération.
    """

    CLUBS = "clubs"
    COLORS = "colors"
    COUNTRIES = "countries"
    DIVISIONS = "divisions"
    ELEMENT_TYPES = "element_types"
    ELEMENTS = "elements"
    FACE_PARTS_COLORS = "face_parts_colors"
    FACE_PARTS = "face_parts"
    FIRST_NAMES = "first_names"
    LAST_NAMES = "last_names"
    NFT_PARTS = "nft_parts"
    PLAYERS = "players"
    POSITIONS = "positions"
    STAT_TYPES = "stat_types"
    USERS = "users"
    PICTURES = "pictures"
    PLAYERS_CAR = "players"
    RARITIES = "rarities"
    CARD_FONT = "card_font"


FIXTURES = [
    {
        "url": f"https://drive.google.com/u/1/uc?id={settings.FIXTURES_CLUBS_URL_ID}&export=download",
        "file": f"{FixtureEnum.CLUBS.value}.csv",
        "parent_path": f"{settings.FIXTURE_FILES_PATH}/csv",
    },
    {
        "url": f"https://drive.google.com/u/1/uc?id={settings.FIXTURES_COUNTRIES_URL_ID}&export=download",
        "file": f"{FixtureEnum.COUNTRIES.value}.csv",
        "parent_path": f"{settings.FIXTURE_FILES_PATH}/csv",
    },
    {
        "url": f"https://drive.google.com/u/1/uc?id={settings.FIXTURES_DIVISIONS_URL_ID}&export=download",
        "file": f"{FixtureEnum.DIVISIONS.value}.csv",
        "parent_path": f"{settings.FIXTURE_FILES_PATH}/csv",
    },
    {
        "url": f"https://drive.google.com/u/1/uc?id={settings.FIXTURES_FIRST_NAMES_URL_ID}&export=download",
        "file": f"{FixtureEnum.FIRST_NAMES.value}.csv",
        "parent_path": f"{settings.FIXTURE_FILES_PATH}/csv",
    },
    {
        "url": f"https://drive.google.com/u/1/uc?id={settings.FIXTURES_LAST_NAMES_URL_ID}&export=download",
        "file": f"{FixtureEnum.LAST_NAMES.value}.csv",
        "parent_path": f"{settings.FIXTURE_FILES_PATH}/csv",
    },
    {
        "url": f"https://drive.google.com/u/1/uc?id={settings.FIXTURES_PLAYERS_URL_ID}&export=download",
        "file": f"{FixtureEnum.PLAYERS.value}.csv",
        "parent_path": f"{settings.FIXTURE_FILES_PATH}/csv",
    },
    {
        "url": f"https://drive.google.com/u/1/uc?id={settings.FIXTURES_POSITIONS_URL_ID}&export=download",
        "file": f"{FixtureEnum.POSITIONS.value}.csv",
        "parent_path": f"{settings.FIXTURE_FILES_PATH}/csv",
    },
    {
        "url": f"https://drive.google.com/u/1/uc?id={settings.FIXTURES_STAT_TYPES_URL_ID}&export=download",
        "file": f"{FixtureEnum.STAT_TYPES.value}.csv",
        "parent_path": f"{settings.FIXTURE_FILES_PATH}/csv",
    },
    {
        "url": f"https://drive.google.com/u/1/uc?id={settings.FIXTURES_PICTURES_URL_ID}&export=download",
        "zip": f"{FixtureEnum.PICTURES.value}.zip",
        "parent_path": f"{settings.FIXTURE_FILES_PATH}",
    },
    {
        "url": f"https://drive.google.com/u/1/uc?id={settings.FIXTURES_COLORS_URL_ID}&export=download",
        "file": f"{FixtureEnum.COLORS.value}.csv",
        "parent_path": f"{settings.FIXTURE_FILES_PATH}/csv",
    },
    {
        "url": f"https://drive.google.com/u/1/uc?id={settings.FIXTURES_ELEMENT_TYPES_URL_ID}&export=download",
        "file": f"{FixtureEnum.ELEMENT_TYPES.value}.csv",
        "parent_path": f"{settings.FIXTURE_FILES_PATH}/csv",
    },
    {
        "url": f"https://drive.google.com/u/1/uc?id={settings.FIXTURES_ELEMENTS_URL_ID}&export=download",
        "file": f"{FixtureEnum.ELEMENTS.value}.csv",
        "parent_path": f"{settings.FIXTURE_FILES_PATH}/csv",
    },
    {
        "url": f"https://drive.google.com/u/1/uc?id={settings.FIXTURES_FACE_PARTS_COLORS_URL_ID}&export=download",
        "file": f"{FixtureEnum.FACE_PARTS_COLORS.value}.csv",
        "parent_path": f"{settings.FIXTURE_FILES_PATH}/csv",
    },
    {
        "url": f"https://drive.google.com/u/1/uc?id={settings.FIXTURES_FACE_PARTS_URL_ID}&export=download",
        "file": f"{FixtureEnum.FACE_PARTS.value}.csv",
        "parent_path": f"{settings.FIXTURE_FILES_PATH}/csv",
    },
    {
        "url": f"https://drive.google.com/u/1/uc?id={settings.FIXTURES_NFT_PARTS_URL_ID}&export=download",
        "file": f"{FixtureEnum.NFT_PARTS.value}.csv",
        "parent_path": f"{settings.FIXTURE_FILES_PATH}/csv",
    },
    {
        "url": f"https://drive.google.com/u/1/uc?id={settings.FIXTURES_PLAYERS_ID}&export=download&confirm=t",
        "zip": f"{FixtureEnum.PLAYERS.value}.zip",
        "parent_path": f"{settings.FIXTURE_FILES_PATH}/pictures",
    },
    {
        "url": f"https://drive.google.com/u/1/uc?id={settings.FIXTURES_RARITIES_URL_ID}&export=download",
        "file": f"{FixtureEnum.RARITIES.value}.csv",
        "parent_path": f"{settings.FIXTURE_FILES_PATH}/csv",
    },
    {
        "url": f"https://drive.google.com/u/1/uc?id={settings.FIXTURES_CARD_FONT_ID}&export=download",
        "file": f"{FixtureEnum.CARD_FONT.value}.ttf",
        "parent_path": f"{settings.FIXTURE_FILES_PATH}/fonts",
    },
]

FIXTURES_ORDER = [
    {"table": FixtureEnum.RARITIES.value},
    {"table": FixtureEnum.NFT_PARTS.value},
    {"table": FixtureEnum.COLORS.value},
    {"table": FixtureEnum.ELEMENT_TYPES.value},
    {"table": FixtureEnum.ELEMENTS.value},
    {"table": FixtureEnum.POSITIONS.value},
    {"table": FixtureEnum.STAT_TYPES.value},
    {"table": FixtureEnum.COUNTRIES.value},
    {"table": FixtureEnum.DIVISIONS.value},
    {"table": FixtureEnum.CLUBS.value},
    {"table": FixtureEnum.FIRST_NAMES.value},
    {"table": FixtureEnum.LAST_NAMES.value},
    {"table": FixtureEnum.PLAYERS.value, "parse_dates": [7]},
    {"table": FixtureEnum.USERS.value},
    {"table": FixtureEnum.FACE_PARTS.value},
    {"table": FixtureEnum.FACE_PARTS_COLORS.value},
]


class NameTypeCode(Enum):
    """Name type code liste.

    Args:
        Enum (enum): enumération.
    """

    FIRST_NAME = 1
    LAST_NAME = 2


class StatTypeCode(Enum):
    """Stat type code liste.

    Args:
        Enum (enum): enumération.
    """

    GOALKEEPING = 1
    MENTAL = 2
    PHYSICAL = 3
    TECHNICAL = 4


class StatCode(Enum):
    """Stat code liste.

    Args:
        Enum (enum): enumération.
    """

    AERIAL_ABILITY = 5
    COMMAND_OF_AREA = 6
    COMMUNICATION = 7
    ECCENTRICITY = 8
    FIRST_TOUCH = 9
    HANDLING = 10
    KICKING = 11
    ONE_ON_ONES = 12
    PASSING = 13
    TENDENCY_TO_PUNCH = 14
    REFLEXES = 15
    RUSHING_OUT = 16
    THROWING = 17
    CORNERS = 18
    CROSSING = 19
    DRIBBLING = 20
    FINISHING = 21
    FREEKICKS = 22
    HEADING = 23
    LONG_SHOTS = 24
    LONG_THROWS = 25
    MARKING = 26
    PENALTY_TAKING = 27
    TACKLING = 28
    TECHNIQUE = 29
    AGGRESSION = 30
    ANTICIPATION = 31
    BRAVERY = 32
    COMPOSURE = 33
    CONCENTRATION = 34
    DECISIONS = 35
    DETERMINATION = 36
    FLAIR = 37
    LEADERSHIP = 38
    OFF_THE_BALL = 39
    POSITIONING = 40
    TEAMWORK = 41
    VISION = 42
    WORKRATE = 43
    CONSISTENCY = 44
    DIRTINESS = 45
    VERSATILITY = 46
    AMBITION = 47
    LOYALTY = 48
    PRESSURE = 49
    PROFESSIONAL = 50
    ACCELERATION = 51
    AGILITY = 52
    BALANCE = 53
    JUMPING = 54
    NATURAL_FITNESS = 55
    PACE = 56
    STAMINA = 57
    STRENGTH = 58
    ADAPTABILITY = 59


class PositionTypeCode(Enum):
    """Position type code liste.

    Args:
        Enum (enum): enumération.
    """

    DEFENDER = 1
    MIDFIELDER = 2
    ATTACKER = 3
    GOALKEEPER = 4


class PositionCode(Enum):
    """Position code liste.

    Args:
        Enum (enum): enumération.
    """

    ATTACKING_MIDFIELDER = 5
    ATTACKING_MIDFIELDER_CENTER = 6
    ATTACKING_MIDFIELDER_LEFT = 7
    ATTACKING_MIDFIELDER_LEFT_CENTER = 8
    ATTACKING_MIDFIELDER_RIGHT = 9
    ATTACKING_MIDFIELDER_RIGHT_CENTER = 10
    ATTACKING_MIDFIELDER_RIGHT_LEFT = 11
    ATTACKING_MIDFIELDER_RIGHT_LEFT_CENTER = 12
    DEFEND = 13
    CENTER_BACK = 14
    LEFT_BACK = 15
    LEFT_CENTER_BACK = 16
    RIGHT_BACK = 17
    RIGHT_CENTER_BACK = 18
    RIGHT_LEFT_BACK = 19
    RIGHT_LEFT_CENTER_BACK = 20
    DEFENSIVE_MIDFIELDER = 21
    CENTER_FORWARD = 22
    GOALKEEPER = 23
    CENTER_MIDFIELDER = 24
    LEFT_MIDFIELDER = 25
    LEFT_CENTER_MIDFIELDER = 26
    RIGHT_MIDFIELDER = 27
    RIGHT_CENTER_MIDFIELDER = 28
    RIGHT_LEFT_MIDFIELDER = 29
    RIGHT_LEFT_CENTER_MIDFIELDER = 30
    STRIKER = 31
    WING_BACK = 32
    WING_BACK_LEFT = 33
    WING_BACK_RIGHT = 34
    WING_BACK_RIGHT_LEFT = 35


class RarityCode(Enum):
    """Rarity code liste.

    Args:
        Enum (enum): enumération.
    """

    COMMON = 1
    UNCOMMUN = 2
    RARE = 3
    VERY_RARE = 4
    SUPER_RARE = 5
    HYPER_RARE = 6
    EPIC = 7
    LEGENDARY = 8


class CardShapeCode(Enum):
    """Card shape code liste.

    Args:
        Enum (enum): enumération.
    """

    SHAPE_1 = "1"
    SHAPE_2 = "2"
    SHAPE_3 = "3"


class CardPatternCode(Enum):
    """Card pattern code liste.

    Args:
        Enum (enum): enumération.
    """

    PATTERN_1 = "13"
    PATTERN_2 = "14"


class CardColor(Enum):
    """Card color liste.

    Args:
        Enum (enum): enumération.
    """

    COMMON = "#2A2766"
    UNCOMMON = "#662763"
    RARE = "#662A27"
    VERY_RARE = "#664927"


class ShirtPatternCode(Enum):
    """Shirt pattern code liste.

    Args:
        Enum (enum): enumération.
    """

    PATTERN_1 = "15"
    PATTERN_2 = "16"
    PATTERN_3 = "17"
    PATTERN_4 = "18"


class ShirtCrestShapeCode(Enum):
    """Shirt crest shape code liste.

    Args:
        Enum (enum): enumération.
    """

    SHAPE_1 = "4"
    SHAPE_2 = "5"
    SHAPE_3 = "6"
    SHAPE_4 = "7"
    SHAPE_5 = "8"
    SHAPE_6 = "9"
    SHAPE_7 = "10"
    SHAPE_8 = "11"
    SHAPE_9 = "12"


class ShirtCrestPatternCode(Enum):
    """Shirt crest pattern code liste.

    Args:
        Enum (enum): enumération.
    """

    PATTERN_1 = "19"
    PATTERN_2 = "20"
    PATTERN_3 = "21"
    PATTERN_4 = "22"
    PATTERN_5 = "23"
    PATTERN_6 = "24"
    PATTERN_7 = "25"


class ShirtCrestContentCode(Enum):
    """Shirt crest content code liste.

    Args:
        Enum (enum): enumération.
    """

    CONTENT_1 = "26"
    CONTENT_2 = "27"
    CONTENT_3 = "28"
    CONTENT_4 = "29"
    CONTENT_5 = "30"
    CONTENT_6 = "31"
    CONTENT_7 = "32"
    CONTENT_8 = "33"
    CONTENT_9 = "34"
    CONTENT_10 = "47"
    CONTENT_11 = "48"
    CONTENT_12 = "49"
    CONTENT_13 = "50"
    CONTENT_14 = "51"
    CONTENT_15 = "52"
    CONTENT_16 = "53"
    CONTENT_17 = "54"
    CONTENT_18 = "55"
    CONTENT_19 = "56"
    CONTENT_20 = "57"
    CONTENT_21 = "58"
    CONTENT_22 = "59"
    CONTENT_23 = "60"
    CONTENT_24 = "61"
    CONTENT_25 = "62"
    CONTENT_26 = "63"
    CONTENT_27 = "64"


class CountryCode(Enum):
    """Country code liste.

    Args:
        Enum (enum): enumération.
    """

    ANDORRA = "AD"
    UNITED_ARAB_EMIRATES = "AE"
    AFGHANISTAN = "AF"
    ANTIGUA_AND_BARBUDA = "AG"
    ANGUILLA = "AI"
    ALBANIA = "AL"
    ARMENIA = "AM"
    ANGOLA = "AO"
    ANTARCTICA = "AQ"
    ARGENTINA = "AR"
    AMERICAN_SAMOA = "AS"
    AUSTRIA = "AT"
    AUSTRALIA = "AU"
    ARUBA = "AW"
    ÅLAND_ISLANDS = "AX"
    AZERBAIJAN = "AZ"
    BOSNIA_AND_HERZEGOVINA = "BA"
    BARBADOS = "BB"
    BANGLADESH = "BD"
    BELGIUM = "BE"
    BURKINA_FASO = "BF"
    BULGARIA = "BG"
    BAHRAIN = "BH"
    BURUNDI = "BI"
    BENIN = "BJ"
    SAINT_BARTHÉLEMY = "BL"
    BERMUDA = "BM"
    BRUNEI_DARUSSALAM = "BN"
    BOLIVIA = "BO"
    BONAIRE = "BQ"
    BRAZIL = "BR"
    BAHAMAS = "BS"
    BHUTAN = "BT"
    BOUVET_ISLAND = "BV"
    BOTSWANA = "BW"
    BELARUS = "BY"
    BELIZE = "BZ"
    CANADA = "CA"
    COCOS_ISLANDS = "CC"
    CONGO_DEMOCRATIC = "CD"
    CENTRAL_AFRICAN_REPUBLIC = "CF"
    CONGO = "CG"
    SWITZERLAND = "CH"
    CÔTE_IVOIRE = "CI"
    COOK_ISLANDS = "CK"
    CHILE = "CL"
    CAMEROON = "CM"
    CHINA = "CN"
    COLOMBIA = "CO"
    COSTA_RICA = "CR"
    CUBA = "CU"
    CABO_VERDE = "CV"
    CURAÇAO = "CW"
    CHRISTMAS_ISLAND = "CX"
    CYPRUS = "CY"
    CZECH_REPUBLIC = "CZ"
    GERMANY = "DE"
    DJIBOUTI = "DJ"
    DENMARK = "DK"
    DOMINICA = "DM"
    DOMINICAN_REPUBLIC = "DO"
    ALGERIA = "DZ"
    ECUADOR = "EC"
    ESTONIA = "EE"
    EGYPT = "EG"
    WESTERN_SAHARA = "EH"
    ERITREA = "ER"
    SPAIN = "ES"
    ETHIOPIA = "ET"
    FINLAND = "FI"
    FIJI = "FJ"
    FALKLAND_ISLANDS = "FK"
    MICRONESIA = "FM"
    FAROE_ISLANDS = "FO"
    FRANCE = "FR"
    GABON = "GA"
    UNITED_KINGDOM = "GB"
    GRENADA = "GD"
    GEORGIA = "GE"
    FRENCH_GUIANA = "GF"
    GUERNSEY = "GG"
    GHANA = "GH"
    GIBRALTAR = "GI"
    GREENLAND = "GL"
    GAMBIA = "GM"
    GUINEA = "GN"
    GUADELOUPE = "GP"
    EQUATORIAL_GUINEA = "GQ"
    GREECE = "GR"
    SOUTH_GEORGIA = "GS"
    GUATEMALA = "GT"
    GUAM = "GU"
    GUINEA_BISSAU = "GW"
    GUYANA = "GY"
    HONG_KONG = "HK"
    HEARD_ISLAND = "HM"
    HONDURAS = "HN"
    CROATIA = "HR"
    HAITI = "HT"
    HUNGARY = "HU"
    INDONESIA = "ID"
    IRELAND = "IE"
    ISRAEL = "IL"
    ISLE_OF_MAN = "IM"
    INDIA = "IN"
    BRITISH_INDIAN_OCEAN_TERRITORY = "IO"
    IRAQ = "IQ"
    IRAN = "IR"
    ICELAND = "IS"
    ITALY = "IT"
    JERSEY = "JE"
    JAMAICA = "JM"
    JORDAN = "JO"
    JAPAN = "JP"
    KENYA = "KE"
    KYRGYZSTAN = "KG"
    CAMBODIA = "KH"
    KIRIBATI = "KI"
    COMOROS = "KM"
    SAINT_KITTS_AND_NEVIS = "KN"
    NORTH_KOREA = "KP"
    SOUTH_KOREA = "KR"
    KUWAIT = "KW"
    CAYMAN_ISLANDS = "KY"
    KAZAKHSTAN = "KZ"
    LAOS = "LA"
    LEBANON = "LB"
    SAINT_LUCIA = "LC"
    LIECHTENSTEIN = "LI"
    SRI_LANKA = "LK"
    LIBERIA = "LR"
    LESOTHO = "LS"
    LITHUANIA = "LT"
    LUXEMBOURG = "LU"
    LATVIA = "LV"
    LIBYA = "LY"
    MOROCCO = "MA"
    MONACO = "MC"
    MOLDOVA = "MD"
    MONTENEGRO = "ME"
    SAINT_MARTIN = "MF"
    MADAGASCAR = "MG"
    MARSHALL_ISLANDS = "MH"
    NORTH_MACEDONIA = "MK"
    MALI = "ML"
    MYANMAR = "MM"
    MONGOLIA = "MN"
    MACAO = "MO"
    NORTHERN_MARIANA_ISLANDS = "MP"
    MARTINIQUE = "MQ"
    MAURITANIA = "MR"
    MONTSERRAT = "MS"
    MALTA = "MT"
    MAURITIUS = "MU"
    MALDIVES = "MV"
    MALAWI = "MW"
    MEXICO = "MX"
    MALAYSIA = "MY"
    MOZAMBIQUE = "MZ"
    NAMIBIA = "NA"
    NEW_CALEDONIA = "NC"
    NIGER = "NE"
    NORFOLK_ISLAND = "NF"
    NIGERIA = "NG"
    NICARAGUA = "NI"
    NETHERLANDS = "NL"
    NORWAY = "NO"
    NEPAL = "NP"
    NAURU = "NR"
    NIUE = "NU"
    NEW_ZEALAND = "NZ"
    OMAN = "OM"
    PANAMA = "PA"
    PERU = "PE"
    FRENCH_POLYNESIA = "PF"
    PAPUA_NEW_GUINEA = "PG"
    PHILIPPINES = "PH"
    PAKISTAN = "PK"
    POLAND = "PL"
    SAINT_PIERRE_AND_MIQUELON = "PM"
    PITCAIRN = "PN"
    PUERTO_RICO = "PR"
    PALESTINE = "PS"
    PORTUGAL = "PT"
    PALAU = "PW"
    PARAGUAY = "PY"
    QATAR = "QA"
    RÉUNION = "RE"
    ROMANIA = "RO"
    SERBIA = "RS"
    RUSSIA = "RU"
    RWANDA = "RW"
    SAUDI_ARABIA = "SA"
    SOLOMON_ISLANDS = "SB"
    SEYCHELLES = "SC"
    SUDAN = "SD"
    SWEDEN = "SE"
    SINGAPORE = "SG"
    SAINT_HELENA = "SH"
    SLOVENIA = "SI"
    SVALBARD_AND_JAN_MAYEN = "SJ"
    SLOVAKIA = "SK"
    SIERRA_LEONE = "SL"
    SAN_MARINO = "SM"
    SENEGAL = "SN"
    SOMALIA = "SO"
    SURINAME = "SR"
    SOUTH_SUDAN = "SS"
    SAO_TOME_AND_PRINCIPE = "ST"
    EL_SALVADOR = "SV"
    SINT_MAARTEN = "SX"
    SYRIA = "SY"
    ESWATINI = "SZ"
    TURKS_AND_CAICOS_ISLANDS = "TC"
    CHAD = "TD"
    FRENCH_SOUTHERN_TERRITORIES = "TF"
    TOGO = "TG"
    THAILAND = "TH"
    TAJIKISTAN = "TJ"
    TOKELAU = "TK"
    TIMOR_LESTE = "TL"
    TURKMENISTAN = "TM"
    TUNISIA = "TN"
    TONGA = "TO"
    EAST_TIMOR = "TP"
    TURKEY = "TR"
    TRINIDAD_AND_TOBAGO = "TT"
    TUVALU = "TV"
    TAIWAN = "TW"
    TANZANIA = "TZ"
    UKRAINE = "UA"
    UGANDA = "UG"
    UNITED_STATES_MINOR_OUTLYING_ISLANDS = "UM"
    UNITED_STATES = "US"
    URUGUAY = "UY"
    UZBEKISTAN = "UZ"
    HOLY_SEE = "VA"
    SAINT_VINCENT_AND_THE_GRENADINES = "VC"
    VENEZUELA = "VE"
    VIRGIN_ISLANDS_BRITISH = "VG"
    VIRGIN_ISLANDS_US = "VI"
    VIETNAM = "VN"
    VANUATU = "VU"
    WALLIS_AND_FUTUNA = "WF"
    SAMOA = "WS"
    KOSOVO = "XK"
    YEMEN = "YE"
    MAYOTTE = "YT"
    SOUTH_AFRICA = "ZA"
    ZAMBIA = "ZM"
    ZIMBABWE = "ZW"
    INCONNU = "ZZ"


class SkinColor(Enum):
    """Skin color liste.

    Args:
        Enum (enum): enumération.
    """

    COLOR_1 = "#FFE0BD"
    COLOR_2 = "#EBD3C5"
    COLOR_3 = "#FFCF94"
    COLOR_4 = "#D7B6A5"
    COLOR_5 = "#C48466"
    COLOR_6 = "#BA957D"
    COLOR_7 = "#A08A83"
    COLOR_8 = "#9F7967"
    COLOR_9 = "#CC8F60"
    COLOR_10 = "#714937"
    COLOR_11 = "#5B452D"
    COLOR_12 = "#6A3A26"
    COLOR_13 = "#492816"
    COLOR_14 = "#321B0F"


class HairColor(Enum):
    """Hair color liste.

    Args:
        Enum (enum): enumération.
    """

    COLOR_1 = "#AA8866"
    COLOR_2 = "#DEBE99"
    COLOR_3 = "#241C11"
    COLOR_4 = "#4F1A00"
    COLOR_5 = "#9A3300"


class EyesColor(Enum):
    """Eyes color liste.

    Args:
        Enum (enum): enumération.
    """

    COLOR_1 = "#343321"
    COLOR_2 = "#1E8C97"
    COLOR_3 = "#515254"
    COLOR_4 = "#3C492F"
    COLOR_5 = "#304B69"
    COLOR_6 = "#606568"
    COLOR_7 = "#96421D"
    COLOR_8 = "#2E1C1C"
    COLOR_9 = "#9A9ABE"
