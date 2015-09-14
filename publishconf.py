#!/usr/bin/env python
# -*- coding: utf-8 -*- #
"""Docstring."""
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *  # noqa

SITEURL = 'http://kalmanolah.net'
FEED_DOMAIN = SITEURL

DELETE_OUTPUT_DIRECTORY = True
