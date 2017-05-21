#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Huiliang Huang'
SITENAME = u'spirits away'
SITEURL = 'spiritsaway.info'
JINJA_ENVIRONMENT = {"extensions": ['jinja2.ext.ExprStmtExtension',"jinja2.ext.do"]}

PATH = 'content'
STATIC_PATHS  = ["image", "pdf", ]
TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = u'Chinese (Simplified)'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
USE_FOLDER_AS_CATEGORY = True
# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

MY_TOC_UPDATE_CONTENT = True
THEME = "E:/Github/niu-x2-sidebar"
PLUGIN_PATHS = ["E:/Github/pelican-plugins",]
PLUGINS = ["render_math", "extract_headings", "extract_toc"]
import hashlib
def my_slugify(value, sep):
    m = hashlib.md5(value.encode('utf8'))
    # m = hashlib.md5(value)
    result = m.hexdigest()[:6]
    # print(result)
    return result
MY_SLUGIFY_FUNC = my_slugify
MY_TOC_LIST_TYPE = 'ol'
from markdown.extensions.headerid import HeaderIdExtension
MARKDOWN = {"extensions":["extra", "codehilite", HeaderIdExtension(configs=[('slugify', my_slugify)])]}
# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

# NIUX2_PYGMENTS_THEME = 'monokai'
NIUX2_HEADER_SECTIONS = [ 
     ("关于", "about", "/pages/about.html", "icon-anchor"),
     ("存档", "archives", "/archives.html", "icon-archive"),
     ("标签", "tags", "/tags.html", "icon-tag"),
]