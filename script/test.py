#!/usr/bin/env python
# coding: utf-8
import unittest
import sys
from copy import copy
import os


TEST_LIST = (
    'test.solver',
)


def setup_arg_parser(parser):
    parser.add_argument('-t', '--test-only', help='Run only specified tests')


def main(test_only, **kwargs):
    if test_only:
        test_list = [test_only]
    else:
        test_list = TEST_LIST

    # Ensure that all test modules are imported correctly
    for path in test_list:
        __import__(path, None, None, ['foo'])

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for path in test_list:
        mod_suite = loader.loadTestsFromName(path)
        for some_suite in mod_suite:
            for test in some_suite:
                suite.addTest(test)

    runner = unittest.TextTestRunner()

    result = runner.run(suite)

    if result.wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)
