"""empty message

Revision ID: 8e16b616cc31
Revises: 35165205de3d
Create Date: 2020-12-23 20:45:55.361574

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e16b616cc31'
down_revision = '35165205de3d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Show', sa.Column('artist_id', sa.Integer(), nullable=True))
    op.add_column('Show', sa.Column('venue_id', sa.Integer(), nullable=True))
    op.drop_constraint('Show_Artist_id_fkey', 'Show', type_='foreignkey')
    op.drop_constraint('Show_Venue_id_fkey', 'Show', type_='foreignkey')
    op.create_foreign_key(None, 'Show', 'Venue', ['venue_id'], ['id'])
    op.create_foreign_key(None, 'Show', 'Artist', ['artist_id'], ['id'])
    op.drop_column('Show', 'Artist_id')
    op.drop_column('Show', 'Venue_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Show', sa.Column('Venue_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('Show', sa.Column('Artist_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'Show', type_='foreignkey')
    op.drop_constraint(None, 'Show', type_='foreignkey')
    op.create_foreign_key('Show_Venue_id_fkey', 'Show', 'Venue', ['Venue_id'], ['id'])
    op.create_foreign_key('Show_Artist_id_fkey', 'Show', 'Artist', ['Artist_id'], ['id'])
    op.drop_column('Show', 'venue_id')
    op.drop_column('Show', 'artist_id')
    # ### end Alembic commands ###