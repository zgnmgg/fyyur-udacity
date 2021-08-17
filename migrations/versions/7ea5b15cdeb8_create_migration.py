#!/usr/bin/python
# -*- coding: utf-8 -*-
"""create migration

Revision ID: 7ea5b15cdeb8
Revises: 0aadf7496cba
Create Date: 2021-08-17 12:51:29.079034

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.

revision = '7ea5b15cdeb8'
down_revision = '0aadf7496cba'
branch_labels = None
depends_on = None



def upgrade():
    op.create_table(
        'artists',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('city', sa.String(length=120), nullable=True),
        sa.Column('state', sa.String(length=120), nullable=True),
        sa.Column('phone', sa.String(length=120), nullable=True),
        sa.Column('genres', sa.String(length=120), nullable=True),
        sa.Column('website', sa.String(length=120), nullable=True),
        sa.Column('image_link', sa.String(length=500), nullable=True),
        sa.Column('facebook_link', sa.String(length=120),
                  nullable=True),
        sa.Column('seeking_venue', sa.Boolean(), nullable=False),
        sa.Column('seeking_description', sa.String(length=120),
                  nullable=True),
        sa.PrimaryKeyConstraint('id'),
        )
    op.create_table(
        'venues',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('city', sa.String(length=120), nullable=True),
        sa.Column('state', sa.String(length=120), nullable=True),
        sa.Column('address', sa.String(length=120), nullable=True),
        sa.Column('phone', sa.String(length=120), nullable=True),
        sa.Column('genres', sa.String(length=120), nullable=True),
        sa.Column('image_link', sa.String(length=500), nullable=True),
        sa.Column('facebook_link', sa.String(length=120),
                  nullable=True),
        sa.Column('website', sa.String(length=120), nullable=True),
        sa.Column('seeking_talent', sa.Boolean(), nullable=False),
        sa.Column('seeking_description', sa.String(length=120),
                  nullable=True),
        sa.PrimaryKeyConstraint('id'),
        )
    op.create_table(
        'shows',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('artist_id', sa.Integer(), nullable=False),
        sa.Column('venue_id', sa.Integer(), nullable=False),
        sa.Column('start_time', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['artist_id'], ['artists.id']),
        sa.ForeignKeyConstraint(['venue_id'], ['venues.id']),
        sa.PrimaryKeyConstraint('id'),
        )

    op.create_table(
        'PastShow',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('venue_id', sa.Integer(), nullable=False),
        sa.Column('artist_id', sa.Integer(), nullable=False),
        sa.Column('start_time', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['artist_id'], ['Artist.id']),
        sa.ForeignKeyConstraint(['venue_id'], ['Venue.id']),
        sa.PrimaryKeyConstraint('id'),
        )
    op.create_table(
        'UpcomingShow',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('venue_id', sa.Integer(), nullable=False),
        sa.Column('artist_id', sa.Integer(), nullable=False),
        sa.Column('start_time', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['artist_id'], ['Artist.id']),
        sa.ForeignKeyConstraint(['venue_id'], ['Venue.id']),
        sa.PrimaryKeyConstraint('id'),
        )
    op.drop_table('Show')
    op.create_table('Area', sa.Column('id', sa.Integer(),
                    nullable=False), sa.Column('city',
                    sa.String(length=120), nullable=True),
                    sa.Column('state', sa.String(length=120),
                    nullable=True), sa.PrimaryKeyConstraint('id'))
    op.add_column('Venue', sa.Column('area_id', sa.Integer(),
                  nullable=False))
    op.create_foreign_key(None, 'Venue', 'Area', ['area_id'], ['id'])


def downgrade():

    op.drop_table('shows')
    op.drop_table('venues')
    op.drop_table('artists')
    op.drop_constraint(None, 'Venue', type_='foreignkey')
    op.drop_column('Venue', 'area_id')
    op.drop_table('Area')
    op.create_table(
        'Show',
        sa.Column('id', sa.INTEGER(),
                  server_default=sa.text('nextval(\'"Show_id_seq"\'::regclass)'
                  ), autoincrement=True, nullable=False),
        sa.Column('name', sa.VARCHAR(), autoincrement=False,
                  nullable=True),
        sa.Column('venue_id', sa.INTEGER(), autoincrement=False,
                  nullable=False),
        sa.Column('artist_id', sa.INTEGER(), autoincrement=False,
                  nullable=False),
        sa.Column('start_time', postgresql.TIMESTAMP(),
                  autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(['artist_id'], ['Artist.id'],
                                name='Show_artist_id_fkey'),
        sa.ForeignKeyConstraint(['venue_id'], ['Venue.id'],
                                name='Show_venue_id_fkey'),
        sa.PrimaryKeyConstraint('id', name='Show_pkey'),
        )
    op.drop_table('UpcomingShow')
    op.drop_table('PastShow')

