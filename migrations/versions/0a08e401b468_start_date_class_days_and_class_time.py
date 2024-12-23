"""start date class days and class time

Revision ID: 0a08e401b468
Revises: 051c970355fb
Create Date: 2024-11-20 18:20:12.745394

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a08e401b468'
down_revision = '051c970355fb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('course', schema=None) as batch_op:
        batch_op.add_column(sa.Column('start_date', sa.Date(), nullable=True))
        batch_op.add_column(sa.Column('class_days', sa.String(length=200), nullable=True))
        batch_op.add_column(sa.Column('class_time', sa.String(length=50), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('course', schema=None) as batch_op:
        batch_op.drop_column('class_time')
        batch_op.drop_column('class_days')
        batch_op.drop_column('start_date')

    # ### end Alembic commands ###
