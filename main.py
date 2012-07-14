#!/usr/bin/env python


import webapp2
from views import LinkShortener, LinkRedirect


app = webapp2.WSGIApplication([('/short/?', LinkShortener),
                               ('/(\w{3})', LinkRedirect)], debug=True)
