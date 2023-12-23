"""image column aded

Revision ID: 8716a1e6c5ad
Revises: 307caf767254
Create Date: 2023-12-21 10:51:29.097435

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8716a1e6c5ad'
down_revision: Union[str, None] = '307caf767254'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('image', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product', 'image')
    # ### end Alembic commands ###
