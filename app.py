#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

#------#
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form 
from forms import *
from flask_migrate import Migrate

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')


# TODO: connect to a local postgresql database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    genres = db.Column(db.String())## missing fields
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))## missing fields
    seeking_talent = db.Column(db.Boolean, default=False)## missing fields
    seeking_description = db.Column(db.String(500))## missing fields
    shows = db.relationship('Show', backref="venue", lazy=True) ##  relationship between show and venue
    # TODO: implement any missing fields, as a database migration using Flask-Migrate

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
    website = db.Column(db.String(120)) ##missing field
    seeking_venue = db.Column(db.Boolean)##missing field
    seeking_description = db.Column(db.String(500))##missing field
    shows = db.relationship('Show', backref="artist", lazy=True) ## relationship between artist and show
    # TODO: implement any missing fields, as a database migration using Flask-Migrate


# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'),nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False )##


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

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
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
 # data=[{
  #  "city": "San Francisco",
   # "state": "CA",
    #"venues": [{
     # "id": 1,
      #"name": "The Musical Hop",
      #"num_upcoming_shows": 0,
    #}, {
     # "id": 3,
      #"name": "Park Square Live Music & Coffee",
      #"num_upcoming_shows": 1,
    #}]
  #}, {
    #"city": "New York",
    #"state": "NY",
    #"venues": [{
      #"id": 2,
      #"name": "The Dueling Pianos Bar",
      #"num_upcoming_shows": 0,
    #}]
  #}]

 states = Venue.query.with_entities(
        Venue.state, Venue.city).group_by(Venue.state, Venue.city).all()
 data = []
 for state, city in states:
     venues = Venue.query.with_entities(Venue.id, Venue.name).filter_by(
        state=state, city=city).order_by('id').all()
     data.append({'city': city,'state': state,'venues': venues})#####

 return render_template('pages/venues.html', areas=data)



#########################
@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
 # response={
 #   "count": 1,
  #  "data": [{
   #   "id": 2,
    #  "name": "The Dueling Pianos Bar",
     # "num_upcoming_shows": 0,
    #}]
  #}
 key = '%' + request.form.get('search_term') + '%'
 values = Venue.query.filter(Venue.name.ilike(key)).all()
 response = {'count': len(values), 'data': values}

 return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))



