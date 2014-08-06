#!/usr/bin/env python
# ----------------------------------------------------------------------------
# Author: Ravit Khurana <ravit.khurana@gmail.com>
# ----------------------------------------------------------------------------
# TODO: Alert user if title for gnome terminal/guake is set as dynamic
# this utility scrapes html information from the web based on the configuration
import urllib2
response = urllib2.urlopen('http://python.org/')
html = response.read()
print html