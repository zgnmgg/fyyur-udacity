#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, \
    redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from flask_migrate import Migrate
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)

    app.jinja_env.filters['datetime'] = format_datetime

@app.route('/')
def index():
    return render_template('pages/home.html')

#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():

    all_areas = Venue.query.with_entities(func.count(Venue.id), Venue.city,
            Venue.state).group_by(Venue.city, Venue.state).all()
    data = []

    for area in all_areas:

        area_venues = \
            Venue.query.filter_by(state=area.state).filter_by(city=area.city).all()

        venue_data = []
    for venue in area_venues:
        venue_data.append({
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": len(db.session.query(Show).filter(Show.venue_id==1).filter(Show.start_time>datetime.now()).all())
        })
    data.append({
        "city": area.city,
        "state": area.state,
        "venues": venue_data
    })

    return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term', '')
    search_result = db.session.query(Venue).filter(Venue.name.ilike(f'%{search_term}%')).all()
    data = []

    for result in search_result:
        data.append({
            "id": result.id,
            "name": result.name,
            "num_upcoming_shows": len(db.session.query(Show).filter(Show.venue_id == result.id).filter(Show.start_time > datetime.now()).all()),
        })

    response={
        "count": len(search_result),
        "data": data
    }

    return render_template('pages/search_venues.html', results=response,
                       search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query.get(venue_id)

    if not venue:
        return render_template('errors/404.html')

    upcoming_shows_query = db.session.query(Show).join(Artist).filter(Show.venue_id==venue_id).filter(Show.start_time>datetime.now()).all()
    upcoming_shows = []

    past_shows_query = db.session.query(Show).join(Artist).filter(Show.venue_id==venue_id).filter(Show.start_time<datetime.now()).all()
    past_shows = []

    for show in past_shows_query:
        past_shows.append({
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
        })

    for show in upcoming_shows_query:
        upcoming_shows.append({
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": show.start_time.strftime("%Y-%m-%d %H:%M:%S")
        })

    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }

    return render_template('pages/show_venue.html', venue=data)

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    error = False

    try:
        name = request.form['name']
        city = request.form['city']
        state = request.form['state']
        address = request.form['address']
        phone = request.form['phone']
        genres = request.form.getlist('genres')
        image_link = request.form['image_link']
        facebook_link = request.form['facebook_link']
        website = request.form['website']
        seeking_talent = True if 'seeking_talent' in request.form else False
        seeking_description = request.form['seeking_description']

        venue = Venue(name=name, city=city, state=state, address=address, phone=phone, genres=genres, facebook_link=facebook_link, image_link=image_link, website=website, seeking_talent=seeking_talent, seeking_description=seeking_description)
        db.session.add(venue)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        flash('An error occurred. Venue ' + request.form['name']+ ' could not be listed.')
    if not error:
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    name = Venue.query.get(venue_id).name
    try:
        deleted_venue = db.session.query(Venue).filter(Venue.id == venue_id)
        deleted_venue.delete()
        db.session.commit()
        flash("Venue: " + name + " was successfully deleted.")

    except:
        db.session.rollback()
        print(sys.exc_info())
        return jsonify(
            {
                "errorMessage": "Something went wrong. This venue was not successfully deleted. Please try again."
            }
        )

    finally:
        db.session.close()
        return redirect(url_for("index"))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    fields = ["id", "name"]
    artists_data = db.session.query(Artist).options(load_only(*fields)).all()

    return render_template("pages/artists.html", artists=artists_data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
    search_query = request.form.get("search_term", "")
    search_response = {"count": 0, "data": []}

    fields = ["id", "name"]
    artist_search_results = (
        db.session.query(Artist)
        .filter(Artist.name.ilike(f"%{search_query}%"))
        .options(load_only(*fields))
        .all()
    )

    num_upcoming_shows = 0

    search_response["count"] = len(artist_search_results)

    for result in artist_search_results:
        item = {
            "id": result.id,
            "name": result.name,
            "num_upcoming_shows": num_upcoming_shows,
        }
        search_response["data"].append(item)

    return render_template(
        "pages/search_artists.html",
        results=search_response,
        search_term=request.form.get("search_term", ""),
    )

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    data = {}

    try:
        requested_artist = Artist.query.get(artist_id)

        if requested_artist is None:
            return not_found_error(404)
            # Figure out a better way to do this

        genres = []
        for item in requested_artist.genres:
            genres.append(item.genre)

        shows = Show.query.filter_by(artist_id=artist_id)

        today = datetime.datetime.now()

        raw_past_shows = shows.filter(Show.start_time < today).all()
        past_shows = []
        for show in raw_past_shows:
            venue = Venue.query.get(show.venue_id)
            show_data = {
                "venue_id": venue.id,
                "venue_name": venue.name,
                "venue_image_link": venue.image_link,
                "start_time": str(show.start_time),
            }
            past_shows.append(show_data)

        raw_upcoming_shows = shows.filter(Show.start_time >= today).all()
        upcoming_shows = []
        for show in raw_upcoming_shows:
            venue = Venue.query.get(show.venue_id)
            show_data = {
                "venue_id": venue.id,
                "venue_name": venue.name,
                "venue_image_link": venue.image_link,
                "start_time": str(show.start_time),
            }
            upcoming_shows.append(show_data)

        data = {
            "id": requested_artist.id,
            "name": requested_artist.name,
            "genres": genres,
            "city": requested_artist.city,
            "state": requested_artist.state,
            "phone": requested_artist.phone,
            "seeking_venue": False,
            "facebook_link": requested_artist.facebook_link,
            "image_link": requested_artist.image_link,
            "past_shows": past_shows,
            "upcoming_shows": upcoming_shows,
            "past_shows_count": len(past_shows),
            "upcoming_shows_count": len(upcoming_shows),
        }

    except:
        print(sys.exc_info())
        flash("Something went wrong. Please try again.")

    finally:
        db.session.close()

    return render_template("pages/show_artist.html", artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()

    data = {}

    try:
        requested_artist = Artist.query.get(artist_id)
        print(requested_artist)
        if requested_artist is None:
            return not_found_error(404)

        genres = []
        if len(requested_artist.genres) > 0:
            for item in requested_artist.genres:
                genres.append(item.genre)

            data = {
                "id": requested_artist.id,
                "name": requested_artist.name,
                "city": requested_artist.city,
                "state": requested_artist.state,
                "phone": requested_artist.phone,
                "genres": genres,
                "facebook_link": requested_artist.facebook_link,
                "seeking_venue": requested_artist.seeking_venue,
                "seeking_description": requested_artist.seeking_description,
                "image_link": requested_artist.image_link,
            }

    except:
        print(sys.exc_info())
        flash("Something went wrong. Please try again.")
        return redirect(url_for("index"))

    finally:
        db.session.close()

    return render_template("forms/edit_artist.html", form=form, artist=data)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    artist = Artist.query.get(artist_id)

    try:
        artist.name = request.form['name']
        artist.city = request.form['city']
        artist.state = request.form['state']
        artist.phone = request.form['phone']
        db.session.commit()
    except SQLAlchemyError as e:
        print(e.__traceback__)
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.get(venue_id)
    return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    venue = Venue.query.get(venue_id)

    try:
        venue.name = request.form['name']
        venue.city = request.form['city']
        venue.state = request.form['state']
        venue.address = request.form['address']
        venue.phone = request.form['phone']
        db.session.commit()
    except SQLAlchemyError as e:
        print(e.__traceback__)
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    error = False
    try:
        name = request.form['name']
        city = request.form['city']
        state = request.form['state']
        phone = request.form['phone']
        genres = request.form.getlist('genres'),
        facebook_link = request.form['facebook_link']
        image_link = request.form['image_link']
        website = request.form['website']
        seeking_venue = True if 'seeking_venue' in request.form else False
        seeking_description = request.form['seeking_description']

        artist = Artist(name=name, city=city, state=state, phone=phone, genres=genres, facebook_link=facebook_link, image_link=image_link, website=website, seeking_venue=seeking_venue, seeking_description=seeking_description)
        db.session.add(artist)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        flash('An error occurred. Artist ' + request.form['name']+ ' could not be listed.')
    if not error:
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    return render_template('pages/home.html')

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    data = db.session.query(UpcomingShow, Venue, Artist).select_from(UpcomingShow).join(Venue).join(Artist).all()

    return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    error = False
    try:
        artist_id = request.form['artist_id']
        venue_id = request.form['venue_id']
        start_time = request.form['start_time']

        show = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
        db.session.add(show)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        flash('An error occurred. Show could not be listed.')
    if not error:
        flash('Show was successfully listed')
    return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
