#!/usr/bin/env python
# encoding: utf-8

import glob
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

def run_tests():
	files = []
	for filename in glob.glob(os.path.join(os.path.dirname(__file__), "*.py")):
		basename = os.path.basename(filename)
		if basename.startswith("test_") and basename.endswith(".py"):
			files.append(basename.replace(".py", ""))

	suite = unittest.TestLoader().loadTestsFromNames(files)

	testresult = unittest.TextTestRunner(verbosity=1).run(suite)
	sys.exit(0 if testresult.wasSuccessful() else 1)

if __name__ == "__main__":
	run_tests()
