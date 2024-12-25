"""added new models for roles and permissions

Revision ID: c7b8da708214
Revises: d2ffd3a4aa35
Create Date: 2024-12-24 02:03:53.801262

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c7b8da708214'
down_revision: Union[str, None] = 'd2ffd3a4aa35'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
