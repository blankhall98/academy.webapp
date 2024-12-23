"""add promo_image and syllabus to Course

Revision ID: 051c970355fb
Revises: 92d9f32b66e8
Create Date: 2024-11-20 17:35:56.748222

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '051c970355fb'
down_revision = '92d9f32b66e8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('course', schema=None) as batch_op:
        batch_op.add_column(sa.Column('promo_image', sa.String(length=200), nullable=True))
        batch_op.add_column(sa.Column('syllabus', sa.String(length=200), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('course', schema=None) as batch_op:
        batch_op.drop_column('syllabus')
        batch_op.drop_column('promo_image')

    # ### end Alembic commands ###
