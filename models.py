from google.appengine.ext import db
import os
import urllib


class Link(db.Model):
    url = db.LinkProperty()
    hash = db.StringProperty()
    created = db.DateTimeProperty(auto_now=False, auto_now_add=True)
    hits = db.IntegerProperty()

    def seed(self, url):
        if self.is_valid_url(url):
            self.url = url
            self.hash = self.generate_unique_hash()
            self.hits = 0
            self.put()
            return self
        else:
            raise ValueError('Invalid URL')

    def is_valid_url(self, url):
        try:
            u = urllib.urlopen(url)
            if u.code != 200:
                return False
            else:
                return True
        except:
            return False

    def generate_unique_hash(self):
        h = self.generate_hash()
        l = Link.all().filter("hash =", h).get()
        if l:
            #WARNING could caused infinite loop when no more unique hashes are left
            #Fix when not feeling lazy
            return self.generate_unique_hash()
        else:
            return h

    def generate_hash(self):
        #returns random 16-bit string
        return os.urandom(2).encode('hex')
