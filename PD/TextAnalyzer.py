import math
import random
from googlesearch import search
from PD.Vector import Vector
from PD.WebScraper import WebScraper


# Class of object that retrieves a collection of document to be used for analysis
class TextAnalyzer:
    def __init__(self, query_file_name="../Texts/GoogleQuery.txt"):
        self.query_file_name = query_file_name
        self.query_list = []
        self.query_str = ""
        # collection_dict structure: {text: url}
        self.collection_dict = {}

    def get_collection_from_google(self, num_collection=5):
        """
        Generates the collection of texts from the URL's using the first 32 words
        :return:
        """
        query_32_list = self.query_list[:32]
        query_32 = " ".join(query_32_list)
        collection_index = 1
        for url in search(query_32, tld='com', lang='en', num=20, stop=2, pause=2):
            print(url)
            web_scraper = WebScraper(url)
            text = web_scraper.extract_text()
            if text != "":
                try:
                    with open("../Texts/Collection_" + str(collection_index) + ".txt", 'w') as f:
                        f.write(url + "\n\n")
                        f.write(text)
                except UnicodeEncodeError:
                    pass
                collection_index += 1
            self.collection_dict[text] = url
            if "" in self.collection_dict and len(self.collection_dict) == num_collection + 1:
                self.collection_dict.pop("")
                break
            elif "" not in self.collection_dict and len(self.collection_dict) == num_collection:
                break

        print(len(self.collection_dict))


    def get_query_from_file(self):
        """
        Retrieves query as String from file
        :return:
        """
        with open(self.query_file_name, 'r') as f:
            self.query_str = f.read().lower()
        self.query_list = self.query_str.split(' ')

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
        for text in self.collection_dict:
            match_index = self.rabin_karp(text, self.query_str)
            if match_index:
                print("Matching text found in url:", self.collection_dict[text])
                print("At position:", match_index)

    def sentence_rabin_karp(self):
        """
        Splits the query into sentences to allow for finer searches using the Rabin-Karp algorithm
        :return:
        """
        sentences = self.query_str.split(". ")
        for i in range(len(sentences)):
            for text in self.collection_dict:
                match_index = self.rabin_karp(text, sentences[i])
                if match_index:
                    print("sentence {i} matches at: {positions}".format(i=i, positions=match_index))

    def get_scores_and_url(self):
        """
        Calculates the similarity scores between the query and documents, and returns a tuple (score, url)in reverse
        sorted order, with the url that has the most similar text as the first element.
        :return:
        """
        scores = {}
        query_vector = self.calculate_query_vector()
        print(query_vector)
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
        df = 0
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
        """
        Returns a hash value for a string using a polynomial hash function
        :param s:
        :param p:
        :param x:
        :return:
        """
        h = 0
        for i in range(len(s) - 1, -1, -1):
            h = (h * x + ord(s[i])) % p
        return h
