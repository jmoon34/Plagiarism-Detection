from unittest import TestCase
from Vector import Vector
import math


class TestVector(TestCase):
    def test_dot_product(self):
        """
        Tests calculation of dot products between two vectors
        :return:
        """
        v1 = Vector([1, 2, 3, 4])
        v2 = Vector([3, 3, 2, 1])
        self.assertEqual(v1.dot_product(v2), 19)

        # Checks for error raised when dimensions don't match
        v3 = Vector([1])
        self.assertRaises(ValueError, v1.dot_product, v3)

    def test_norm(self):
        v = Vector([1,2,3,4])
        self.assertEqual(v.norm(), math.sqrt(30))

    def test_normalize(self):
        v = Vector([1,2,3])
        norm = v.norm()
        v.normalize()
        self.assertEqual(v.components, [1/norm, 2/norm, 3/norm])

    def test_calculate_cosine_similarity(self):
        v1 = Vector([1,2,3,4])
        v2 = Vector([4,3,2,1])
        self.assertEqual(v1.calculate_cosine_similarity(v2), v1.dot_product(v2)/(v1.norm()*v2.norm()))
        v1 = Vector([1,0,0])
        v2 = Vector([1,0,0])
        self.assertEqual(v1.calculate_cosine_similarity(v2), 1) # cos(0) = 1
        v1 = Vector([1,0,0])
        v2 = Vector([0,1,0])
        self.assertEqual(v1.calculate_cosine_similarity(v2), 0) # cos(90) = 0

    def test_str(self):
        v = Vector([1,2,3,4])
        self.assertEqual(v.__str__(), '[1, 2, 3, 4]')