from flask import Flask, Response, request, render_template, url_for, send_from_directory, redirect
from werkzeug.utils import secure_filename

from mimetypes import guess_type

from sqlalchemy import or_, and_, func

from db import Session
from db import Person, Job, SeriesJob, Tag, Series, Note, Entity, File, Rating, User

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
	return render_template("index.html")

@app.route('/file/<int:id>')
def file(id):
	session = Session()

	f = session.query(File).filter(File.id == id) .first()

	return Response(f.data, mimetype=f.mime)

@app.route("/list/<type>", methods=['GET'])
def list(type):
	session = Session()

	entites = session.query(Entity).filter(Entity.type == type).all()

	rendered = render_template("tiles.html", entities=entites, type=type)

	session.commit()

	return rendered

@app.route("/manage/series", methods=['GET'])
def manage_series():
	session = Session()

	series = session.query(Series).all()
	persons = session.query(Person).all()

	rendered = render_template("series.html", series=series, persons=persons)

	session.commit()

	return rendered

@app.route("/manage/files", methods=['GET'])
def manage_files():
	session = Session()

	files = session.query(File).all()

	rendered = render_template("files.html", files=files)

	session.commit()

	return rendered

@app.route("/manage/persons", methods=['GET'])
def manage_persons():
	session = Session()

	persons = session.query(Person).all()

	rendered = render_template("persons.html", persons=persons)

	session.commit()

	return rendered

@app.route("/manage/tags", methods=['GET'])
def manage_tags():
	session = Session()

	tags = session.query(Tag).all()

	rendered = render_template("tags.html", tags=tags)

	session.commit()

	return rendered

@app.route("/item/<int:id>", methods=['GET'])
def item(id):
	session = Session()

	entity = session.query(Entity).filter(Entity.id == id).first()

	persons = session.query(Person).all()
	users = session.query(User).all()

	rating = session.query(func.avg(Rating.value).label('rating')).filter(Rating.entity_id == id).first().rating

	rendered = render_template("item.html", entity=entity, persons=persons, users=users, rating=rating)

	return rendered

@app.route("/form/file", methods=['GET'])
def form_file():
	return render_template("form_file.html")

@app.route("/form/entity/<type>/<int:id>", methods=['GET'])
@app.route("/form/entity/<type>", methods=['GET'])
def form_entity(type, id=None):
	session = Session()

	entity = None
	tag_ids = None

	if id != None:
		entity = session.query(Entity).filter(Entity.id == id).first()
		tag_ids = [ tag.id for tag in entity.tags ]
	
	files = None
	series = None
	soundtracks = None

	if(type == 'song'):
		files = session.query(File).filter(File.type == 'song').all()
		series = session.query(Series).filter(or_(Series.type == 'album', Series.type == 'soundtrack')).all()
	if(type == 'book'):
		files = session.query(File).filter(File.type == 'book').all()
		series = session.query(Series).filter(Series.type == 'book_series').all()
	if(type == 'movie'):
		series = session.query(Series).filter(Series.type == 'movie_series').all()
		soundtracks = session.query(Series).filter(Series.type == 'soundtrack').all()

	covers = session.query(File).filter(File.type == 'image').all()
	keywords = session.query(Tag).filter(Tag.type == 'keyword').all()
	genres = session.query(Tag).filter(Tag.type == 'genres').all()

	rendered = render_template("form_entity.html", type=type, entity=entity, covers=covers, files=files, 
		series=series, soundtracks=soundtracks, keywords=keywords, genres=genres, tag_ids=tag_ids)

	session.commit()

	return rendered

@app.route("/form/series/<type>/<int:id>", methods=['GET'])
@app.route("/form/series/<type>", methods=['GET'])
def form_series(type, id=None):
	session = Session()

	series = None

	if id != None:
		series = session.query(Series).filter(Series.id == id).first()
		tag_ids = [ tag.id for tag in series.tags ]
	
	covers = session.query(File).filter(File.type == 'image').all()
	keywords = session.query(Tag).filter(Tag.type == 'keyword').all()

	rendered = render_template("form_series.html", type=type, series=series, covers=covers, keywords=keywords)

	session.commit()

	return rendered

