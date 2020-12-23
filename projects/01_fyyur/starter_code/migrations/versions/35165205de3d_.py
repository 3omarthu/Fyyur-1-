"""empty message

Revision ID: 35165205de3d
Revises: d5e7ce2702b9
Create Date: 2020-12-22 23:03:13.624026

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35165205de3d'
down_revision = 'd5e7ce2702b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Artist_genres')
    op.drop_table('Venue_genres')
    op.add_column('Artist', sa.Column('genres', sa.String(length=120), nullable=True))
    op.add_column('Artist', sa.Column('seeking_description', sa.String(length=120), nullable=True))
    op.add_column('Artist', sa.Column('seeking_venue', sa.Boolean(), nullable=True))
    op.add_column('Venue', sa.Column('genres', sa.String(length=120), nullable=True))
    op.add_column('Venue', sa.Column('seeking_description', sa.String(length=120), nullable=True))
    op.add_column('Venue', sa.Column('seeking_talent', sa.Boolean(), nullable=True))
    op.add_column('Venue', sa.Column('website', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'website')
    op.drop_column('Venue', 'seeking_talent')
    op.drop_column('Venue', 'seeking_description')
    op.drop_column('Venue', 'genres')
    op.drop_column('Artist', 'seeking_venue')
    op.drop_column('Artist', 'seeking_description')
    op.drop_column('Artist', 'genres')
    op.create_table('Venue_genres',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Venue_genres_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('Venue_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('genre', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['Venue_id'], ['Venue.id'], name='Venue_genres_Venue_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='Venue_genres_pkey')
    )
    op.create_table('Artist_genres',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Artist_genres_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('Artist_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('genre', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['Artist_id'], ['Artist.id'], name='Artist_genres_Artist_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='Artist_genres_pkey')
    )
    # ### end Alembic commands ###
