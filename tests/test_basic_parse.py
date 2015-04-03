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

    def test_declaration_in_struct(self):
        res = parse_string("""
            int c;
            switch(c) {
                case 1:
                    c++;
                case 2:
                    int c;
            }
        """, optimize=False)

    def test_declaration_in_if(self):
        res = parse_string("""
            if(1) {
                int c;
            } else {
                int b;
            }
        """, optimize=False)

    def test_switch_in_struct(self):
        res = parse_string("""
            struct BLAH {
                int c;

                switch(c) {
                    case 1:
                        int aa;
                    case 2:
                        int bb;
                    default:
                        int cc;
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

    def test_metadata(self):
        res = parse_string("""
            local int a <hidden=true>;
        """, optimize=False)

    def test_typedef(self):
        res = parse_string("""
            typedef unsigned int UINT2;
            UINT2 blah;
        """, optimize=False)

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
        """, optimize=False)

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
        """, optimize=False)
   
    def test_pass_by_reference(self):
        res = parse_string("""
        void some_function(int &num) {
        }
        """, optimize=False)
    
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
        """, optimize=False)

    def test_struct_bitfield_with_metadata(self):
        res = parse_string("""
            typedef struct tgCifDirEntry {
                    uint16 storage_method : 2;
                    uint16 data_type : 3;
                    uint16 id_code : 11 <format=hex>;
            } CifDirEntry <read=ReadCifDirEntry>;
        """, optimize=False)

    def test_untypedefd_enum_as_typeid(self):
        res = parse_string("""
            enum <ulong> BLAH {
                BLAH1, BLAH2, BLAH3
            };
            local BLAH x;
        """, optimize=False)

    def test_initializer_in_struct(self):
        res = parse_string("""
            local int b = 11;
            typedef struct BLAH {
                local int a = 10;
                int a:10;
            } blah;
        """, optimize=False)

    def test_nested_bitfield_in_struct(self):
        res = parse_string("""
            typedef struct BLAH {
                int a;
                switch(a) {
                    case 10:
                        int b:10;
                    default:
                        int c:10;
                }
            } blah;
        """, optimize=False)

    def test_large_template(self):
        res = parse_file(template_path("JPGTemplate.bt"))

if __name__ == "__main__":
        unittest.main()