@app.route("/form/person/<int:id>", methods=['GET'])
@app.route("/form/person", methods=['GET'])
def form_person(id=None):
	session = Session()

	person = None

	if id != None:
		person = session.query(Person).filter(Person.id == id).first()
	
	covers = session.query(File).filter(File.type == 'image').all()

	rendered = render_template("form_person.html", person=person, covers=covers)

	session.commit()

	return rendered

@app.route("/form/tag/<type>/<int:id>", methods=['GET'])
@app.route("/form/tag/<type>", methods=['GET'])
def form_tag(type, id=None):
	session = Session()
	
	tag = None

	if id != None:
		tag = session.query(Tag).filter(Tag.id == id).first()

	rendered = render_template("form_tag.html", type=type, tag=tag)

	session.commit()

	return rendered

@app.route("/submit/person", methods=['POST'])
def submit_person():
	session = Session()

	person = None

	if 'id' in request.form:
		person = session.query(Person).filter(Person.id == request.form['id']).first()
	else:
		person = Person()

	person.name = request.form['name']
	if 'location' in request.form:
		person.location = request.form['location']

	if 'image_id' in request.form and request.form['image_id']:
		person.image_id = request.form['image_id']
	elif('cover' in request.files) and request.files['cover'] and request.files['cover'].filename:
		upload = request.files['cover']
		file = File()

		file.name = secure_filename(upload.filename)
		file.type = 'image'
		file.mime = guess_type(file.name)[0]
		file.data = upload.read()

		person.image = file

	session.add(person)

	session.commit()

	return redirect(url_for('index'))

@app.route("/submit/tag/<type>", methods=['POST'])
def submit_tag(type):
	session = Session()

	tag = None

	if 'id' in request.form:
		tag = session.query(Tag).filter(Tag.id == request.form['id']).first()
	else:
		tag = Tag()

	tag.name = request.form['name']
	tag.type = type

	session.add(tag)

	session.commit()

	return redirect(url_for('index'))

@app.route("/submit/job", methods=['POST'])
def submit_job():
	session = Session()

	job = Job()

	job.entity_id = request.form['entity_id']
	job.person_id = request.form['person_id']
	job.type = request.form['type']

	session.add(job)

	session.commit()

	return redirect(url_for('item', id=request.form['entity_id']))

@app.route("/submit/series_job", methods=['POST'])
def submit_series_job():
	session = Session()

	job = SeriesJob()

	job.series_id = request.form['series_id']
	job.person_id = request.form['person_id']
	job.type = request.form['type']

	session.add(job)

	session.commit()

	return redirect(url_for('manage_series'))

@app.route("/submit/rating", methods=['POST'])
def submit_rating():
	session = Session()

	rating = Rating()

	rating.entity_id = request.form['entity_id']
	rating.user_id = request.form['user_id']

	rating.value = request.form['value']

	if int(rating.value) > 0 and int(rating.value) <= 5:
		session.add(rating)

	session.commit()

	return redirect(url_for('item', id=request.form['entity_id']))

@app.route("/submit/note", methods=['POST'])
def submit_note():
	session = Session()

	note = Note()

	note.entity_id = request.form['entity_id']

	note.type = request.form['type']
	note.contents = request.form['contents']

	session.add(note)

	session.commit()

	return redirect(url_for('item', id=request.form['entity_id']))

@app.route("/submit/series/<type>", methods=['POST'])
def submit_series(type):
	session = Session()

	series = None

	if 'id' in request.form:
		series = session.query(Series).filter(Series.id == request.form['id']).first()
	else:
		series = Series()

	series.name = request.form['name']
	series.type = type
	
	if 'first_year' in request.form:
		series.first_year = request.form['first_year']
	if 'last_year' in request.form:
		series.last_year = request.form['last_year']

	if 'image_id' in request.form and request.form['image_id']:
		series.image_id = request.form['image_id']
	elif('cover' in request.files) and request.files['cover'] and request.files['cover'].filename:
		upload = request.files['cover']
		file = File()

		file.name = secure_filename(upload.filename)
		file.type = 'image'
		file.mime = guess_type(file.name)[0]
		file.data = upload.read()

		series.image = file

	session.add(series)

	session.commit()

	return redirect(url_for('index'))

@app.route("/submit/file/<type>", methods=['POST'])
def submit_file(type):
	session = Session()

	file.type = type

	upload = request.files['data']

	file.name = secure_filename(upload.filename)
	file.mime = guess_type(file.name)[0]
	file.data = upload

	session.add(file)

	session.commit()

	return redirect(url_for('index'))

