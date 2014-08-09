from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Binary, Enum, ForeignKey
from sqlalchemy import Table
from sqlalchemy.orm import relationship, backref

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///db.db', echo=True)

Session = sessionmaker()
Session.configure(bind=engine)

Base = declarative_base()

class Person(Base):
	__tablename__ = 'person'

	id = Column(Integer, primary_key=True)
	name = Column(String)

	location = Column(String)

	jobs = relationship("Job", backref="person")
	series_jobs = relationship("SeriesJob", backref="person")

	image_id = Column(Integer, ForeignKey('file.id'))

class Job(Base):
	__tablename__ = 'entity_person'

	id = Column(Integer, primary_key=True)
	
	person_id = Column(Integer, ForeignKey('person.id'))
	entity_id = Column(Integer, ForeignKey('entity.id'))

	type = Column(Enum('band', 'author', 'actor', 'director', 'producer', 'singer', 'composer', 'production_company', 'publisher'))

class SeriesJob(Base):
	__tablename__ = 'series_person'

	id = Column(Integer, primary_key=True)
	
	person_id = Column(Integer, ForeignKey('person.id'))
	series_id = Column(Integer, ForeignKey('series.id'))

	type = Column(Enum('band', 'singer', 'producer'))

tag_entity = Table('tag_entity', Base.metadata,
	Column('entity_id', Integer, ForeignKey('entity.id')),
	Column('tag_id', Integer, ForeignKey('tag.id'))
)

tag_series = Table('tag_series', Base.metadata,
	Column('series_id', Integer, ForeignKey('series.id')),
	Column('tag_id', Integer, ForeignKey('tag.id'))
)

class Tag(Base):
	__tablename__ = 'tag'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	type = Column(Enum('genre', 'keyword'))

	entities = relationship("Entity",
                    secondary=tag_entity,
                    backref="tags")

	series = relationship("Series",
                    secondary=tag_series,
                    backref="tags")

class Series(Base):
	__tablename__ = 'series'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	type = Column(Enum('album', 'movie_series', 'book_series', 'soundtrack'))

	first_year = Column(Integer)
	last_year = Column(Integer)

	image_id = Column(Integer, ForeignKey('file.id'))

	entities = relationship("Entity", backref="series", foreign_keys="Entity.series_id")
	soundtrack_for = relationship("Entity", backref="soundtrack", foreign_keys="Entity.soundtrack_id")

	jobs = relationship("SeriesJob", backref="series")

class Note(Base):
	__tablename__ = 'note'

	id = Column(Integer, primary_key=True)
	type = Column(Enum('quote', 'note', 'trailer'))
	contents = Column(String)

	entity_id = Column(Integer, ForeignKey('entity.id'))

class Entity(Base):
	__tablename__ = 'entity'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	type = Column(Enum('movie', 'book', 'song'))

	year = Column(Integer)
	description = Column(String)
	length = Column(Integer)
	isbn = Column(String)

	image_id = Column(Integer, ForeignKey('file.id'))
	data_id = Column(Integer, ForeignKey('file.id'))

	series_id = Column(Integer, ForeignKey('series.id'))

	series_order = Column(Integer)
	soundtrack_id = Column(Integer, ForeignKey('series.id'))

	notes = relationship("Note", backref="entity")

	ratings = relationship("Rating", backref="entity")

	jobs = relationship("Job", backref="entity")

	book_id = Column(Integer, ForeignKey('entity.id'))
	movie_id = Column(Integer, ForeignKey('entity.id'))

	books_from = relationship("Entity", backref=backref('movie', remote_side=[id]), foreign_keys="Entity.movie_id")
	movies_from = relationship("Entity", backref=backref('book', remote_side=[id]), foreign_keys="Entity.book_id")

class File(Base):
	__tablename__ = 'file'

	id = Column(Integer, primary_key=True)
	data = Column(Binary)
	name = Column(String)
	type = Column(Enum('image', 'song', 'book'))
	mime = Column(String)

	image_references = relationship("Entity", backref="image", foreign_keys=Entity.image_id)
	data_references = relationship("Entity", backref="data", foreign_keys=Entity.data_id)

	image_series_references = relationship("Series", backref="image")
	person_references = relationship("Person", backref="image")

class Rating(Base):
	__tablename__ = 'rating'

	id = Column(Integer, primary_key=True)
	value = Column(Integer)

	entity_id = Column(Integer, ForeignKey('entity.id'))
	user_id = Column(Integer, ForeignKey('user.id'))

class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True)
	name = Column(String)

	ratings = relationship("Rating", backref="user")

Base.metadata.create_all(engine)
