#!/usr/bin/env python

import os
import webapp2
import jinja2
import re

from models import Link

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


class BaseHandler(webapp2.RequestHandler):
    def render(self, template, **kw):
        self.response.out.write(self.render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)


class LinkShortener(BaseHandler):
    def get(self):
        self.render("url_form.html")

    def post(self):
        url = self.request.get('url')
        if url:
            URL_RE = re.compile(r"(https|http)")
            if not URL_RE.match(url):
                url = 'http://%s' % url
            try:
                l = Link()
                l.seed(url)
                h = l.hash
                params = {'hash': h, 'link': str(l.url)}
                self.render("url_form.html", **params)
            except ValueError:
                params = {'error': True}
                self.render("url_form.html", **params)
        else:
            params = {'error': True}
            self.render("url_form.html", **params)


class LinkRedirect(BaseHandler):

    def get(self, hash):
        l = Link.all().filter("hash =", hash).get()
        if l:
            l.hits += 1
            l.put()
            self.redirect('%s' % str(l.url))
        else:
            self.redirect('/short')
