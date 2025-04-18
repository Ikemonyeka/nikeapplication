"""Add embeddings column to items

Revision ID: 4464f26fa677
Revises: 3eea4fe808ad
Create Date: 2025-03-17 09:02:41.013177

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4464f26fa677'
down_revision: Union[str, None] = '3eea4fe808ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('items', sa.Column('embeddings', sa.ARRAY(sa.Double()), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('items', 'embeddings')
    # ### end Alembic commands ###
