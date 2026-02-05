"""add status to courses

Revision ID: 68e4806f2b9e
Revises: 8beaa97b378d
Create Date: 2026-02-05 14:20:10.236084
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '68e4806f2b9e'
down_revision: Union[str, Sequence[str], None] = '8beaa97b378d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1️⃣ Add column with safe default
    op.add_column(
        'courses',
        sa.Column(
            'status',
            sa.String(length=20),
            nullable=False,
            server_default='draft'
        )
    )

    # 2️⃣ (Optional but clean) remove default for future inserts
    op.alter_column(
        'courses',
        'status',
        server_default=None
    )


def downgrade() -> None:
    op.drop_column('courses', 'status')
