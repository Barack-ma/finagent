"""add loans table

Revision ID: 38d1b69e605b
Revises: 5d7d883a8834
Create Date: 2026-09-06 00:05:06.016746

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '38d1b69e605b'
down_revision: Union[str, Sequence[str], None] = '5d7d883a8834'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
