"""remove step from unique contraint

Revision ID: 3140747f399a
Revises: 84079287ee2f
Create Date: 2016-08-17 16:57:47.803013

"""

# revision identifiers, used by Alembic.
revision = '3140747f399a'
down_revision = '84079287ee2f'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(u'_uc_case_start_status_step', 'analysis', type_='unique')
    op.create_unique_constraint('_uc_case_start_status_step', 'analysis', ['case_id', 'started_at', 'status'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('_uc_case_start_status_step', 'analysis', type_='unique')
    op.create_unique_constraint(u'_uc_case_start_status_step', 'analysis', ['case_id', 'started_at', 'status', 'failed_step'])
    ### end Alembic commands ###
