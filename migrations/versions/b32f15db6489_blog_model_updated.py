"""blog model updated

Revision ID: b32f15db6489
Revises: 6ad9c867c5ee
Create Date: 2024-01-03 23:37:54.776212

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b32f15db6489'
down_revision: Union[str, None] = '6ad9c867c5ee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('blog', sa.Column('title', sa.String(length=150), nullable=False))
    op.alter_column('blog', 'description',
               existing_type=sa.VARCHAR(),
               type_=sa.Text(),
               existing_nullable=True)
    op.drop_column('blog', 'subject')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('blog', sa.Column('subject', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.alter_column('blog', 'description',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(),
               existing_nullable=True)
    op.drop_column('blog', 'title')
    # ### end Alembic commands ###
