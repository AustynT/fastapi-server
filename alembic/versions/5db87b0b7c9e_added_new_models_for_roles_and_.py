"""added new models for roles and permissions

Revision ID: 5db87b0b7c9e
Revises: c7b8da708214
Create Date: 2024-12-24 02:05:48.320417

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5db87b0b7c9e'
down_revision: Union[str, None] = 'c7b8da708214'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
