import math
from unittest import TestCase

from PD.TextAnalyzer import TextAnalyzer


class TestText(TestCase):
    def test_calculate_tf(self):
        self.assertEqual(TextAnalyzer.calculate_tf("term", "doc"), 0)
        self.assertEqual(TextAnalyzer.calculate_tf("term", "term"), 1)
        self.assertEqual(TextAnalyzer.calculate_tf("term", "termterm"), 1 + math.log10(2))
        self.assertEqual(TextAnalyzer.calculate_tf("term", "term" * 10), 2)
        self.assertEqual(TextAnalyzer.calculate_tf("term", "term" * 1000), 4)

