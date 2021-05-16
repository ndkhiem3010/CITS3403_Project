"""empty message

Revision ID: 2f2f7b6fc556
Revises: ad9b04bf4689
Create Date: 2021-05-15 05:43:06.097239

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f2f7b6fc556'
down_revision = 'ad9b04bf4689'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('attempted_quiz',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('quiz_name', sa.Integer(), nullable=True),
    sa.Column('quiz_score', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['quiz_name'], ['quiz.quizname'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.drop_table('completed_quiz')
    op.drop_index('ix_course_timestamp', table_name='course')
    op.drop_column('course', 'timestamp')
    op.add_column('enrolled_course', sa.Column('course_name', sa.Integer(), nullable=True))
    op.drop_constraint(None, 'enrolled_course', type_='foreignkey')
    op.create_foreign_key(None, 'enrolled_course', 'course', ['course_name'], ['coursename'])
    op.drop_column('enrolled_course', 'course_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('enrolled_course', sa.Column('course_id', sa.INTEGER(), nullable=True))
    op.drop_constraint(None, 'enrolled_course', type_='foreignkey')
    op.create_foreign_key(None, 'enrolled_course', 'course', ['course_id'], ['id'])
    op.drop_column('enrolled_course', 'course_name')
    op.add_column('course', sa.Column('timestamp', sa.DATETIME(), nullable=True))
    op.create_index('ix_course_timestamp', 'course', ['timestamp'], unique=False)
    op.create_table('completed_quiz',
    sa.Column('quiz_id', sa.INTEGER(), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['quiz_id'], ['quiz.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.drop_table('attempted_quiz')
    # ### end Alembic commands ###
