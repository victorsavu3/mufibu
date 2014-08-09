from db import Session
from db import Person, Job, SeriesJob, Tag, Series, Note, Entity, File, Rating, User

session = Session()

user1 = User()
user1.name="Lisa"

user2 = User()
user2.name="Hanne"

user3 = User()
user3.name="Deindra"

user4 = User()
user4.name="Niklas"

user5 = User()
user5.name="Leander"

user6 = User()
user6.name="Piotr"

user7 = User()
user7.name="Victor"

session.add(user1)
session.add(user2)
session.add(user3)
session.add(user4)
session.add(user5)
session.add(user6)
session.add(user7)

session.commit()
