"""Add Passages ORM, drop legacy passages, cascading deletes for file-passages and user-jobs

Revision ID: c5d964280dff
Revises: a91994b9752f
Create Date: 2024-12-10 15:05:32.335519

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c5d964280dff'
down_revision: Union[str, None] = 'a91994b9752f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('passages', sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.add_column('passages', sa.Column('is_deleted', sa.Boolean(), server_default=sa.text('FALSE'), nullable=False))
    op.add_column('passages', sa.Column('_created_by_id', sa.String(), nullable=True))
    op.add_column('passages', sa.Column('_last_updated_by_id', sa.String(), nullable=True))

    # Data migration step:
    op.add_column("passages", sa.Column("organization_id", sa.String(), nullable=True))
    # Populate `organization_id` based on `user_id`
    # Use a raw SQL query to update the organization_id
    op.execute(
        """
        UPDATE passages
        SET organization_id = users.organization_id
        FROM users
        WHERE passages.user_id = users.id
    """
    )

    # Set `organization_id` as non-nullable after population
    op.alter_column("passages", "organization_id", nullable=False)

    op.alter_column('passages', 'text',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('passages', 'embedding_config',
               existing_type=postgresql.JSON(astext_type=sa.Text()),
               nullable=False)
    op.alter_column('passages', 'metadata_',
               existing_type=postgresql.JSON(astext_type=sa.Text()),
               nullable=False)
    op.alter_column('passages', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=False)
    op.drop_index('passage_idx_user', table_name='passages')
    op.create_foreign_key(None, 'passages', 'organizations', ['organization_id'], ['id'])
    op.create_foreign_key(None, 'passages', 'agents', ['agent_id'], ['id'])
    op.create_foreign_key(None, 'passages', 'files', ['file_id'], ['id'], ondelete='CASCADE')
    op.drop_column('passages', 'user_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('passages', sa.Column('user_id', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'passages', type_='foreignkey')
    op.drop_constraint(None, 'passages', type_='foreignkey')
    op.drop_constraint(None, 'passages', type_='foreignkey')
    op.create_index('passage_idx_user', 'passages', ['user_id', 'agent_id', 'file_id'], unique=False)
    op.alter_column('passages', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=True)
    op.alter_column('passages', 'metadata_',
               existing_type=postgresql.JSON(astext_type=sa.Text()),
               nullable=True)
    op.alter_column('passages', 'embedding_config',
               existing_type=postgresql.JSON(astext_type=sa.Text()),
               nullable=True)
    op.alter_column('passages', 'text',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_column('passages', 'organization_id')
    op.drop_column('passages', '_last_updated_by_id')
    op.drop_column('passages', '_created_by_id')
    op.drop_column('passages', 'is_deleted')
    op.drop_column('passages', 'updated_at')
    # ### end Alembic commands ###