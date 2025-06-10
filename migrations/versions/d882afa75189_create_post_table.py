"""Create Post table

Revision ID: d882afa75189
Revises: 8f54d3318dfb
Create Date: 2025-06-09 23:30:50.430005

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'd882afa75189'
down_revision: Union[str, None] = '8f54d3318dfb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Only alter the posts table to update the default value for id if necessary.
    # No dropping of users or posts tables.
    pass


def downgrade() -> None:
    """Downgrade schema."""
    # No dropping or recreating users or posts tables.
    pass
