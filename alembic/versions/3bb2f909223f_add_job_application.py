"""add job application

Revision ID: 3bb2f909223f
Revises: 23c5b7347c27
Create Date: 2023-09-22 17:24:32.868190

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3bb2f909223f'
down_revision = '23c5b7347c27'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('job_application',
                    sa.Column('application_id', sa.UUID(), nullable=False),
                    sa.Column('jobseeker_id', sa.UUID(), nullable=False),
                    sa.Column('job_id', sa.UUID(), nullable=False),
                    sa.Column('date_created', sa.DateTime(timezone=True),
                              nullable=False),
                    sa.Column('date_updated', sa.DateTime(timezone=True),
                              nullable=False),
                    sa.Column('created_by', sa.String(length=100),
                              server_default='Unknown', nullable=False),
                    sa.Column('updated_by', sa.String(length=100),
                              server_default='Unknown', nullable=False),
                    sa.Column('active', sa.Boolean(), nullable=False),
                    sa.Column('meta', postgresql.JSON(astext_type=sa.Text()),
                              server_default='{}', nullable=True),
                    sa.ForeignKeyConstraint(['job_id'], ['job.job_id'], ),
                    sa.PrimaryKeyConstraint('application_id')
                    )
    op.add_column('job', sa.Column('date', sa.Date(), nullable=False))
    op.add_column('job', sa.Column('filled', sa.Boolean(), nullable=False))
    op.add_column('job', sa.Column('job_code', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('job', 'job_code')
    op.drop_column('job', 'filled')
    op.drop_column('job', 'date')
    op.drop_table('job_application')
    # ### end Alembic commands ###
