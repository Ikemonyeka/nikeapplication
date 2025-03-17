"""change embeddings format

Revision ID: 4f52225384bb
Revises: 4464f26fa677
Create Date: 2025-03-17 09:39:45.617903

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '4f52225384bb'
down_revision: Union[str, None] = '4464f26fa677'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('items', sa.Column('embedding', sa.Text(), nullable=True))
    op.drop_column('items', 'embeddings')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('items', sa.Column('embeddings', postgresql.ARRAY(sa.DOUBLE_PRECISION(precision=53)), autoincrement=False, nullable=True))
    op.drop_column('items', 'embedding')
    # ### end Alembic commands ###
