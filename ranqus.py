from pymongo import MongoClient
from flask import Flask, request, render_template

from models import Picture

connection = MongoClient('mongodb://localhost')
database = connection.ranqus

app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', error=error)


@app.route('/')
def hello_world():
    picture = Picture(database)
    return 'Hello World!' + picture.show()


@app.route('/<int:width>/<int:height>/')
def get_image(width, height):
    return 'width: %d height: %d' % (width, height)


@app.route('/admin/upload/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        print 'post'
    return render_template('admin/upload.html')


if __name__ == '__main__':
    app.run()
