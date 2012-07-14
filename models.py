from google.appengine.ext import db


class Link(db.Model):
    url = db.LinkProperty()
    hash = db.StringProperty()
    created = db.DateTimeProperty(auto_now=False, auto_now_add=True)
    hits = db.IntegerProperty()

    def seed(self, url):
        if Link.is_valid_url(url):
            self.url = url
            self.hash = Link.generate_unique_hash()
            self.hits = 0
            self.put()
            return self
        else:
            raise ValueError('Invalid URL')

    @staticmethod
    def is_valid_url(url):
        import urllib
        try:
            u = urllib.urlopen(url)
            if u.code != 200:
                return False
            else:
                return True
        except:
            return False

    @staticmethod
    def generate_unique_hash():
        h = Link.generate_hash()
        l = Link.all().filter("hash =", h).get()
        if l:
            return Link.generate_unique_hash()
        else:
            return h

    @staticmethod
    def generate_hash(self):
        import string
        import random
        # 238,328 possible unique string now
        return  ''.join([random.choice(string.letters + string.digits)
                         for x in xrange(3)])
