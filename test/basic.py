from grab import Grab
from captcha_solver import CaptchaService
from unittest import TestCase

HTML = """
<html>
<body>
<h1>Header 1</h1>
<ul id="ul-1">
    <li>Item 1</li>
    <li>Item 2</li>
"""


class BasicTestCase(TestCase):
    def test_lxml_fromstring(self):
        self.assertEqual('Header 1', 'Header 1')
