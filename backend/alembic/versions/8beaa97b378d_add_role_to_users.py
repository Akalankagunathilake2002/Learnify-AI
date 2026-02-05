"""add role to users

Revision ID: 8beaa97b378d
Revises: 2cfe3063f893
Create Date: 2026-02-05 10:24:14.193772
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8beaa97b378d"
down_revision: Union[str, Sequence[str], None] = "2cfe3063f893"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Upgrade schema.
    1) Add role column with default='student' so existing rows are safe
    2) Remove default afterwards (optional but clean)
    """
    # Add column with default so old users get "student"
    op.add_column(
        "users",
        sa.Column(
            "role",
            sa.String(length=20),
            nullable=False,
            server_default="student",
        ),
    )

    # Remove default after migration (optional but recommended)
    op.alter_column("users", "role", server_default=None)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "role")
