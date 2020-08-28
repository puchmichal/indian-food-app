"""adding url and want to go to restaurant

Revision ID: 7378a2ba5b88
Revises: dc3d31b16660
Create Date: 2020-08-28 12:25:29.888949

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7378a2ba5b88'
down_revision = 'dc3d31b16660'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('restaurant', sa.Column('url', sa.String(length=255), nullable=True))
    op.add_column('restaurant', sa.Column('want_to_go', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('restaurant', 'want_to_go')
    op.drop_column('restaurant', 'url')
    # ### end Alembic commands ###
