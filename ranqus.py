import random

from cStringIO import StringIO
from PIL import Image
from pymongo import MongoClient
from gridfs import GridFS
from flask import Flask, request, render_template, make_response, send_file

connection = MongoClient('mongodb://localhost')
database = connection.ranqus

fs = GridFS(database)

app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', error=error)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/<int:width>/<int:height>/')
def get_image(width, height):
    quantity = database.picture.find({}).count()
    if quantity == 0:
        return 'No data'
    random_value = random.randrange(0, quantity)
    photo = database.picture.find({})[random_value]
    object_id = photo['picture_id']
    _file = fs.get(object_id)

    im = StringIO()
    im.write(_file.read())
    im.seek(0)
    im = Image.open(im)
    size = (width, height)
    im = im.resize(size, Image.ANTIALIAS)
    im_io = StringIO()
    format_file = _file.name.split('.')[1]
    if format_file == 'jpg':
        format_file = 'jpeg'
    im.save(im_io, format_file, quality=50)
    im_io.seek(0)

    return send_file(im_io, mimetype='image/jpeg')

    # response = make_response(_file.read())
    # response.mimetype = _file.content_type
    # return response


@app.route('/admin/upload/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        photo = request.files['photo']
        _id = fs.put(photo, contentType=photo.content_type, filename='test.jpg')
        database.picture.insert({'picture_id': _id, 'size': 'big'})
        return 'complete: ' + str(_id)
    return render_template('admin/upload.html')


if __name__ == '__main__':
    app.run()
