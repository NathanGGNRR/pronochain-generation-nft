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

File: app/generation_nft_db/scripts/queries.py
"""
from sqlalchemy.sql import text

PLAYER_POSITIONS = text(
    """
    SELECT pl.id as player_id, ARRAY_AGG(po.code) as position_codes
    FROM players pl
        JOIN players_positions pp ON pl.id = pp.player_id
        JOIN positions po ON pp.position_id = po.id
    GROUP BY pl.id
    """
)

PLAYER_POSITION_STATS_VALUES = text(
    """
    SELECT ARRAY_AGG(ps.value) AS values
    FROM players_stats ps
        JOIN stats s ON ps.stat_id = s.id
        JOIN stats_positions sp ON s.id = sp.stat_id
        JOIN positions p ON sp.position_id = p.id
    WHERE p.code = :position_code
    AND ps.player_id = :player_id;
    """
)

PLAYER_OTHERS_STATS_VALUES = text(
    """
    SELECT ARRAY_AGG(ps.value) AS values
    FROM players_stats ps
        JOIN stats s ON ps.stat_id = s.id
        JOIN stats_stat_types sst ON s.id = sst.stat_id
        JOIN stat_types st ON sst.type_id = st.id
    WHERE st.code IN (2, 3)
    AND ps.player_id = :player_id;
    """
)

MOUTH_COLOR_VALUE = text(
    """
    SELECT c2.hex
    FROM face_parts_colors                    fpc
             JOIN dependent_face_parts_colors dfpc ON fpc.id = dfpc.depend_face_part_color_id
             JOIN face_parts_colors           fpc2 ON fpc2.id = dfpc.face_part_color_id
             JOIN colors                      c2 ON c2.id = fpc2.color_id
    WHERE fpc.color_id = :skin_color_id;
    """
)

STAT_BY_TYPES = text(
    """
    SELECT ps.value
    FROM players_stats                  ps
             LEFT JOIN stats            s ON s.id = ps.stat_id
             LEFT JOIN stats_stat_types sst ON s.id = sst.stat_id
             LEFT JOIN stat_types       st ON sst.type_id = st.id
    WHERE st.code = :type_code
      AND player_id = :player_id
    """
)


STAT_BY_POSITIONS = text(
    """
    SELECT ps.value
    FROM players_stats                 ps
             LEFT JOIN stats           s ON s.id = ps.stat_id
             LEFT JOIN stats_positions sp ON s.id = sp.stat_id
             LEFT JOIN positions       p ON p.id = sp.position_id
    WHERE p.code = :position_code
      AND ps.player_id = :player_id
    """
)

FILTER_NAMES = text(
    """
    SELECT n.id id
    FROM names               n
             JOIN name_types nt ON nt.id = n.type_id
    WHERE nt.code = :type_code
    AND LOWER(n.value) = :name
    """
)
