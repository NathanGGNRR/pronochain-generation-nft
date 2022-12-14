# -*- coding: utf-8 -*-
"""Initial.

Revision ID: 4d3619cdbf13
Revises:
Create Date: 2022-04-13 19:57:48.923002

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "4d3619cdbf13"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Upgrade."""
    # ### commands auto generated by Alembic - please adjust! ###
    rarities_id = "rarities.id"
    stats_id = "stats.id"
    countries_id = "countries.id"
    colors_id = "colors.id"
    players_id = "players.id"

    op.create_table(
        "rarities",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("code", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("percentage", sa.REAL(precision=3), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_rarities_code"), "rarities", ["code"], unique=True)
    op.create_index(op.f("ix_rarities_id"), "rarities", ["id"], unique=False)
    op.create_table(
        "countries",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("code", sa.String(length=2), nullable=False),
        sa.Column("value", sa.String(length=255), nullable=False),
        sa.Column("cid", sa.String(length=255), nullable=True),
        sa.Column("filename", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_countries_code"), "countries", ["code"], unique=True)
    op.create_index(op.f("ix_countries_id"), "countries", ["id"], unique=False)
    op.create_table(
        "element_types",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("code", sa.SmallInteger(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_element_types_code"), "element_types", ["code"], unique=True
    )
    op.create_index(op.f("ix_element_types_id"), "element_types", ["id"], unique=False)
    op.create_table(
        "face_parts",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("code", sa.SmallInteger(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_face_parts_code"), "face_parts", ["code"], unique=True)
    op.create_index(op.f("ix_face_parts_id"), "face_parts", ["id"], unique=False)
    op.create_table(
        "name_types",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("code", sa.SmallInteger(), nullable=False),
        sa.Column("value", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_name_types_code"), "name_types", ["code"], unique=True)
    op.create_index(op.f("ix_name_types_id"), "name_types", ["id"], unique=False)
    op.create_table(
        "nft_parts",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("code", sa.SmallInteger(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_nft_parts_code"), "nft_parts", ["code"], unique=True)
    op.create_index(op.f("ix_nft_parts_id"), "nft_parts", ["id"], unique=False)
    op.create_table(
        "elements",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("code", sa.SmallInteger(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("nft_part_id", sa.Integer(), nullable=True),
        sa.Column("type_id", sa.Integer(), nullable=True),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.Column("cid", sa.String(length=255), nullable=True),
        sa.Column("filename", sa.String(length=255), nullable=True),
        sa.Column("rarity_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["nft_part_id"], ["nft_parts.id"], ondelete="cascade"),
        sa.ForeignKeyConstraint(["parent_id"], ["elements.id"], ondelete="cascade"),
        sa.ForeignKeyConstraint(["type_id"], ["element_types.id"], ondelete="cascade"),
        sa.ForeignKeyConstraint(["rarity_id"], [rarities_id], ondelete="cascade"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_elements_code"), "elements", ["code"], unique=True)
    op.create_index(op.f("ix_elements_id"), "elements", ["id"], unique=False)
    op.create_index(
        op.f("ix_elements_parent_id"), "elements", ["parent_id"], unique=False
    )
    op.create_table(
        "position_types",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("code", sa.SmallInteger(), nullable=False),
        sa.Column("abbreviation", sa.String(length=10), nullable=False),
        sa.Column("value", sa.String(length=255), nullable=False),
        sa.Column("element_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["element_id"], ["elements.id"], ondelete="cascade"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_position_types_code"), "position_types", ["code"], unique=True
    )
    op.create_index(
        op.f("ix_position_types_id"), "position_types", ["id"], unique=False
    )
    op.create_table(
        "positions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("code", sa.SmallInteger(), nullable=False),
        sa.Column("abbreviation", sa.String(length=10), nullable=False),
        sa.Column("value", sa.String(length=255), nullable=False),
        sa.Column("type_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["type_id"], ["position_types.id"], ondelete="cascade"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_positions_code"), "positions", ["code"], unique=True)
    op.create_index(op.f("ix_positions_id"), "positions", ["id"], unique=False)
    op.create_table(
        "stat_types",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("code", sa.SmallInteger(), nullable=False),
        sa.Column("value", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_stat_types_code"), "stat_types", ["code"], unique=True)
    op.create_index(op.f("ix_stat_types_id"), "stat_types", ["id"], unique=False)
    op.create_table(
        "stats",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("code", sa.SmallInteger(), nullable=False),
        sa.Column("value", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_stats_code"), "stats", ["code"], unique=True)
    op.create_index(op.f("ix_stats_id"), "stats", ["id"], unique=False)
    op.create_table(
        "stats_positions",
        sa.Column("stat_id", sa.Integer(), nullable=False),
        sa.Column("position_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["position_id"], ["positions.id"], ondelete="cascade"),
        sa.ForeignKeyConstraint(["stat_id"], [stats_id], ondelete="cascade"),
        sa.PrimaryKeyConstraint("stat_id", "position_id"),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("login", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_superuser", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("login"),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_table(
        "colors",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("hex", sa.String(length=7), nullable=False),
        sa.Column("nft_part_id", sa.Integer(), nullable=True),
        sa.Column("rarity_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["nft_part_id"], ["nft_parts.id"], ondelete="cascade"),
        sa.ForeignKeyConstraint(["rarity_id"], [rarities_id], ondelete="cascade"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("hex"),
    )
    op.create_index(op.f("ix_colors_id"), "colors", ["id"], unique=False)
    op.execute("ALTER SEQUENCE colors_id_seq restart with 40;")
    op.create_table(
        "divisions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("code", sa.BigInteger(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("country_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["country_id"], [countries_id], ondelete="cascade"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_divisions_code"), "divisions", ["code"], unique=True)
    op.create_index(op.f("ix_divisions_id"), "divisions", ["id"], unique=False)
    op.create_table(
        "names",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("value", sa.String(length=255), nullable=False),
        sa.Column("type_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["type_id"], ["name_types.id"], ondelete="cascade"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_names_id"), "names", ["id"], unique=False)
    op.create_table(
        "stats_stat_types",
        sa.Column("stat_id", sa.Integer(), nullable=False),
        sa.Column("type_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["stat_id"], [stats_id], ondelete="cascade"),
        sa.ForeignKeyConstraint(["type_id"], ["stat_types.id"], ondelete="cascade"),
        sa.PrimaryKeyConstraint("stat_id", "type_id"),
    )
    op.create_table(
        "clubs",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("code", sa.BigInteger(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("country_id", sa.Integer(), nullable=True),
        sa.Column("division_id", sa.Integer(), nullable=True),
        sa.Column("first_color_id", sa.Integer(), nullable=True),
        sa.Column("second_color_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["country_id"], [countries_id], ondelete="cascade"),
        sa.ForeignKeyConstraint(["division_id"], ["divisions.id"], ondelete="cascade"),
        sa.ForeignKeyConstraint(["first_color_id"], [colors_id], ondelete="cascade"),
        sa.ForeignKeyConstraint(["second_color_id"], [colors_id], ondelete="cascade"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_clubs_code"), "clubs", ["code"], unique=True)
    op.create_index(op.f("ix_clubs_id"), "clubs", ["id"], unique=False)
    op.create_table(
        "face_parts_colors",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("face_part_id", sa.Integer(), nullable=True),
        sa.Column("color_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["color_id"], [colors_id], ondelete="cascade"),
        sa.ForeignKeyConstraint(
            ["face_part_id"], ["face_parts.id"], ondelete="cascade"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_face_parts_colors_id"), "face_parts_colors", ["id"], unique=False
    )
    op.execute("ALTER SEQUENCE face_parts_colors_id_seq restart with 36;")
    op.create_table(
        "dependent_face_parts_colors",
        sa.Column("face_part_color_id", sa.Integer(), nullable=False),
        sa.Column("depend_face_part_color_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["depend_face_part_color_id"], ["face_parts_colors.id"], ondelete="cascade"
        ),
        sa.ForeignKeyConstraint(
            ["face_part_color_id"], ["face_parts_colors.id"], ondelete="cascade"
        ),
        sa.PrimaryKeyConstraint("face_part_color_id", "depend_face_part_color_id"),
    )
    op.create_table(
        "players",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("code", sa.BigInteger(), nullable=False),
        sa.Column("first_name_id", sa.Integer(), nullable=True),
        sa.Column("last_name_id", sa.Integer(), nullable=False),
        sa.Column("age", sa.Integer(), nullable=False),
        sa.Column("birth", sa.Date(), nullable=False),
        sa.Column("height", sa.SmallInteger(), nullable=False),
        sa.Column("weight", sa.SmallInteger(), nullable=False),
        sa.Column("cid", sa.String(length=255), nullable=True),
        sa.Column("filename", sa.String(length=255), nullable=True),
        sa.Column("club_id", sa.Integer(), nullable=True),
        sa.Column("rarity_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["club_id"], ["clubs.id"], ondelete="cascade"),
        sa.ForeignKeyConstraint(["first_name_id"], ["names.id"], ondelete="cascade"),
        sa.ForeignKeyConstraint(["last_name_id"], ["names.id"], ondelete="cascade"),
        sa.ForeignKeyConstraint(["rarity_id"], [rarities_id], ondelete="cascade"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_players_code"), "players", ["code"], unique=True)
    op.create_index(op.f("ix_players_id"), "players", ["id"], unique=False)
    op.create_table(
        "players_countries",
        sa.Column("player_id", sa.Integer(), nullable=False),
        sa.Column("country_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["country_id"], [countries_id], ondelete="cascade"),
        sa.ForeignKeyConstraint(["player_id"], [players_id], ondelete="cascade"),
        sa.PrimaryKeyConstraint("player_id", "country_id"),
    )
    op.create_table(
        "players_positions",
        sa.Column("player_id", sa.Integer(), nullable=False),
        sa.Column("position_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["player_id"], [players_id], ondelete="cascade"),
        sa.ForeignKeyConstraint(["position_id"], ["positions.id"], ondelete="cascade"),
        sa.PrimaryKeyConstraint("player_id", "position_id"),
    )
    op.create_table(
        "players_stats",
        sa.Column("player_id", sa.Integer(), nullable=False),
        sa.Column("stat_id", sa.Integer(), nullable=False),
        sa.Column("value", sa.SmallInteger(), nullable=False),
        sa.ForeignKeyConstraint(["player_id"], [players_id], ondelete="cascade"),
        sa.ForeignKeyConstraint(["stat_id"], [stats_id], ondelete="cascade"),
        sa.PrimaryKeyConstraint("player_id", "stat_id"),
    )
    # ### end Alembic commands ###


def downgrade():
    """Downgrade."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("stats_positions")
    op.drop_index(op.f("ix_rarities_id"), table_name="rarities")
    op.drop_index(op.f("ix_rarities_code"), table_name="rarities")
    op.drop_table("players_stats")
    op.drop_table("players_positions")
    op.drop_table("players_countries")
    op.drop_index(op.f("ix_players_id"), table_name="players")
    op.drop_index(op.f("ix_players_code"), table_name="players")
    op.drop_table("players")
    op.drop_index(op.f("ix_names_id"), table_name="names")
    op.drop_table("names")
    op.drop_table("dependent_face_parts_colors")
    op.drop_index(op.f("ix_face_parts_colors_id"), table_name="face_parts_colors")
    op.drop_table("face_parts_colors")
    op.drop_index(op.f("ix_clubs_id"), table_name="clubs")
    op.drop_index(op.f("ix_clubs_code"), table_name="clubs")
    op.drop_table("clubs")
    op.drop_table("stats_stat_types")
    op.drop_index(op.f("ix_positions_id"), table_name="positions")
    op.drop_index(op.f("ix_positions_code"), table_name="positions")
    op.drop_table("positions")
    op.drop_index(op.f("ix_position_types_id"), table_name="position_types")
    op.drop_index(op.f("ix_position_types_code"), table_name="position_types")
    op.drop_table("position_types")
    op.drop_index(op.f("ix_elements_parent_id"), table_name="elements")
    op.drop_index(op.f("ix_elements_id"), table_name="elements")
    op.drop_index(op.f("ix_elements_code"), table_name="elements")
    op.drop_table("elements")
    op.drop_index(op.f("ix_divisions_id"), table_name="divisions")
    op.drop_index(op.f("ix_divisions_code"), table_name="divisions")
    op.drop_table("divisions")
    op.drop_index(op.f("ix_colors_id"), table_name="colors")
    op.drop_table("colors")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")
    op.drop_index(op.f("ix_stats_id"), table_name="stats")
    op.drop_index(op.f("ix_stats_code"), table_name="stats")
    op.drop_table("stats")
    op.drop_index(op.f("ix_stat_types_id"), table_name="stat_types")
    op.drop_index(op.f("ix_stat_types_code"), table_name="stat_types")
    op.drop_table("stat_types")
    op.drop_index(op.f("ix_nft_parts_id"), table_name="nft_parts")
    op.drop_index(op.f("ix_nft_parts_code"), table_name="nft_parts")
    op.drop_table("nft_parts")
    op.drop_index(op.f("ix_name_types_id"), table_name="name_types")
    op.drop_index(op.f("ix_name_types_code"), table_name="name_types")
    op.drop_table("name_types")
    op.drop_index(op.f("ix_face_parts_id"), table_name="face_parts")
    op.drop_index(op.f("ix_face_parts_code"), table_name="face_parts")
    op.drop_table("face_parts")
    op.drop_index(op.f("ix_element_types_id"), table_name="element_types")
    op.drop_index(op.f("ix_element_types_code"), table_name="element_types")
    op.drop_table("element_types")
    op.drop_index(op.f("ix_countries_id"), table_name="countries")
    op.drop_index(op.f("ix_countries_code"), table_name="countries")
    op.drop_table("countries")
    op.drop_table("rarities")
    # ### end Alembic commands ###
