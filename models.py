from PIL import Image


class Picture(object):

    def __init__(self, database):
        self.db = database
        self.objects = self.db.picture

    def crop_image(self):
        pass

    def show(self):
        txt = ''
        for picture in self.objects.find({}):
            txt += str(picture)
        return txt
