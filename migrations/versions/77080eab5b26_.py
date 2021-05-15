"""empty message

Revision ID: 77080eab5b26
Revises: 37ff4d3e1a2c
Create Date: 2021-05-15 13:31:51.759795

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77080eab5b26'
down_revision = '37ff4d3e1a2c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('quiz', schema=None) as batch_op:
        batch_op.drop_index('ix_quiz_quizname')
        batch_op.drop_index('ix_quiz_timestamp')

    op.drop_table('quiz')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('quiz',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('quiz_maxscore', sa.INTEGER(), nullable=True),
    sa.Column('quizname', sa.VARCHAR(length=128), nullable=True),
    sa.Column('timestamp', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('quiz', schema=None) as batch_op:
        batch_op.create_index('ix_quiz_timestamp', ['timestamp'], unique=False)
        batch_op.create_index('ix_quiz_quizname', ['quizname'], unique=1)

    # ### end Alembic commands ###
