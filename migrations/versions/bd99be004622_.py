"""empty message

Revision ID: bd99be004622
Revises: 38ebaddb5d86
Create Date: 2021-05-16 06:05:41.681775

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd99be004622'
down_revision = '38ebaddb5d86'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('course', schema=None) as batch_op:
        batch_op.add_column(sa.Column('courseurl', sa.String(length=128), nullable=True))
        batch_op.create_index(batch_op.f('ix_course_courseurl'), ['courseurl'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('course', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_course_courseurl'))
        batch_op.drop_column('courseurl')

    # ### end Alembic commands ###
