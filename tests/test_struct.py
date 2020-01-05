#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import unittest


sys.path.insert(0, "..")
from py010parser import parse_file, parse_string, c_ast
from py010parser.plyparser import ParseError


class TestStruct(unittest.TestCase):
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
        def inner_test():
            res = parse_string("""
                struct NAME (int a) {
                    int blah;
                } name;
            """, optimize=True, predefine_types=False)

        # this is invalid syntax! name should be name(X) with X being the "a"
        # parameter!
        self.assertRaises(ParseError, inner_test)

    def test_basic_struct_with_args2(self):
        res = parse_string("""
            typedef struct (int a) {
                int blah;
            } SPECIAL_STRUCT;
        """, optimize=True, predefine_types=False)

    def test_basic_struct_with_args3(self):
        res = parse_string("""
            typedef struct(int variable)
            {
                unsigned short a;
                unsigned short b;
            } RESOURCE_DIRECTORY_TABLE;

            struct RESOURCE_DIRECTORY_TABLE test(1);
        """, optimize=True, predefine_types=False)
        decl = res.children()[1][1]
        self.assertTrue(isinstance(decl.type, c_ast.StructCallTypeDecl))
        decl_args = decl.type.args.children()
        self.assertEqual(decl_args[0][1].value, "1")
        self.assertEqual(len(decl_args), 1)

    def test_basic_struct_call_png(self):
        res = parse_string("""
            typedef struct {
                byte btRed <format=hex>;
                byte btGreen <format=hex>;
                byte btBlue <format=hex>;
            } PNG_PALETTE_PIXEL;

            struct PNG_CHUNK_PLTE (int32 chunkLen) {
                PNG_PALETTE_PIXEL plteChunkData[chunkLen/3];
            };
        """, optimize=True, predefine_types=True)

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

    def test_basic_struct_with_args_calling_non_simple_params(self):
        res = parse_string("""
            struct PNG_CHUNK_BKGD (int32 colorType) {
            };

            int blah[4];
            typedef struct {
                PNG_CHUNK_BKGD bkgd(blah[1]);
            } PNG_CHUNK;
        """, optimize=True, predefine_types=True)
    
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

    def test_struct_bitfield_with_metadata(self):
        res = parse_string("""
            typedef struct tgCifDirEntry {
                    uint16 storage_method : 2;
                    uint16 data_type : 3;
                    uint16 id_code : 11 <format=hex>;
            } CifDirEntry <read=ReadCifDirEntry>;
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

    def test_implicit_struct_typedef(self):
        res = parse_string("""
            struct Blah { int a; } blah;

            Blah b;
        """, optimize=True)

    def test_two_part_struct_decl(self):
        res = parse_string("""
            struct StructTest;

            StructTest testing;
        """, optimize=True)


    # see #9 - https://github.com/d0c-s4vage/py010parser/issues/9 - _structs_with_params
    # was not being reset between separate calls to CParser.parse()
    def test_structs_with_params_resetting1(self):
        res = parse_string("""
            typedef struct (int a, int b) {
                char chars1[a];
                char chars2[b];
            } blah;

            blah test(2, 3);
        """, optimize=True)

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
        """, optimize=True)

    # see #31 - Failure parsing direct struct decls with parameters
    def test_typedefd_struct_with_parameters(self):
        """Test that direct struct declarations work with parameters.
        """
        res = parse_string("""
            struct TEST_STRUCT(int arraySize, int arraySize2)
            {
                uchar b[arraySize];
                uchar c[arraySize2];
            };
            local int bytes = 4;
            typedef struct TEST_STRUCT NEW_STRUCT;
            NEW_STRUCT l(bytes, 3);
        """, optimize=False)


if __name__ == "__main__":
        unittest.main()
