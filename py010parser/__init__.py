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
__version__ = '0.1.10'

from .c_parser import CParser

from py010parser.ply import cpp
import py010parser.ply.lex as lex


def preprocess_file(text, filename):
    """Preprocess the file to remove comments
    """
    lexer = lex.lex(object=cpp)

    preprocessor = ply.cpp.Preprocessor(lexer)
    preprocessor.parse(text, filename)

    text = ""

    while True:
        tok = preprocessor.token()
        if not tok: break
        if tok.type != "CPP_COMMENT":
            text += tok.value

    return text

def parse_file(filename, parser=None, predefine_types=True, keep_scopes=False):
    """ Parse an 010 template file using py010parser

        filename:
            Name of the file you want to parse.

        parser:
            Optional parser object to be used instead of the default CParser

        keep_scopes:
            If the parser should retain its scope stack for type names from previous
            parsings.

        When successful, an AST is returned. ParseError can be
        thrown if the file doesn't parse successfully.

        Errors from cpp will be printed out.
    """
    with open(filename, 'rU') as f:
        text = f.read()
    text = preprocess_file(text, filename)

    if parser is None:
        parser = CParser()

    return parser.parse(
        text,
        filename,
        predefine_types = predefine_types,
        keep_scopes     = keep_scopes
    )


def parse_string(
        text,
        parser          = None,
        filename        = "<string>",
        optimize        = True,
        predefine_types = True,
        keep_scopes     = False
    ):
    text = preprocess_file(text, filename)

    if parser is None:
        parser = CParser(
            lex_optimize=optimize,
            yacc_optimize=optimize
        )

    return parser.parse(
        text,
        filename,
        predefine_types = predefine_types,
        keep_scopes     = keep_scopes
    )
