#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import unittest


sys.path.insert(0, "..")
from py010parser import parse_file, parse_string, c_ast


class TestEnum(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_enum_types(self):
        # note that there have been problems using a built-in
        # type (int/float/etc) vs the typedefd ones, TYPEID vs 
        res = parse_string("""
        enum <ulong> COLORS {
            WHITE = 1
        } var1;

        enum <int> COLORS {
            WHITE = 1
        } var1;

        enum IFD_dirtype {
            IFD_TYPE_EXIF = 1,
            IFD_TYPE_GEOTAG,
            IFD_TYPE_CASIO_QV_R62,
        };

        enum {
            TEST,
            TEST2
        } blah;
        """, optimize=True)

    def test_untypedefd_enum_as_typeid(self):
        res = parse_string("""
            enum <ulong> BLAH {
                BLAH1, BLAH2, BLAH3
            };
            local BLAH x;
        """, optimize=True)

    def test_c_keywords_in_enum(self):
        res = parse_string("""
            enum <int> BLAH {
                goto,
                register,
                extern,
                goto,
                volatile,
                static
            };
            local BLAH x;
        """, optimize=True)

    def test_untypedefd_enum_as_typeid(self):
        res = parse_string("""
            enum <ulong> BLAH {
                BLAH1, BLAH2, BLAH3
            };
            local BLAH x;
        """, optimize=True)

    def test_enum_types(self):
        # note that there have been problems using a built-in
        # type (int/float/etc) vs the typedefd ones, TYPEID vs 
        res = parse_string("""
        enum <ulong> COLORS {
            WHITE = 1
        } var1;

        enum <int> COLORS {
            WHITE = 1
        } var1;

        enum IFD_dirtype {
            IFD_TYPE_EXIF = 1,
            IFD_TYPE_GEOTAG,
            IFD_TYPE_CASIO_QV_R62,
        };

        enum {
            TEST,
            TEST2
        } blah;
        """, optimize=True)


        

if __name__ == "__main__":
        unittest.main()
