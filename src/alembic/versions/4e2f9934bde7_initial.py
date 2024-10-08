"""initial

Revision ID: 4e2f9934bde7
Revises: 
Create Date: 2024-07-21 13:24:42.418519

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4e2f9934bde7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('test_your_partner',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('relationship_status', sa.String(), nullable=False),
    sa.Column('gender', sa.String(), nullable=False),
    sa.Column('therapy_experience', sa.String(), nullable=False),
    sa.Column('q1', sa.Integer(), nullable=False),
    sa.Column('q2', sa.Integer(), nullable=False),
    sa.Column('q3', sa.Integer(), nullable=False),
    sa.Column('q4', sa.Integer(), nullable=False),
    sa.Column('q5', sa.Integer(), nullable=False),
    sa.Column('q6', sa.Integer(), nullable=False),
    sa.Column('q7', sa.Integer(), nullable=False),
    sa.Column('q8', sa.Integer(), nullable=False),
    sa.Column('q9', sa.Integer(), nullable=False),
    sa.Column('q10', sa.Integer(), nullable=False),
    sa.Column('q11', sa.Integer(), nullable=False),
    sa.Column('q12', sa.Integer(), nullable=False),
    sa.Column('q13', sa.Integer(), nullable=False),
    sa.Column('q14', sa.Integer(), nullable=False),
    sa.Column('q15', sa.Integer(), nullable=False),
    sa.Column('q16', sa.Integer(), nullable=False),
    sa.Column('q17', sa.Integer(), nullable=False),
    sa.Column('q18', sa.Integer(), nullable=False),
    sa.Column('q19', sa.Integer(), nullable=False),
    sa.Column('q20', sa.Integer(), nullable=False),
    sa.Column('q21', sa.Integer(), nullable=False),
    sa.Column('q22', sa.Integer(), nullable=False),
    sa.Column('q23', sa.Integer(), nullable=False),
    sa.Column('q24', sa.Integer(), nullable=False),
    sa.Column('q25', sa.Integer(), nullable=False),
    sa.Column('q26', sa.Integer(), nullable=False),
    sa.Column('q27', sa.Integer(), nullable=False),
    sa.Column('q28', sa.Integer(), nullable=False),
    sa.Column('q29', sa.Integer(), nullable=False),
    sa.Column('q30', sa.Integer(), nullable=False),
    sa.Column('q31', sa.Integer(), nullable=False),
    sa.Column('q32', sa.Integer(), nullable=False),
    sa.Column('q33', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('test_yourself',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('relationship_status', sa.String(), nullable=False),
    sa.Column('gender', sa.String(), nullable=False),
    sa.Column('therapy_experience', sa.String(), nullable=False),
    sa.Column('q1', sa.Integer(), nullable=False),
    sa.Column('q2', sa.Integer(), nullable=False),
    sa.Column('q3', sa.Integer(), nullable=False),
    sa.Column('q4', sa.Integer(), nullable=False),
    sa.Column('q5', sa.Integer(), nullable=False),
    sa.Column('q6', sa.Integer(), nullable=False),
    sa.Column('q7', sa.Integer(), nullable=False),
    sa.Column('q8', sa.Integer(), nullable=False),
    sa.Column('q9', sa.Integer(), nullable=False),
    sa.Column('q10', sa.Integer(), nullable=False),
    sa.Column('q11', sa.Integer(), nullable=False),
    sa.Column('q12', sa.Integer(), nullable=False),
    sa.Column('q13', sa.Integer(), nullable=False),
    sa.Column('q14', sa.Integer(), nullable=False),
    sa.Column('q15', sa.Integer(), nullable=False),
    sa.Column('q16', sa.Integer(), nullable=False),
    sa.Column('q17', sa.Integer(), nullable=False),
    sa.Column('q18', sa.Integer(), nullable=False),
    sa.Column('q19', sa.Integer(), nullable=False),
    sa.Column('q20', sa.Integer(), nullable=False),
    sa.Column('q21', sa.Integer(), nullable=False),
    sa.Column('q22', sa.Integer(), nullable=False),
    sa.Column('q23', sa.Integer(), nullable=False),
    sa.Column('q24', sa.Integer(), nullable=False),
    sa.Column('q25', sa.Integer(), nullable=False),
    sa.Column('q26', sa.Integer(), nullable=False),
    sa.Column('q27', sa.Integer(), nullable=False),
    sa.Column('q28', sa.Integer(), nullable=False),
    sa.Column('q29', sa.Integer(), nullable=False),
    sa.Column('q30', sa.Integer(), nullable=False),
    sa.Column('q31', sa.Integer(), nullable=False),
    sa.Column('q32', sa.Integer(), nullable=False),
    sa.Column('q33', sa.Integer(), nullable=False),
    sa.Column('q34', sa.Integer(), nullable=False),
    sa.Column('q35', sa.Integer(), nullable=False),
    sa.Column('q36', sa.Integer(), nullable=False),
    sa.Column('q37', sa.Integer(), nullable=False),
    sa.Column('q38', sa.Integer(), nullable=False),
    sa.Column('q39', sa.Integer(), nullable=False),
    sa.Column('q40', sa.Integer(), nullable=False),
    sa.Column('q41', sa.Integer(), nullable=False),
    sa.Column('q42', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('test_yourself')
    op.drop_table('test_your_partner')
    # ### end Alembic commands ###
