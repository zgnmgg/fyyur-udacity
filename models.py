from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

Shows = db.Table("Shows",
                 db.Column("id", db.Integer, primary_key=True),
                 db.Column("artist_id", db.Integer, db.ForeignKey("Artist.id")),
                 db.Column("venue_id", db.Integer, db.ForeignKey("Venue.id")),
                 db.Column("start_time", db.DateTime, default=datetime.utcnow()))

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

    genres = db.Column(db.String(120))
    website = db.Column(db.String)
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String)
    upcoming_shows_count = db.Column(db.Integer)
    upcoming_shows = db.relationship('UpcomingShow', backref='Venue')
    past_shows_count = db.Column(db.Integer)
    past_shows = db.relationship('PastShow', backref='Venue')

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    seeking_venues = db.Column(db.Boolean)
    seeking_description = db.Column(db.String)
    upcoming_shows_count = db.Column(db.Integer)
    upcoming_shows = db.relationship('UpcomingShow', backref='Artist')
    past_shows_count = db.Column(db.Integer)
    past_shows = db.relationship('PastShow', backref='Artist')

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class UpcomingShow(db.Model):
  __tablename__ = 'UpcomingShow'

  id = db.Column(db.Integer, primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
  start_time = db.Column(db.DateTime)

class PastShow(db.Model):
  __tablename__ = 'PastShow'

  id = db.Column(db.Integer, primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
  start_time = db.Column(db.DateTime)

class Area(db.Model):
  __tablename__ = 'Area'

  id = db.Column(db.Integer, primary_key=True)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  venues = db.relationship('Venue', backref='Area')
