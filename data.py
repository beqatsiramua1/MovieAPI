from main import db, MovieModel, UserModel

db.create_all()


movies = [
    {'id': 1, 'title': 'Interstellar', 'imdb': 8.6, 'release_date': 2014, 'director': 'Christopher Nolan', 'link': "https://www.imdb.com/title/tt0816692/"},
    {'id': 1, 'title': 'Inception', 'imdb': 8.8, 'release_date': 2010, 'director': 'Christopher Nolan', 'link': "https://www.imdb.com/title/tt1375666/?ref_=nv_sr_srsg_0"},
    {'id': 1, 'title': 'The Prestige', 'imdb': 8.5, 'release_date': 2006, 'director': 'Christopher Nolan', 'link': "https://www.imdb.com/title/tt0482571/?ref_=nv_sr_srsg_0"},
    {'id': 1, 'title': 'Shutter Island"', 'imdb': 8.2, 'release_date': 2010, 'director': 'Martin Scorsese', 'link': "https://www.imdb.com/title/tt1130884/?ref_=nv_sr_srsg_0"},
    {'id': 1, 'title': 'The Dark Knight', 'imdb': 9.0, 'release_date': 2008, 'director': 'Christopher Nolan', 'link': "https://www.imdb.com/title/tt0468569/?ref_=nv_sr_srsg_0"},
    {'id': 1, 'title': 'Forrest Gump', 'imdb': 8.8, 'release_date': 1994, 'director': "Robert Zemeckis", 'link': "https://www.imdb.com/title/tt0109830/?ref_=nv_sr_srsg_0"},
    {'id': 1, 'title': 'The Shawshank Redemption', 'imdb': 9.3, 'release_date': 1994, 'director': 'Frank Darabont', 'link': "https://www.imdb.com/title/tt0111161/?ref_=nv_sr_srsg_0"},
    {'id': 1, 'title': 'The Usual Suspects', 'imdb': 8.5, 'release_date': 1995, 'director': 'Bryan Singer', 'link': "https://www.imdb.com/title/tt0114814/?ref_=nv_sr_srsg_0"},
    {'id': 1, 'title': 'The Imitation Game', 'imdb': 8.0, 'release_date': 2014, 'director': 'Morten Tyldum', 'link': "https://www.imdb.com/title/tt2084970/?ref_=nv_sr_srsg_0"},
    {'id': 1, 'title': "Knockin' on Heaven's Door", 'imdb': 7.9, 'release_date': 1997, 'director': 'Thomas Jahn', 'link': "https://www.imdb.com/title/tt0119472/?ref_=nv_sr_srsg_0"},
    {'id': 1, 'title': 'Primal Fear', 'imdb': 7.7, 'release_date': 1996, 'director': 'Gregory Hoblit', 'link': "https://www.imdb.com/title/tt0117381/?ref_=nv_sr_srsg_0"},
    {'id': 1, 'title': 'The Invisible Guest', 'imdb': 8.1, 'release_date': 2016, 'director': 'Oriol Paulo', 'link': "https://www.imdb.com/title/tt4857264/?ref_=nv_sr_srsg_0"},

]


def create_database():
    for movie in movies:
        allmovie = MovieModel(title=movie['title'], imdb=movie['imdb'], release_date=movie['release_date'],
                              director=movie['director'], link=movie['link'])
        db.session.add(allmovie)
        db.session.commit()


if __name__ == "__main__":
    create_database()