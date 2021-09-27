from peewee import *
from datetime import datetime
import hashlib

database = MySQLDatabase('fastapi_cf',
                    user='root',
                    password='Machiniram117.',
                    host='localhost',
                    port=3306)

class User(Model):
    username = CharField(max_length=50, unique=True)
    password = CharField(max_length=50)
    created_at = DateTimeField(default=datetime.now())

    def __str__(self):
        return self.username
    @classmethod
    def create_password(cls,password):
        h = hashlib.md5()
        h.update(password.encode('utf-8'))
        return h.hexdigest()

    class Meta:
        database = database
        table_name = 'users'

class Movie(Model):
    title = CharField(max_length=50)
    created_at = DateTimeField(default=datetime.now())

    def __str__(self):
        return self.title

    class Meta:
        database = database
        table_name = 'movies'

class UserReview(Model):
    user = ForeignKeyField(User,backref='reviews')
    movie = ForeignKeyField(Movie, backref='reviews' )
    reviews = TextField()
    score = IntegerField()
    created_at = DateTimeField(default=datetime.now())
    
    def __str__(self):
        return f'{self.user.username} - {self.movie.title}'
    
    class Meta:
        database = database
        table_name = 'user_reviews'