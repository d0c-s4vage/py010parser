#!/usr/bin/env python

import os
import sys
import unittest

sys.path.insert(0, "..")
from pycparser import parse_file, parse_string, c_ast

def template_path(template_name):
    return os.path.join("templates", template_name)

class TestBasicParse(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_basic(self):
        return
        res = parse_string("""
            struct NAME {
                    int		stringLength;
                    char	name[stringLength];
            } name;
        """, optimize=False)

    def test_if_in_struct(self):
        res = parse_string("""
            struct BLAH {
                int a:1;
                int b:2;
                int c:29;

                if(hello) {
                    b = 10;
                }
            } blah;
            """, optimize=False)
    
    def test_nested_structs(self):
        res = parse_string("""
            struct FILE {
                    struct HEADER {
                        char    type[4];
                        int     version;
                        int     numRecords;
                    } header;

                    struct RECORD {
                        int     employeeId;
                        char    name[40];
                        float   salary;
                    } record[ header.numRecords ];

                } file;
        """, optimize=False)
    
    # http://www.sweetscape.com/010editor/manual/TemplateVariables.htm
    def test_local_keyword(self):
        res = parse_string("""
            local int a;
            local int b;
        """, optimize=False)

if __name__ == "__main__":
        unittest.main()
