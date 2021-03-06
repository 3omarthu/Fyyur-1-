#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from datetime import datetime
from models import app, db, Venue, Artist, Show
import sys
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#


moment = Moment(app)
app.config.from_object('config')
db.init_app(app)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

#models.py

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  venues = Venue.query.all()
  data =[]
  locations = set()
  
  
  for venue in venues:
        locations.add((venue.city, venue.state))

  for location in locations:
        data.append({
          "city": location[0],
          "state": location[1],
          "venues": []
        })
  for venue in venues:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%S:%M')
        coming_shows = 0
        shows = Show.query.filter_by(venue_id=venue.id).all()
        # for show in shows:
        #   if show.start_time > current_time:
        #     coming_shows += 1
        for venue_location in data:
          if venue.state == venue_location['state'] and venue.city == venue_location['city']:
            venue_location['venues'].append({
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": coming_shows
            })
  
  return render_template('pages/venues.html', areas=data);
  
@app.route('/venues/search', methods=['POST'])
def search_venues():

  terms = request.form.get('search_term', '')
  venues = Venue.query.filter(Venue.name.ilike(f'%{terms}%'))

  response={
    "count": venues.count(),
    "data": venues
  }
  
  return render_template('pages/search_venues.html', results=response, search_term=terms)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  venue = Venue.query.get(venue_id)
  past_shows = []
  upcoming_shows = []
  current_time = datetime.now().strftime('%Y-%m-%d %H:%S:%M')
  upcoming_shows_details = db.session.query(Show).join(Artist).filter(Show.venue_id==venue_id).all()
  past_show_details=db.session.query(Show).join(Artist).filter(Show.venue_id==venue_id).all()
  data_shows=[]

  for show in shows:
      data = {
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": format_datetime(str(show.start_time))
            }
        
  for show in upcoming_shows_details:
      data_shows.append({
      #here you data as start_time
      'start_time': show.start_time.strftime('%Y-%m-%d %H:%M:%S'),
      })
      if data_shows.start_time > current_time:
          upcoming_shows.append(data)

  for show in past_show_details:
      data_shows.append({
      #here you data as start_time
      'start_time': show.start_time.strftime('%Y-%m-%d %H:%M:%S'),
      })
      if data_shows.start_time > current_time:
          past_shows.append(data)

  data={
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
    "seeking_description":venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows)
  }

  return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
      form = VenueForm(request.form)
      try:
        newVenue = Venue(
        name=form.name.data, 
        city= form.city.data, 
        address=form.address.data ,
        genres =form.genres.getlist ,
        phone=form.phone.data ,  
        facebook_link=form.facebook_link.data,
        image_link =form.image_link.data ,
        seeking_talent =form.seeking_talent.data ,
        seeking_description =form.seeking_description.data
        )
        db.session.add(newVenue)
        
        # genres= request.form['genres']

        # for genre in genres:  
        #     newGenre = Genres(
        #       Venue_id = newVenue.id,
        #       genre = genres[genre]
        #     )
        #     db.session.add_all(newGenre)

        db.session.commit()

        flash('Venue '+  request.form['name']  +' was successfully listed!') 
      except:
        db.session.rollback()
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
      finally:
        db.session.close()
        return render_template('pages/home.html')
 

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()

  return redirect(url_for('index'))
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  artists = Artist.query.group_by(Artist.id).all()
  data =[]
  
  for artist in artists:
        data.append({
          "name": artist.name,
          "city": artist.city,
          "state": artist.state,
          "venue.phone": artist.phone,
          "facebook_link": artist.facebook_link
        })
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  term = request.form.get('search_term', '')

  artists = Artist.query.filter(Artist.name.ilike(f'%{term}%'))

  response={
    "count": artists.count(),
    "data": artists
  }
  return render_template('pages/search_artists.html', results=response, search_term=term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.get(artist_id)
  past_shows = []
  upcoming_shows = []
  current_time = datetime.now()
  upcoming_shows_details = db.session.query(Show).join(Artist).filter(Show.venue_id==venue_id).all()
  past_show_details=db.session.query(Show).join(Artist).filter(Show.venue_id==venue_id).all()
  data_shows = []

 for show in upcoming_shows_details:
      data_shows.append({
      #here you data as start_time
      'start_time': show.start_time.strftime('%Y-%m-%d %H:%M:%S'),
      })
      if data_shows.start_time > current_time:
          upcoming_shows.append(data)

  for show in past_show_details:
      data_shows.append({
      #here you data as start_time
      'start_time': show.start_time.strftime('%Y-%m-%d %H:%M:%S'),
      })
      if data_shows.start_time > current_time:
          past_shows.append(data)


  data={
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "facebook_link": artist.facebook_link,
    "image_link": artist.image_link,
    "seeking_venue": artist.seeking_venue,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows)
  }
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)

  artistData = {
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link
    }
  return render_template('forms/edit_artist.html', form=form, artist=artistData)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  try:
    form = ArtistForm()

    artist = Artist.query.get(artist_id)


    artist.name = form.name.data
    artist.phone = form.phone.data
    artist.state = form.state.data
    artist.city = form.city.data
    artist.genres = form.genres.data
    artist.image_link = form.image_link.data
    artist.facebook_link = form.facebook_link.data
    artist.website = form.website
    artist.seeking_venue = form.seeking_venue
    artist.seeking_description = form.seeking_description
  
    db.session.commit()
  except:
    db.session.rolback()
  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  venue={
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "image_link": venue.image_link,
    "facebook_link": venue.facebook_link,
    "website": venue.website,    
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
  }
  
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  try:
    form = VenueForm()
    venue = Venue.query.get(venue_id)

    venue.name = form.name.data
    venue.genres = form.genres.data
    venue.city = form.city.data
    venue.state = form.state.data
    venue.address = form.address.data
    venue.phone = form.phone.data
    venue.facebook_link = form.facebook_link.data
    venue.website = form.website.data
    venue.image_link = form.image_link.data
    venue.seeking_talent = form.seeking_talent.data
    venue.seeking_description = form.seeking_description.data

    db.session.commit()
  except:
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
      form = ArtistForm(request.form)
      try:
        newArtist = Artist(
        name=form.name.data, 
        city= form.city.data, 
        address=form.address.data ,
        genres =form.genres.getlist ,
        phone=form.phone.data ,  
        facebook_link=form.facebook_link.data,
        image_link =form.image_link.data ,
        seeking_venu =form.seeking_venu.data ,
        seeking_description =form.seeking_description.data
        )
        db.session.add(newArtist)
        db.session.commit()

        flash('Artist ' + request.form['name'] + ' was successfully listed!')
      except:
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
      finally:
        db.session.close()
        return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  
  data = []
  shows = Show.query.all()  
  for show in shows:
        data.append({
            'venue_id': show.venue.id,
            'venue_name': show.venue.name,
            'artist_id': show.artist.id,
            'artist_name': show.artist.name,
            'artist_image_link': show.artist.image_link,
            'start_time': show.start_time.isoformat()
        })
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
      form = ShowForm(request.form)
      try:
        newShow = Show(
        artist_id =form.artist_id.data, 
        venue_id=form.venue_id.data, 
        start_time=form.start_time.data
        )
        db.session.add(newShow)
        db.session.commit()

        flash('Show was successfully listed!')
      except:
        flash('An error occurred. Show could not be listed.')
      finally:
        db.session.close()
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
