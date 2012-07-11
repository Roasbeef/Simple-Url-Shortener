#!/usr/bin/env python


import webapp2
from views import LinkShortener, LinkRedirect


app = webapp2.WSGIApplication([('/u/?', LinkShortener),
                               ('/(\w{4})', LinkRedirect)], debug=True)
