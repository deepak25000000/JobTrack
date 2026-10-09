
"""Create the initial user and job tables.

Revision ID: c4d9e2a7b610
Revises:
"""

from alembic import op
import sqlalchemy as sa


# Revision identifiers used by Alembic.
revision = "c4d9e2a7b610"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create users first because jobs will reference users.
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("username", sa.String(100), nullable=False),
        sa.Column("email", sa.String(150), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.UniqueConstraint("username", name="uq_user_username"),
        sa.UniqueConstraint("email", name="uq_user_email"),
    )

    # The user_id column is added by the next migration.
    op.create_table(
        "job",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("role", sa.String(100), nullable=False),
        sa.Column("location", sa.String(100), nullable=False),
        sa.Column("company", sa.String(100), nullable=False),
        sa.Column("status", sa.String(50), nullable=False),
    )


def downgrade():
    op.drop_table("job")
    op.drop_table("user")
