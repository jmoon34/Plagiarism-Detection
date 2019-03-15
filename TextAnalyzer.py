import json
import math
import random
from Vector import Vector
from WebScraper import WebScraper
from googlesearch import search


# Class of object that retrieves a collection of document to be used for analysis
class TextAnalyzer:
    def __init__(self, query_file_name="Texts/GoogleQuery.txt"):
        self.query_file_name = query_file_name
        self.query_list = []
        self.query_str = ""
        # collection_dict structure: {text: url}
        self.collection_dict = {}

    def get_collection_from_google(self):
        """
        Generates the collection of texts from the URL's using the first 32 words
        :return:
        """
        query_32_list = self.query_list[:32]
        query_32 = " ".join(query_32_list)
        for url in search(query_32, tld='com', lang='en', num=5, stop=2, pause=2):
            print(url)
            web_scraper = WebScraper(url)
            self.collection_dict[web_scraper.extract_text()] = url
        print("collection_dict size:", len(self.collection_dict))

    def get_query_from_file(self):
        """
        Retrieves query as String from file
        :return:
        """
        with open(self.query_file_name, 'r') as f:
            self.query_str = f.read().lower()
        self.query_list = self.query_str.split(' ')
        print("query list: ", end="")
        print(self.query_list)

    def precompute_hashes(self, text, phrase_len, p, x):
        """
        Precomputes hashes of the text given length of phrase and a fixed hash function
        :param text: searched text
        :param phrase_len: length of phrase
        :param p: parameter of fixed hash function, large prime number
        :param x: parameter of fixed hash function
        :return: list of hash values as an array
        """
        t = len(text)
        hash_list = [None for _ in range(t - phrase_len + 1)]
        last_string = text[(t - phrase_len): t]
        hash_list[t - phrase_len] = self.hash_string(last_string, p, x)
        y = 1
        for i in range(phrase_len):
            y = (y * x) % p
        for i in range(t - phrase_len - 1, -1, -1):
            hash_list[i] = (x * hash_list[i + 1] + ord(text[i]) - y * ord(text[i + phrase_len])) % p
        return hash_list

    def rabin_karp(self, text, phrase):
        if len(phrase) > len(text):
            return []
        p = self.get_big_prime(len(phrase) + 1)
        x = random.randint(1, p - 1)
        result = []
        phrase_hash = self.hash_string(phrase, p, x)
        hash_list = self.precompute_hashes(text, len(phrase), p, x)
        for i in range(len(text) - len(phrase) + 1):
            if phrase_hash != hash_list[i]:
                continue
            if text[i:i + len(phrase)] == phrase:
                result.append(i)
        return result

    def run_rabin_karp(self):
        i = 0
        for text in self.collection_dict:
            with open("Texts/collection" + str(i) + ".txt", 'w') as f:
                f.write(text)
                f.write("\n\n")
            match_index = self.rabin_karp(text, self.query_str)
            if match_index:
                print("Matching text found in url:", self.collection_dict[text])
                print("At position:", match_index)
            i += 1




    def get_scores_and_url(self):
        scores = {}
        query_vector = self.calculate_query_vector()
        for document in self.collection_dict:
            doc_vector = self.calculate_doc_vector(document)
            document_score = query_vector.dot_product(doc_vector)
            url = self.collection_dict[document]
            scores[document_score] = url
        sorted_scores = sorted(scores, reverse=True)
        sorted_urls = [scores[doc_score] for doc_score in sorted_scores]
        return list(zip(sorted_scores, sorted_urls))

    def calculate_doc_vector(self, document):
        """
        Calculates and returns a document vector
        :param document: single document
        :param query: list of queries
        :return:
        """
        return Vector([self.calculate_tf(term, document) for term in self.query_list]).normalize()

    def calculate_query_vector(self):
        """
        Calculates and returns a query vector
        :param query: string
        :return:
        """
        return Vector([self.calculate_tf_idf(term, self.query_str) for term in self.query_list]).normalize()

    def calculate_tf_idf(self, term, document):
        return self.calculate_tf(term, document)*self.calculate_idf(term)

    def calculate_idf(self, term):
        """
        Calculates "informativeness", which is inversely proportional to document frequency,
        or how often a term appears in the entire collection
        :param term:
        :return:
        """
        df = 1
        for text in self.collection_dict:
            if term in text:
                df += 1
        return math.log10(len(self.collection_dict) / df)

    @staticmethod
    def calculate_tf(term, document):
        """
        Calculates term frequency, or how often a term is found in a document
        :param term:
        :param document:
        :return:
        """
        if term not in document:
            return 0
        else:
            tf = document.count(term)
            return 1 + math.log10(tf)

    @staticmethod
    def is_prime(n):
        if n <= 0:
            raise ValueError("n <= 0")
        if n == 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

    @staticmethod
    def get_big_prime(max_length):
        """
        Returns prime such that probability of collision for hash value is <= 1/10**6
        :param max_length:
        :return:
        """
        p = max_length * 10 ** 6
        while not TextAnalyzer.is_prime(p):
            p += 1
        return p

    @staticmethod
    def hash_string(s, p, x):
        h = 0
        for i in range(len(s) - 1, -1, -1):
            h = (h * x + ord(s[i])) % p
        return h