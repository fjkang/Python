import urllib
import json
import time
import web

urls = (
    '/', 'index',
    '/movie/(.*)', 'movie',
    '/cast/(.*)', 'cast',
    '/director/(.*)', 'director',
)

class index:
    def GET(self):
        movies = db.select('movie')
        statement = 'SELECT COUNT(*) AS COUNT FROM movie'
        result = db.query(statement)
        data = result[0]
        count = data['COUNT']
        return render.index(movies, count, None)

    def POST(self):
        key = web.input()
        condition = r'title like "%' + key.title + r'%"'
        movies = db.select('movie', where=condition)
        statement = 'SELECT COUNT(*) AS COUNT FROM movie WHERE ' + condition
        result = db.query(statement)
        data = result[0]
        count = data['COUNT']
        return render.index(movies, count, key.title)


class movie:
    def GET(self, movie_id):
        movie_id = movie_id
        condition = r'id=' + movie_id
        movie = db.select('movie', where=condition)[0]
        return render.movie(movie)


class cast:
    def GET(self, cast_name):
        condition = r'casts like "%' + cast_name + '%"'
        movies = db.select('movie', where=condition)
        statement = 'SELECT COUNT(*) AS COUNT FROM movie WHERE ' + condition
        result = db.query(statement)
        data = result[0]
        count = data['COUNT']
        return render.index(movies, count, cast_name)


class director:
    def GET(self, director_name):
        condition = r'directors like "%' + director_name + '%"'
        movies = db.select('movie', where=condition)
        statement = 'SELECT COUNT(*) AS COUNT FROM movie WHERE ' + condition
        result = db.query(statement)
        data = result[0]
        count = data['COUNT']
        return render.index(movies, count, director_name)


render = web.template.render('templates/')
db = web.database(dbn='sqlite', db='douban.db')

'''movie_ids = []
for index in range(0, 250, 50):
    print index
    response = urllib.urlopen('http://api.douban.com/v2/movie/top250?start=%d&count=50' % index)
    data = response.read()
    data_json = json.loads(data)
    movie250 = data_json['subjects']
    for movie in movie250:
        movie_ids.append(movie['id'])
        print movie['id'], movie['title']
    time.sleep(3)
print movie_ids

def add_movie(data):
    try:
        movie = json.loads(data)
        print movie['title']
        db.insert('movie',
                  id=int(movie['id']),
                  title=movie['title'],
                  origin=movie['original_title'],
                  url=movie['alt'],
                  image=movie['images']['large'],
                  directors=','.join([d['name'] for d in movie['directors']]),
                  casts=','.join([c['name'] for c in movie['casts']]),
                  year=movie['year'],
                  genres=','.join(movie['genres']),
                  countries=','.join(movie['countries']),
                  summary=movie['summary'],
                  )
    except:
        db.insert('movie',
                  id=int(mid),
                  )'''

def get_poster(id, url):
    pic = urllib.urlopen(url).read()
    file_name = r'poster/%d.jpg' % id
    f = file(file_name, 'wb')
    f.write(pic)
    f.close()

'''movies = db.select('movie')
count = 0
for movie in movies:
    if movie.image:
        get_poster(movie.id, movie.image)
    count += 1
    print count, movie.title
    time.sleep(2)'''

'''count = 0
for mid in movie_ids:
    print count, mid
    response = urllib.urlopen('http://api.douban.com/v2/movie/subject/%s' % mid)
    data = response.read()
    add_movie(data)
    count += 1
    time.sleep(3)'''

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()