@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  
  #data1={
    #"id": 1,
    #"name": "The Musical Hop",
    #"genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    #"address": "1015 Folsom Street",
    #"city": "San Francisco",
    #"state": "CA",
    #"phone": "123-123-1234",
    #"website": "https://www.themusicalhop.com",
    #"facebook_link": "https://www.facebook.com/TheMusicalHop",
    #"seeking_talent": True,
    #"seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    #"image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    #"past_shows": [{
      #"artist_id": 4,
      #"artist_name": "Guns N Petals",
      #"artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
      #"start_time": "2019-05-21T21:30:00.000Z"
    #}],
    #"upcoming_shows": [],
    #"past_shows_count": 1,
    #"upcoming_shows_count": 0,
  #}
  #data2={
    #"id": 2,
    #"name": "The Dueling Pianos Bar",
    #"genres": ["Classical", "R&B", "Hip-Hop"],
    #"address": "335 Delancey Street",
    #"city": "New York",
    #"state": "NY",
    #"phone": "914-003-1132",
    #"website": "https://www.theduelingpianos.com",
    #"facebook_link": "https://www.facebook.com/theduelingpianos",
    #"seeking_talent": False,
    #"image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
    #"past_shows": [],
    #"upcoming_shows": [],
    #"past_shows_count": 0,
    #"upcoming_shows_count": 0,
  #}
  #data3={
    #"id": 3,
    #"name": "Park Square Live Music & Coffee",
    #"genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
    #"address": "34 Whiskey Moore Ave",
    #"city": "San Francisco",
    #"state": "CA",
    #"phone": "415-000-1234",
    #"website": "https://www.parksquarelivemusicandcoffee.com",
    #"facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    #"seeking_talent": False,
    #"image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    #"past_shows": [{
      #"artist_id": 5,
      #"artist_name": "Matt Quevedo",
      #"artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      #"start_time": "2019-06-15T23:00:00.000Z"
    #}],
    #"upcoming_shows": [{
      #"artist_id": 6,
      #"artist_name": "The Wild Sax Band",
      #"artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      #"start_time": "2035-04-01T20:00:00.000Z"
    #}, {
      #"artist_id": 6,
      #"artist_name": "The Wild Sax Band",
      #"artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      #"start_time": "2035-04-08T20:00:00.000Z"
    #}, {
      #"artist_id": 6,
      #"artist_name": "The Wild Sax Band",
      #"artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      #"start_time": "2035-04-15T20:00:00.000Z"
    #}],
    #"past_shows_count": 1,
    #"upcoming_shows_count": 1,
  #}
  #data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
   venue = Venue.query.get(venue_id)
   shows = venue.shows
   upcoming_shows = []
   past_shows = []
   for show in shows:
       if show.start_time > datetime.utcnow():
          upcoming_shows.append(show)
       else:
         past_shows.append(show)
         show.start_time = str(show.start_time)
         show.artist_image_link = show.artist.image_link
         show.artist_name = show.artist.name

   venue.upcoming_shows = upcoming_shows
   venue.upcoming_shows_count = len(upcoming_shows)
   venue.past_shows = past_shows
   venue.past_shows_count = len(past_shows)
   return render_template('pages/show_venue.html', venue=venue)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  # on successful db insert, flash success
 data = request.form
 name = data.get('name')
 city = data.get('city')
 state = data.get('state')
 address = data.get('address')
 phone = data.get('phone')
 #genres = data.get('genres')
 genres = ", ".join(data.getlist('genres'))
 facebook_link = data.get('facebook_link')

 venue = Venue(name=name, city=city, state=state, address=address, phone=phone, genres=genres, facebook_link=facebook_link)

 try:
    db.session.add(venue)
    db.session.commit()
    flash('Venue ' + name + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
 except:
        db.session.rollback()
        flash('An error occurred. Venue ' + name + ' could not be listed.')
 finally:
        db.session.close()

 return redirect(url_for("index"))


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    Venue.query.filter_by(id=venue_id).delete()
    try:
        db.session.commit()
        flash("The venue with id %r has been deleted" % venue_id)
    except:
        db.session.rollback()
        flash("The venue with id %r was not deleted" % venue_id)
    finally:
        db.session.close()

    return redirect(url_for('venues'))

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  #data=[{
    #"id": 4,
    #"name": "Guns N Petals",
  #}, {
    #"id": 5,
    #"name": "Matt Quevedo",
  #}, {
    #"id": 6,
    #"name": "The Wild Sax Band",
  #}]
  data = Artist.query.with_entities(Artist.id, Artist.name).order_by('id').all()##

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  #response={
   # "count": 1,
    #"data": [{
     # "id": 4,
      #"name": "Guns N Petals",
      #"num_upcoming_shows": 0,
    #}]
  #}
   key = '%' + request.form.get('search_term') + '%'
   values = Artist.query.filter(Artist.name.ilike(key)).all()
   response = {'count': len(values), 'data': values}

   return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  #data1={
    #"id": 4,
    #"name": "Guns N Petals",
    #"genres": ["Rock n Roll"],
    #"city": "San Francisco",
    #"state": "CA",
    #"phone": "326-123-5000",
    #"website": "https://www.gunsnpetalsband.com",
    #"facebook_link": "https://www.facebook.com/GunsNPetals",
    #"seeking_venue": True,
    #"seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    #"image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    #"past_shows": [{
      #"venue_id": 1,
      #"venue_name": "The Musical Hop",
      #"venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
      #"start_time": "2019-05-21T21:30:00.000Z"
    #}],
    #"upcoming_shows": [],
    #"past_shows_count": 1,
    #"upcoming_shows_count": 0,
  #}
  #data2={
    #"id": 5,
    #"name": "Matt Quevedo",
    #"genres": ["Jazz"],
    #"city": "New York",
    #"state": "NY",
    #"phone": "300-400-5000",
    #"facebook_link": "https://www.facebook.com/mattquevedo923251523",
    #"seeking_venue": False,
    #"image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    #"past_shows": [{
      #"venue_id": 3,
      #"venue_name": "Park Square Live Music & Coffee",
      #"venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      #"start_time": "2019-06-15T23:00:00.000Z"
    #}],
    #"upcoming_shows": [],
    #"past_shows_count": 1,
    #"upcoming_shows_count": 0,
  #}
  #data3={
    #"id": 6,
    #"name": "The Wild Sax Band",
    #"genres": ["Jazz", "Classical"],
    #"city": "San Francisco",
    #"state": "CA",
    #"phone": "432-325-5432",
    #"seeking_venue": False,
    #"image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    #"past_shows": [],
    #"upcoming_shows": [{
      #"venue_id": 3,
      #"venue_name": "Park Square Live Music & Coffee",
      #"venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      #"start_time": "2035-04-01T20:00:00.000Z"
    #}, {
      #"venue_id": 3,
      #"venue_name": "Park Square Live Music & Coffee",
      #"venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      #"start_time": "2035-04-08T20:00:00.000Z"
    #}, {
      #"venue_id": 3,
      #"venue_name": "Park Square Live Music & Coffee",
      #"venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      #"start_time": "2035-04-15T20:00:00.000Z"
    #}],
    #"past_shows_count": 0,
    #"upcoming_shows_count": 3,
 # }
  #data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
    artist = Artist.query.get(artist_id)
    shows = artist.shows
    upcoming_shows = []
    past_shows = []
    for show in shows:
        if show.start_time > datetime.utcnow():
            upcoming_shows.append(show)
        else:
            past_shows.append(show)
        show.start_time = str(show.start_time)
        show.venue_image_link = show.venue.image_link
        show.venue_name = show.venue.name

    artist.upcoming_shows = upcoming_shows
    artist.upcoming_shows_count = len(upcoming_shows)
    artist.past_shows = past_shows
    artist.past_shows_count = len(past_shows)
 
    return render_template('pages/show_artist.html', artist=artist)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = artist.query.get(artist_id)


 # artist={
    #"id": 4,
    #"name": "Guns N Petals",
    #"genres": ["Rock n Roll"],
    #"city": "San Francisco",
    #"state": "CA",
    #"phone": "326-123-5000",
    #"website": "https://www.gunsnpetalsband.com",
    #"facebook_link": "https://www.facebook.com/GunsNPetals",
    #"seeking_venue": True,
    #"seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    #"image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  #}

  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)



