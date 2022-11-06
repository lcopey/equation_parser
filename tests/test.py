import json
from unittest import TestCase

from equation_parser import Node, from_string


class ParserTest(TestCase):
    def setUp(self) -> None:
        with open('./test.json', mode='r') as f:
            self.datas = json.load(f)

    def test_from_string(self):
        for value in self.datas:
            from_string(value['input'])

    def test_from_dict(self):
        for value in self.datas:
            Node.from_dict(value['output'])

    def test_both(self):
        for value in self.datas:
            assert from_string(value['input']) == Node.from_dict(value['output'])
