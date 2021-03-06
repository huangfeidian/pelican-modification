#!/usr/bin/env python
# -*- encoding: UTF-8 -*-
# @author: wilbur.ma@foxmail.com
# @date: 2013-08-23
# @license: BSD 3-Clause License
# @brief: parse h1~h6 headings and generate
#         toc of a markdwon file

from html.parser import HTMLParser
from pelican import signals, readers, contents
# import os, sys, re, md5, markdown, logging
import logging, os, sys, re

from markdown.extensions import headerid

logger = logging.getLogger(__name__)

def gen_heading_id(heading_ids, slugify_func, heading_name):
    hID = slugify_func(heading_name, '-')
    i = 0
    while hID in heading_ids:
        # duplicate heading id
        i += 1
        logger.warn("found duplicate heading id `{0}'=>`{1}', will try {1}_{2} instead".format(heading_name, hID, i))
        hID = "{}_{}".format(hID, i)
    heading_ids.append(hID)
    return hID

class Heading:
    HeadRegex = re.compile("h[1-6]")
    def __init__(self, tag, value):
        self.tag = tag
        self.value = value

    def __repr__(self):
        return "{}:{}".format(self.tag, self.value)

    @classmethod
    def is_heading(cls, tag):
        return None != cls.HeadRegex.match(tag)

class HeadingParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.heading_ids = []
        self.headings = []
        self.tagOpen = False
        self.toc = u""

    def handle_starttag(self, tag, attrs):
        if Heading.is_heading(tag):
            self.headings.append(Heading(tag, ""))
            self.tagOpen = True

    def handle_endtag(self, tag):
        self.tagOpen = False

    def handle_data(self, data):
        if self.tagOpen and len(self.headings) > 0:
            self.headings[-1].value = data

    def generate_toc(self, slugify_func, list_style):
        prevHead = None
        openListSetNum = 0
        linkFormat = u"<a href='#{}'>{}</a>"
        for i in range(len(self.headings)):
            head = self.headings[i]
            head.parent = None
            if type(head.value) != str:
                head.value = str(head.value)
            headAnchor = u"{}".format(gen_heading_id(self.heading_ids, slugify_func, head.value))
            # first elem
            if 0 == i:
                self.toc += (u"<li>" + linkFormat).format(headAnchor, head.value)
                continue
            prevHead = self.headings[i-1]
            if head.tag > prevHead.tag:
                head.parent = prevHead
                openListSetNum += 1
                self.toc += (u"<{}><li>" + linkFormat).format(list_style, headAnchor, head.value)
            elif head.tag < prevHead.tag:
                currParent = prevHead.parent
                while currParent and (head.tag <= currParent.tag):
                    openListSetNum -= 1
                    self.toc += (u"</li></{}>".format(list_style))
                    currParent = currParent.parent
                head.parent = currParent
                self.toc += (u"</li><li>" + linkFormat).format(headAnchor, head.value)
            else:
                head.parent = prevHead.parent
                self.toc += (u"</li><li>" + linkFormat).format(headAnchor, head.value)
        while openListSetNum > 0:
            self.toc += (u"</li></{}>".format(list_style))
            openListSetNum -= 1
        if len(self.headings) > 1:
            self.toc += u"</li>"
        # print(self.toc)
        return self.toc


def extract_headings(content):
    if isinstance(content, contents.Static):
        return

    parser = HeadingParser()
    parser.feed(content._content)
    content.html_headings = parser.headings
    # print("parser.headings ",parser.headings)
    my_slugify = content.settings.get("MY_SLUGIFY_FUNC", headerid.slugify)
    list_style = content.settings.get("MY_TOC_LIST_TYPE", "ul")
    content.html_toc = parser.generate_toc(my_slugify, list_style)

def register():
    signals.content_object_init.connect(extract_headings)


if __name__ == "__main__":
    import hashlib
    def my_slugify(value, sep):
        m = hashlib.md5(value.encode('utf8'))
        # m = hashlib.md5(value)
        return m.hexdigest()[:6]

    parser = HeadingParser()
    htmlStr = "<html><head></head><body><h1>hello</h1>\
            <h2>hi, h2</h2><h2>hi, another h2</h2></body></html>"
    parser.feed(htmlStr)
    print(parser.headings)
    print(parser.generate_toc(my_slugify, "ol"))

