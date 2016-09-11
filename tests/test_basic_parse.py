#!/usr/bin/env python

import os
import sys
import unittest

sys.path.insert(0, "..")
from py010parser import parse_file, parse_string, c_ast

def template_path(template_name):
    return os.path.join(os.path.dirname(__file__), "templates", template_name)

class TestBasicParse(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_sizeof_unary(self):
        res = parse_string("""
            sizeof(this);
        """)
    
    def test_exists_unary(self):
        res = parse_string("""
            exists(this);
        """)
    
    def test_parentof_unary(self):
        res = parse_string("""
            parentof(this);
        """)
    
    def test_function_exists_unary(self):
        res = parse_string("""
            function_exists(this);
        """)
    
    def test_startof_unary(self):
        res = parse_string("""
            startof(this);
        """)
    
    def test_bitfield_in_if(self):
        res = parse_string("""
            struct {
                if(1) {
                    int field1:16;
                    //int field1;
                }
            } blah;
        """, optimize=True, predefine_types=False)

        bitfield_decl = res.children()[0][1].type.type.children()[0][1].iftrue.children()[0][1]
        self.assertNotEqual(type(bitfield_decl), dict)

    def test_bitfield_outside_of_struct(self):
        res = parse_string("""
            uint blah1:4;
            uint blah2:8;
            uint blah3:4;
        """, optimize=True, predefine_types=True)

    def test_basic(self):
        res = parse_string("""
            struct NAME {
                    int        stringLength;
                    char    name[stringLength];
            } name;
        """, optimize=True)

    def test_declaration_in_switch(self):
        res = parse_string("""
            int c;
            switch(c) {
                case 1:
                    c++;
                case 2:
                    int c;
            }
        """, optimize=True)

    def test_declaration_in_if(self):
        res = parse_string("""
            if(1) {
                int c;
            } else {
                int b;
            }
        """, optimize=True)

    # http://www.sweetscape.com/010editor/manual/TemplateVariables.htm
    def test_local_keyword(self):
        res = parse_string("""
            local int a;
            local int b;
        """, optimize=True)

    def test_metadata(self):
        res = parse_string("""
            local int a <hidden=true>;
        """, optimize=True)

    def test_typedef(self):
        res = parse_string("""
            typedef unsigned int UINT2;
            UINT2 blah;
        """, optimize=True)

    def test_value_types(self):
        res = parse_string("""
            time_t var1;
            OLETIME var2;
            FILETIME var3;
            DOSTIME var4;
            DOSDATE var5;
            HFLOAT var6;
            hfloat var7;
            DOUBLE var8;
            double var9;
            FLOAT var10;
            float var11;
            __uint64 var12;
            QWORD var13;
            UINT64 var14;
            UQUAD var15;
            uquad var16;
            uint64 var17;
            __int64 var18;
            INT64 var19;
            QUAD var20;
            quad var21;
            int64 var22;
            DWORD var23;
            ULONG var24;
            UINT32 var25;
            UINT var26;
            ulong var27;
            uint32 var28;
            uint var29;
            LONG var30;
            INT32 var31;
            INT var32;
            long var33;
            int32 var34;
            int var35;
            WORD var36;
            UINT16 var37;
            USHORT var38;
            uint16 var39;
            ushort var40;
            INT16 var41;
            SHORT var42;
            int16 var43;
            short var44;
            UBYTE var45;
            UCHAR var46;
            ubyte var47;
            uchar var48;
            BYTE var49;
            CHAR var50;
            byte var51;
            char var52;

            string var53;
            wstring var54;
            wchar_t var55;
        """, optimize=True)

    def test_block_item_at_root(self):
        # had to get rid of the default int ret val on functions
        # from pycparser

        res = parse_string("""
        int a = 10;
        void some_function(int num) {
            some_function();
        }
        a++;
        some_function();
        """, optimize=True)
   
    def test_pass_by_reference(self):
        res = parse_string("""
        void some_function(int &num, int &num2) {
        }

        void some_function(int &num2) {
        }
        """, optimize=True)
    
    def test_single_decl_in_for_loop(self):
        res = parse_string("""
            for(j = 0; j < 10; j++)
                ushort blah;
        """, optimize=True)

    def test_single_decl_in_while_loop(self):
        res = parse_string("""
            while(1)
                ushort blah;
        """, optimize=True)

    def test_single_decl_in_do_while_loop(self):
        res = parse_string("""
            while(1)
                ushort blah;
        """, optimize=True)

    def test_single_decl_in_do_while_loop(self):
        res = parse_string("""
            do
                ushort blah;
            while(1);
        """, optimize=True)

    def test_single_decl_in_if(self):
        res = parse_string("""
            if(1)
                ushort blah;
        """, optimize=True)

    def test_single_decl_in_if_else(self):
        res = parse_string("""
            if(1)
                ushort blah;
            else
                ushort blah;

            if(1) {
                ushort blah;
            } else
                ushort blah;

            if(1)
                ushort blah;
            else {
                ushort blah;
            }

            if(1) {
                ushort blah;
            } else {
                ushort blah;
            }
        """, optimize=True)

    # I think we'll make a break from 010 syntax here...
    # it's too ridiculous to me to allow types that have
    # not yet been defined
    def test_runtime_declared_type(self):
        res = parse_string("""
            void ReadAscString1(StrAscii1 &s) {
                ;
            }
        """, optimize=True, predefine_types=False)

    def test_comment_single_line(self):
        res = parse_string("""
            // this is a comment
            int blah;
        """, optimize=True, predefine_types=False)

        self.assertEqual(len(res.children()), 1, "should only have one node in the AST")

        node = res.children()[0][1]
        self.assertEqual(node.name, "blah")
        self.assertEqual(node.type.declname, "blah")
        self.assertEqual(node.type.type.names, ["int"])

    def test_comment_multi_line(self):
        res = parse_string("""
            /*
            this is a comment
            */
            int blah;
        """, optimize=True, predefine_types=False)

        self.assertEqual(len(res.children()), 1, "should only have one node in the AST")

        node = res.children()[0][1]
        self.assertEqual(node.name, "blah")
        self.assertEqual(node.type.declname, "blah")
        self.assertEqual(node.type.type.names, ["int"])
    
    def test_metadata_with_string_value(self):
        res = parse_string("""
            int a <comment="this is a comment", key=val>;
            int a <comment="this is a comment">;
        """, optimize=True)

    def test_large_template(self):
        res = parse_file(template_path("JPGTemplate.bt"))
    
    def test_png_template(self):
        res = parse_file(template_path("PNGTemplate.bt"))

    def test_exe_template(self):
        res = parse_file(template_path("EXETemplate.bt"))
    
    def test_preprocessor_with_string(self):
        res = parse_string("""
            //this shouldn't cause any problems
            int a;
        """, optimize=True)
    
    def test_metadata_with_space1(self):
        res = parse_string("""
            int a < key1 = value1 >;
        """, optimize=True)
    
    def test_metadata_with_space2(self):
        res = parse_string("""
            int a < key1 = value1 , key2 = value2 >;
        """, optimize=True)
    

if __name__ == "__main__":
        unittest.main()
