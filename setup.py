import os, sys
try:
    from setuptools import setup
    from setuptools.command.install import install as _install
    from setuptools.command.sdist import sdist as _sdist
except ImportError:
    from distutils.core import setup
    from distutils.command.install import install as _install
    from distutils.command.sdist import sdist as _sdist


def _run_build_tables(dir):
    from subprocess import call
    call([sys.executable, '_build_tables.py'],
         cwd=os.path.join(dir, 'py010parser'))


class install(_install):
    def run(self):
        _install.run(self)
        self.execute(_run_build_tables, (self.install_lib,),
                     msg="Build the lexing/parsing tables")


class sdist(_sdist):
    def make_release_tree(self, basedir, files):
        _sdist.make_release_tree(self, basedir, files)
        self.execute(_run_build_tables, (basedir,),
                     msg="Build the lexing/parsing tables")


setup(
    # metadata
    name             = 'py010parser',
    description      = '010 template parser in Python',
    long_description = """
		py010parser is a modified fork of the pycparser project. It is
		pure Python using the PLY parsing library. It parses 010 templates
		into an AST.
    """,
    license      = 'BSD',
    version      = '0.1.8',
    author       = 'James Johnson',
    maintainer   = 'James Johnson',
    author_email = 'd0c.s4vage@gmail.com',
    url          = 'https://github.com/d0c-s4vage/py010parser',
    platforms    = 'Cross Platform',
    classifiers  =  [
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',],
    packages         = ['py010parser', 'py010parser.ply'],
	download_url     = "https://github.com/d0c-s4vage/py010parser/tarball/v0.1.8",
	keywords         = ["010", "template", "parser"],
    package_data     = {'py010parser': ['*.cfg']},
    cmdclass         = {'install': install, 'sdist': sdist},
	install_requires = open(os.path.join(os.path.dirname(__file__), "requirements.txt")).read().split("\n"),
)
