# coding: utf-8
import unittest

from python_rest_handler.plugins.bootstrap import *


class BootstrapWidgetsTests(unittest.TestCase):
    def test_input_text(self):
        html = bs_input_text('field')
        self.assertTrue('id="field"' in html)

    def test_input_password(self):
        html = bs_input_password('password')
        self.assertTrue('id="password"' in html)

    def test_input_file(self):
        html = bs_input_file('upload', value='x')
        self.assertTrue('id="upload"' in html)
        self.assertTrue('value=""' in html)

    def test_input_select(self):
        options = [{'label':'Option 1', 'value':'value1'}, {'label':'Option 2', 'value':'value2'}]
        html = bs_select_field('choices', options, selected_value='value2')
        self.assertTrue('id="choices"' in html)

    def test_button(self):
        html = bs_button(label='Add')
        self.assertTrue('id="btn-save"' in html)
