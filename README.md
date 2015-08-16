[![master Build Status](https://travis-ci.org/d0c-s4vage/py010parser.svg?branch=master)](https://travis-ci.org/d0c-s4vage/py010parser) - master
[![develop Build Status](https://travis-ci.org/d0c-s4vage/py010parser.svg?branch=develop)](https://travis-ci.org/d0c-s4vage/py010parser) - develop

# py010parser

py010parser is a python library that can parse 010 templates.
It is a modified fork of [Eli Bendersky's pycparser](https://github.com/eliben/pycparser) project.

## introduction

Sweetscape's [010 editor](http://www.sweetscape.com/) is a binary-format
editor and parser. [Many](https://www.google.com/search?q=github+010+templates&oq=github+010+templates) [templates](http://www.sweetscape.com/010editor/templates/)
can be found online for most binary formats.

This project (py010parser) is an effort to make 010 scripts parseable
from python, with the intent to build additional tools using py010parser,
such as [pfp](http://github.com/d0c-s4vage/pfp), an 010 template
interpreter.