@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

 data = request.form
 artist = Artist.query.get(artist_id)
 prev_name = artist.name
 artist.name = data.get('name')
 artist.city = data.get('city')
 artist.state = data.get('state')
 artist.address = data.get('address')
 artist.phone = data.get('phone')
 artist.genres = ", ".join(data.getlist('genres'))
 artist.facebook_link = data.get('facebook_link')
 try:
    db.session.commit()
    flash('Artist ' + prev_name + ' was successfully updated!')
 except:
     db.session.rollback()
     flash('An error occurred. Artist ' +  prev_name + ' could not be updated.')
 finally:
     db.session.close()
  
 return redirect(url_for('show_artist', artist_id=artist_id))



@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)

  #venue={
    #"id": 1,
    #"name": "The Musical Hop",
    #"genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    #"address": "1015 Folsom Street",
    #"city": "San Francisco",
    #"state": "CA",
    #"phone": "123-123-1234",
    #"website": "https://www.themusicalhop.com",
    #"facebook_link": "https://www.facebook.com/TheMusicalHop",
    #"seeking_talent": True,
    #"seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    #"image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  #}

  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
    data = request.form
    venue = Venue.query.get(venue_id)
    prev_name = venue.name
    venue.name = data.get('name')
    venue.city = data.get('city')
    venue.state = data.get('state')
    venue.address = data.get('address')
    venue.phone = data.get('phone')
    venue.genres = ", ".join(data.getlist('genres'))
    venue.facebook_link = data.get('facebook_link')
    try:
        db.session.commit()
        flash('Venue ' + prev_name + ' was successfully updated!')
    except:
        db.session.rollback()
        flash('An error occurred. Venue ' +
            prev_name + ' could not be updated.')
    finally:
        db.session.close()

    return redirect(url_for('show_venue', venue_id=venue_id))

#------------------------------------------------------------------
#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  data = request.form#
  name = data.get('name')
  city = data.get('city')
  state = data.get('state')
  phone = data.get('phone')
  genres = ", ".join(data.getlist('genres'))
  facebook_link = data.get('facebook_link')
  artist = Artist(name=name, city=city, state=state, phone=phone, genres=genres, facebook_link=facebook_link)
   # on successful db insert, flash success
  try:
     db.session.add(artist)
     db.session.commit()
     flash('Artist ' + name + ' was successfully listed!')
   # TODO: on unsuccessful db insert, flash an error instead.
   # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')

  except:
     db.session.rollback()
     flash('An error occurred. Artist ' + name + ' could not be listed.')
  finally:
     db.session.close()

  return render_template('pages/home.html')

 
#------------------------------------------------------------------
#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  #data=[{
    #"venue_id": 1,
    #"venue_name": "The Musical Hop",
    #"artist_id": 4,
    #"artist_name": "Guns N Petals",
    #"artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    #"start_time": "2019-05-21T21:30:00.000Z"
  #}, {
    #"venue_id": 3,
    #"venue_name": "Park Square Live Music & Coffee",
    #"artist_id": 5,
    #"artist_name": "Matt Quevedo",
    #"artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    #"start_time": "2019-06-15T23:00:00.000Z"
  #}, {
    #"venue_id": 3,
    #"venue_name": "Park Square Live Music & Coffee",
    #"artist_id": 6,
    #"artist_name": "The Wild Sax Band",
    #"artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    #"start_time": "2035-04-01T20:00:00.000Z"
  #}, {
    #"venue_id": 3,
    #"venue_name": "Park Square Live Music & Coffee",
    #"artist_id": 6,
    #"artist_name": "The Wild Sax Band",
    #"artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    #"start_time": "2035-04-08T20:00:00.000Z"
  #}, {
    #"venue_id": 3,
    #"venue_name": "Park Square Live Music & Coffee",
    #"artist_id": 6,
    #"artist_name": "The Wild Sax Band",
    #"artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    #"start_time": "2035-04-15T20:00:00.000Z"
  #}]
  data = Show.query.all()
  for d in data:
        d.artist_name = d.artist.name
        d.artist_image_link = d.artist.image_link
        d.venue_name = d.venue.name
        d.start_time = str(d.start_time)

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
    data = request.form#
    artist_id = data.get('artist_id')
    venue_id = data.get('venue_id')
    start_time = dateutil.parser.parse(data.get('start_time'))
    show = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
    # on successful db insert, flash success

    try:
        db.session.add(show)
        db.session.commit()
        flash('Show was successfully listed!')

  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    except:
        db.session.rollback()
        flash('An error occurred. Show could not be listed, make sure the artist and the venue id already exists!')
    finally:
        db.session.close()

    return redirect(url_for('index'))


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


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
