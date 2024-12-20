"""updated models

Revision ID: d2ffd3a4aa35
Revises: 88aac2ea4e98
Create Date: 2024-12-20 00:34:01.446854

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd2ffd3a4aa35'
down_revision: Union[str, None] = '88aac2ea4e98'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
