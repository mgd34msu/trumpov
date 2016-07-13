# The following is a demonstration of using python's sqlite package to run SQL queries and return formatted data
# This will use information from a database containing information related to Academy Award winners
# available at https://www.aggdata.com/awards/oscar
import sqlite3 as sql

# initialize a connection to academy_awards.db
conn = sql.connect('academy_awards.db')

# find all of the years that the actress Natalie Portman was nominated for an award
portman_movies = conn.execute('SELECT ceremonies.year, nominations.movie FROM nominations INNER JOIN ceremonies ON nominations.ceremony_id == ceremonies.id WHERE nominations.nominee == "Natalie Portman";').fetchall()
print(portman_movies)

# create a join table of movies and actors
conn.execute('CREATE table movies_actors (id INTEGER PRIMARY KEY, movie_id INTEGER REFERENCES movies(id), actor_id INTEGER REFERENCES actors(id));')

# select the first five rows from the new join table, the actors table, and the movies table
movies_actors_query = 'SELECT * FROM movies_actors LIMIT 5;'
actors_query = 'SELECT * FROM actors LIMIT 5;'
movies_query = 'SELECT * FROM movies LIMIT 5;'

five_join_table = conn.execute(movies_actors_query).fetchall()
five_actors = conn.execute(actors_query).fetchall()
five_movies = conn.execute(movies_query).fetchall()

print(five_join_table, five_actors, five_movies)

# find all the actors that starred in The King's Speech
ks_query = '''SELECT actors.actor, movies.movie FROM movies INNER JOIN movies_actors ON movies.id == movies_actors.movie_id INNER JOIN actors ON movies_actors.actor_id == actors.id WHERE movies.movie == "The King's Speech";'''

kings_actors = conn.execute(ks_query).fetchall()

print(kings_actors)

# find all movies starring Natalie Portman
np_query = '''SELECT movies.movie, actors.actor FROM movies INNER JOIN movies_actors ON movies.id == movies_actors.movie_id INNER JOIN actors ON movies_actors.actor_id == actors.id WHERE actors.actor == "Natalie Portman";'''

portman_joins = conn.execute(np_query).fetchall()

print(portman_joins)