@app.route("/submit/entity/<type>", methods=['POST'])
def submit_entity(type):
	session = Session()

	entity = None

	if 'id' in request.form:
		entity = session.query(Entity).filter(Entity.id == request.form['id']).first()
	else:
		entity = Entity()

	entity.type = type

	entity.name = request.form['name']
	if 'description' in request.form:
		entity.description = request.form['description']
	if 'year' in request.form:
		entity.year = request.form['year']
	if 'length' in request.form:
		entity.length = request.form['length']
	if 'isbn' in request.form:
		entity.isbn = request.form['isbn']

	if 'series_id' in request.form and request.form['series_id']:
		entity.series_id = request.form['series_id']
	if 'soundtrack_id' in request.form and request.form['soundtrack_id']:
		entity.soundtrack_id = request.form['soundtrack_id']

	if 'image_id' in request.form and request.form['image_id']:
		entity.image_id = request.form['image_id']
	elif('cover' in request.files) and request.files['cover'] and request.files['cover'].filename:
		upload = request.files['cover']
		file = File()

		file.name = secure_filename(upload.filename)
		file.type = 'image'
		file.mime = guess_type(file.name)[0]
		file.data = upload.read()

		entity.image = file

	if 'data_id' in request.form and request.form['data_id']:
		entity.data_id = request.form['data_id']
	elif('data' in request.files) and request.files['data'] and request.files['data'].filename:
		upload = request.files['data']
		file = File()

		file.name = secure_filename(upload.filename)
		file.type = type
		file.mime = guess_type(file.name)[0]
		file.data = upload.read()

		entity.data = file

	tags = request.form.getlist('keywords') + request.form.getlist('genres')

	entity.tags = [ session.query(Tag).filter(Tag.id==tag_id).first() for tag_id in tags ]

	session.add(entity)

	session.commit()

	return redirect(url_for('index'))

@app.route("/delete/entity/<int:id>", methods=['POST'])
def delete_entity(id):
	session = Session()

	session.query(Entity).filter(Entity.id==id).delete()

	session.commit()

	return redirect(url_for('index'))

@app.route("/delete/tag/<int:id>", methods=['POST'])
def delete_tag(id):
	session = Session()

	session.query(Tag).filter(Tag.id==id).delete()

	session.commit()

	return redirect(url_for('manage_tags'))

@app.route("/delete/series/<int:id>", methods=['POST'])
def delete_series(id):
	session = Session()

	session.query(Series).filter(Series.id==id).delete()

	session.commit()

	return redirect(url_for('manage_series'))

@app.route("/delete/person/<int:id>", methods=['POST'])
def delete_person(id):
	session = Session()

	session.query(Person).filter(Person.id==id).delete()

	session.commit()

	return redirect(url_for('manage_persons'))

@app.route("/delete/rating/<int:id>", methods=['POST'])
def delete_rating(id):
	session = Session()

	session.query(Rating).filter(Rating.id==id).delete()

	session.commit()

	return redirect(url_for('index'))

@app.route("/delete/note/<int:id>", methods=['POST'])
def delete_note(id):
	session = Session()

	session.query(Note).filter(Note.id==id).delete()

	session.commit()

	return redirect(url_for('index'))

@app.route("/delete/file/<int:id>", methods=['POST'])
def delete_file(id):
	session = Session()

	session.query(File).filter(File.id==id).delete()

	session.commit()

	return redirect(url_for('manage_files'))

@app.route("/delete/job/<int:id>", methods=['POST'])
def delete_job(id):
	session = Session()

	session.query(Job).filter(Job.id==id).delete()

	session.commit()

	return redirect(url_for('index'))

@app.route("/delete/series_job/<int:id>", methods=['POST'])
def delete_series_job(id):
	session = Session()

	session.query(SeriesJob).filter(SeriesJob.id==id).delete()

	session.commit()

	return redirect(url_for('index'))

@app.route("/about", methods=['GET'])
def about():
	return render_template("about.html")

@app.route("/playlist", methods=['GET'])
def play():
	session = Session()

	entites = session.query(Entity).filter(Entity.type == 'song').all()

	session.commit()

	return render_template("playlist.html", entities=entites)

@app.route('/get-file/<filename>')
def send_file(filename):
	return send_from_directory('static/mp3', filename)

if __name__=='__main__':
	app.run(host='0.0.0.0', debug=True)
	
