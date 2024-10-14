"""initial

Revision ID: 7fbca9aa75af
Revises:
Create Date: 2024-07-26 19:55:53.485773

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7fbca9aa75af"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "test_your_partner",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.Column("age", sa.Integer(), nullable=False),
        sa.Column("relationship_status", sa.String(), nullable=False),
        sa.Column("gender", sa.String(), nullable=False),
        sa.Column("therapy_experience", sa.String(), nullable=False),
        sa.Column("anxious_q1", sa.Integer(), nullable=False),
        sa.Column("anxious_q2", sa.Integer(), nullable=False),
        sa.Column("anxious_q3", sa.Integer(), nullable=False),
        sa.Column("anxious_q4", sa.Integer(), nullable=False),
        sa.Column("anxious_q5", sa.Integer(), nullable=False),
        sa.Column("anxious_q6", sa.Integer(), nullable=False),
        sa.Column("anxious_q7", sa.Integer(), nullable=False),
        sa.Column("anxious_q8", sa.Integer(), nullable=False),
        sa.Column("anxious_q9", sa.Integer(), nullable=False),
        sa.Column("anxious_q10", sa.Integer(), nullable=False),
        sa.Column("anxious_q11", sa.Integer(), nullable=False),
        sa.Column("secure_q12", sa.Integer(), nullable=False),
        sa.Column("secure_q13", sa.Integer(), nullable=False),
        sa.Column("secure_q14", sa.Integer(), nullable=False),
        sa.Column("secure_q15", sa.Integer(), nullable=False),
        sa.Column("secure_q16", sa.Integer(), nullable=False),
        sa.Column("secure_q17", sa.Integer(), nullable=False),
        sa.Column("secure_q18", sa.Integer(), nullable=False),
        sa.Column("secure_q19", sa.Integer(), nullable=False),
        sa.Column("secure_q20", sa.Integer(), nullable=False),
        sa.Column("secure_q21", sa.Integer(), nullable=False),
        sa.Column("secure_q22", sa.Integer(), nullable=False),
        sa.Column("avoidant_q23", sa.Integer(), nullable=False),
        sa.Column("avoidant_q24", sa.Integer(), nullable=False),
        sa.Column("avoidant_q25", sa.Integer(), nullable=False),
        sa.Column("avoidant_q26", sa.Integer(), nullable=False),
        sa.Column("avoidant_q27", sa.Integer(), nullable=False),
        sa.Column("avoidant_q28", sa.Integer(), nullable=False),
        sa.Column("avoidant_q29", sa.Integer(), nullable=False),
        sa.Column("avoidant_q30", sa.Integer(), nullable=False),
        sa.Column("avoidant_q31", sa.Integer(), nullable=False),
        sa.Column("avoidant_q32", sa.Integer(), nullable=False),
        sa.Column("avoidant_q33", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "test_yourself",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.Column("age", sa.Integer(), nullable=False),
        sa.Column("relationship_status", sa.String(), nullable=False),
        sa.Column("gender", sa.String(), nullable=False),
        sa.Column("therapy_experience", sa.String(), nullable=False),
        sa.Column("anxious_q1", sa.Integer(), nullable=False),
        sa.Column("anxious_q2", sa.Integer(), nullable=False),
        sa.Column("anxious_q3", sa.Integer(), nullable=False),
        sa.Column("anxious_q4", sa.Integer(), nullable=False),
        sa.Column("anxious_q5", sa.Integer(), nullable=False),
        sa.Column("anxious_q6", sa.Integer(), nullable=False),
        sa.Column("anxious_q7", sa.Integer(), nullable=False),
        sa.Column("anxious_q8", sa.Integer(), nullable=False),
        sa.Column("anxious_q9", sa.Integer(), nullable=False),
        sa.Column("anxious_q10", sa.Integer(), nullable=False),
        sa.Column("anxious_q11", sa.Integer(), nullable=False),
        sa.Column("anxious_q12", sa.Integer(), nullable=False),
        sa.Column("anxious_q13", sa.Integer(), nullable=False),
        sa.Column("anxious_q14", sa.Integer(), nullable=False),
        sa.Column("secure_q15", sa.Integer(), nullable=False),
        sa.Column("secure_q16", sa.Integer(), nullable=False),
        sa.Column("secure_q17", sa.Integer(), nullable=False),
        sa.Column("secure_q18", sa.Integer(), nullable=False),
        sa.Column("secure_q19", sa.Integer(), nullable=False),
        sa.Column("secure_q20", sa.Integer(), nullable=False),
        sa.Column("secure_q21", sa.Integer(), nullable=False),
        sa.Column("secure_q22", sa.Integer(), nullable=False),
        sa.Column("secure_q23", sa.Integer(), nullable=False),
        sa.Column("secure_q24", sa.Integer(), nullable=False),
        sa.Column("secure_q25", sa.Integer(), nullable=False),
        sa.Column("secure_q26", sa.Integer(), nullable=False),
        sa.Column("secure_q27", sa.Integer(), nullable=False),
        sa.Column("secure_q28", sa.Integer(), nullable=False),
        sa.Column("avoidant_q29", sa.Integer(), nullable=False),
        sa.Column("avoidant_q30", sa.Integer(), nullable=False),
        sa.Column("avoidant_q31", sa.Integer(), nullable=False),
        sa.Column("avoidant_q32", sa.Integer(), nullable=False),
        sa.Column("avoidant_q33", sa.Integer(), nullable=False),
        sa.Column("avoidant_q34", sa.Integer(), nullable=False),
        sa.Column("avoidant_q35", sa.Integer(), nullable=False),
        sa.Column("avoidant_q36", sa.Integer(), nullable=False),
        sa.Column("avoidant_q37", sa.Integer(), nullable=False),
        sa.Column("avoidant_q38", sa.Integer(), nullable=False),
        sa.Column("avoidant_q39", sa.Integer(), nullable=False),
        sa.Column("avoidant_q40", sa.Integer(), nullable=False),
        sa.Column("avoidant_q41", sa.Integer(), nullable=False),
        sa.Column("avoidant_q42", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("test_yourself")
    op.drop_table("test_your_partner")
    # ### end Alembic commands ###
