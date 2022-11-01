# -*- coding: utf-8 -*-
"""Add fixtures.

Revision ID: 550ceb95fe1d
Revises: b8cfac02486d
Create Date: 2022-04-02 20:10:34.857499

"""
from app.generation_nft_db.scripts.fixtures import Fixtures

# revision identifiers, used by Alembic.
revision = "550ceb95fe1d"
down_revision = "4d3619cdbf13"
branch_labels = None
depends_on = None


def upgrade():
    """Upgrade."""
    fixtures = Fixtures()
    fixtures.set_fixtures()


def downgrade():
    """Downgrade."""
    fixtures = Fixtures(reset=True)
    fixtures.set_fixtures()
