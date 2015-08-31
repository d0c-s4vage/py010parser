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
    
    def test_basic_struct(self):
        res = parse_string("""
            struct NAME {
                int blah;
            } name;
        """, optimize=True, predefine_types=False)

    def test_basic_struct_typedef(self):
        res = parse_string("""
            typedef union {
                int some_int;
                struct {
                    char a;
                    char b;
                    char c;
                    char d;
                } some_chars;
            } blah;

            blah some_union;
        """, optimize=True, predefine_types=False)

    def test_basic_struct_with_args(self):
        res = parse_string("""
            struct NAME (int a) {
                int blah;
            } name;
        """, optimize=True, predefine_types=False)

    def test_basic_struct_with_args2(self):
        res = parse_string("""
            typedef struct (int a) {
                int blah;
            } SPECIAL_STRUCT;
        """, optimize=True, predefine_types=False)

    def test_basic_struct_with_args_calling(self):
        res = parse_string("""
            typedef struct (int a) {
                int blah;
            } SPECIAL_STRUCT;

            SPECIAL_STRUCT test(10);

            int blah() {
                return 10;
            }
        """, optimize=True, predefine_types=False)
        decl = res.children()[1][1]
        self.assertTrue(isinstance(decl.type, c_ast.StructCallTypeDecl))
        decl_args = decl.type.args.children()
        self.assertEqual(decl_args[0][1].value, "10")
        self.assertEqual(len(decl_args), 1)
    
    def test_struct_with_args_calling_not_func_decl(self):
        res = parse_string("""
            typedef struct(int a) {
                char chars[a];
            } test_structure;

            local int size = 4;
            test_structure test(size); // this SHOULD NOT be a function declaration
        """, predefine_types=False)
        decl = res.children()[2][1]
        self.assertEqual(decl.type.__class__, c_ast.StructCallTypeDecl)
        self.assertEqual(decl.type.args.__class__, c_ast.ExprList)
    
    def test_struct_with_args_calling_not_func_decl2(self):
        res = parse_string("""
            typedef struct(int a) {
                char chars[a];
            } test_structure;

            local int size = 4;
            test_structure test(size); // this SHOULD NOT be a function declaration
        """, predefine_types=False)
        decl = res.children()[2][1]
        self.assertEqual(decl.type.__class__, c_ast.StructCallTypeDecl)
        self.assertEqual(decl.type.args.__class__, c_ast.ExprList)
    
    def test_struct_with_args_calling_not_func_decl3(self):
        res = parse_string("""
            typedef struct(int a, int b) {
                char chars1[a];
                char chars2[b];
            } test_structure;

            local int size = 4;
            test_structure test(size, 5); // this SHOULD NOT be a function declaration
        """, predefine_types=False)
        decl = res.children()[2][1]
        self.assertEqual(decl.type.__class__, c_ast.StructCallTypeDecl)
        self.assertEqual(decl.type.args.__class__, c_ast.ExprList)
    
    def test_struct_with_args_calling_not_func_decl4(self):
        res = parse_string("""
            int sum(int a, int b) {
                return a + b;
            }

            typedef struct(int a) {
                char chars1[a];
            } test_structure;

            local int size = 4;
            test_structure test(sum(size, 3)); // this SHOULD NOT be a function declaration
        """, predefine_types=False)
        decl = res.children()[3][1]
        self.assertEqual(decl.type.__class__, c_ast.StructCallTypeDecl)
        self.assertEqual(decl.type.args.__class__, c_ast.ExprList)
    
    def test_struct_with_args_calling_not_func_decl5(self):
        res = parse_string("""
            // variable-width integer used by encoded_value types
            typedef struct (int size, int type) {
                local int s = size + 1;
                local int t = type;
                local int i;
                
                for(i=0; i<s; i++) {
                    ubyte val <comment="Encoded value element">;
                }
            } EncodedValue <read=EncodedValueRead, optimize=false>;

            string EncodedValueRead(EncodedValue &v) {
                local string s = "";

                return s;
            }
        """, predefine_types=True)
    
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
            """, optimize=True)

    def test_declaration_in_struct(self):
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
            """, optimize=True)
    
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

    def test_struct_bitfield_with_metadata(self):
        res = parse_string("""
            typedef struct tgCifDirEntry {
                    uint16 storage_method : 2;
                    uint16 data_type : 3;
                    uint16 id_code : 11 <format=hex>;
            } CifDirEntry <read=ReadCifDirEntry>;
        """, optimize=True)

    def test_untypedefd_enum_as_typeid(self):
        res = parse_string("""
            enum <ulong> BLAH {
                BLAH1, BLAH2, BLAH3
            };
            local BLAH x;
        """, optimize=True)

    def test_initializer_in_struct(self):
        res = parse_string("""
            local int b = 11;
            typedef struct BLAH {
                local int a = 10;
                int a:10;
            } blah;
        """, optimize=True)

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

    def test_implicit_struct_typedef(self):
        res = parse_string("""
            struct Blah { int a; } blah;

            Blah b;
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
    
    def test_metadata_with_string_value(self):
        res = parse_string("""
            int a <comment="this is a comment", key=val>;
            int a <comment="this is a comment">;
        """, optimize=True)

    def test_large_template(self):
        res = parse_file(template_path("JPGTemplate.bt"))
    
    def test_png_template(self):
        res = parse_file(template_path("PNGTemplate.bt"))
    
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
    
    def test_two_part_struct_decl(self):
        res = parse_string("""
            struct StructTest;

            StructTest testing;
        """, optimize=True)

if __name__ == "__main__":
        unittest.main()
