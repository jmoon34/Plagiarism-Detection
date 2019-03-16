import math


class Vector:
    def __init__(self, components):
        self.dim = len(components)
        self.components = components

    def dot_product(self, vector):
        if self.dim != vector.dim:
            raise ValueError("Dimension mismatch")
        product = 0
        for i, component in enumerate(self.components):
            product += component*vector.components[i]
        return product

    def norm(self):
        """
        Calculates the L2 norm of the vector
        :return:
        """
        sum_of_squares = 0
        for components in self.components:
            sum_of_squares += components ** 2

        return math.sqrt(sum_of_squares)

    def normalize(self):
        if self.norm() != 0:
            self.components = [elements / self.norm() for elements in self.components]
        return self

    def calculate_cosine_similarity(self, vector):
        return self.dot_product(vector)/(self.norm()*vector.norm())

    def __str__(self):
        return str(self.components)
