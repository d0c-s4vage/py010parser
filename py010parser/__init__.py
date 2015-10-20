#-----------------------------------------------------------------
# pycparser: __init__.py
#
# This package file exports some convenience functions for
# interacting with pycparser
#
# Copyright (C) 2008-2012, Eli Bendersky
# License: BSD
#-----------------------------------------------------------------
__all__ = ['c_lexer', 'c_parser', 'c_ast']
__version__ = '0.1.6'

from .c_parser import CParser

from ply import cpp
import ply.lex as lex


def parse_file(filename, use_cpp=True, cpp_path='cpp', cpp_args='',
               parser=None, predefine_types=True, keep_scopes=False):
    """ Parse a C file using pycparser.

        filename:
            Name of the file you want to parse.

        use_cpp:
            Set to True if you want to execute the C pre-processor
            on the file prior to parsing it.

        cpp_path:
            If use_cpp is True, this is the path to 'cpp' on your
            system. If no path is provided, it attempts to just
            execute 'cpp', so it must be in your PATH.

        cpp_args:
            If use_cpp is True, set this to the command line arguments strings
            to cpp. Be careful with quotes - it's best to pass a raw string
            (r'') here. For example:
            r'-I../utils/fake_libc_include'
            If several arguments are required, pass a list of strings.

        parser:
            Optional parser object to be used instead of the default CParser

        keep_scopes:
            If the parser should retain its scope stack for type names from previous
            parsings.

        When successful, an AST is returned. ParseError can be
        thrown if the file doesn't parse successfully.

        Errors from cpp will be printed out.
    """
    if use_cpp:
        text = preprocess_file(filename, cpp_path, cpp_args)
    else:
        with open(filename, 'rU') as f:
            text = f.read()

    if parser is None:
        parser = CParser()
    return parser.parse(text, filename, predefine_types=predefine_types, keep_scopes=keep_scopes)

def parse_string(text, parser=None, filename="<string>", optimize=True, predefine_types=True,
        use_cpp=True, cpp_path='cpp', cpp_args='', keep_scopes=False):
    
    if use_cpp:
        lexer = lex.lex(object=cpp)

        preprocessor = ply.cpp.Preprocessor(lexer)
        preprocessor.parse(text, filename)

        text = ""

        while True:
            tok = preprocessor.token()
            if not tok: break
            if tok.type != "CPP_COMMENT":
                text += tok.value

    if parser is None:
        parser = CParser(
            lex_optimize=optimize,
            yacc_optimize=optimize
        )
    return parser.parse(text, filename, predefine_types=predefine_types, keep_scopes=keep_scopes)
