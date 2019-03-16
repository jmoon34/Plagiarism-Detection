import random
import timeit

"""
Script for exploring the methods of searching for a phrase in a text

The two main methods are naive() and rabin_karp().  Naive implements a brute force method and works in O(T*P), where
T and P correspond to the length of the text and phrase respectively.  The Rabin-Karp algorithm uses a hash function
with a prime number designed to make the probability of collision <= 1/(10^6).  By using precomputation of hash values
of the text, this algorithm has runtime closer to O(T+P).
"""

def get_big_prime(max_length):
    """
    Returns prime such that probability of collision for hash value is <= 1/10**6
    :param max_length:
    :return:
    """
    p = max_length * 10**6
    while not is_prime(p):
        p += 1
    return p


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
    while i*i <= n:
        if n % i == 0 or n % (i+2) == 0:
            return False
        i += 6
    return True


def precompute_hashes(text, phrase_len, p, x):
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
    hash_list[t - phrase_len] = hash_string(last_string, p, x)
    y = 1
    for i in range(phrase_len):
        y = (y * x) % p
    for i in range(t-phrase_len-1, -1, -1):
        hash_list[i] = (x * hash_list[i+1] + ord(text[i]) - y * ord(text[i + phrase_len])) % p
    return hash_list

def hash_string(s, p, x):
    h = 0
    for i in range(len(s)-1, -1, -1):
        h = (h*x + ord(s[i])) % p
    return h

def rabin_karp(text, phrase):
    p = get_big_prime(len(phrase) + 1)
    x = random.randint(1, p-1)
    result = []
    phrase_hash = hash_string(phrase, p, x)
    hash_list = precompute_hashes(text, len(phrase), p, x)
    for i in range(len(text) - len(phrase) + 1):
        if phrase_hash != hash_list[i]:
            continue
        if text[i:i+len(phrase)] == phrase:
            result.append(i)
    return result

def naive(text, phrase):
    result = []
    for i in range(0, len(text)-len(phrase)+1):
        if text[i:(i+len(phrase))] == phrase:
            result.append(i)
    return result


def stress_test(max_t_len=10**4, max_p_len=10):
    while True:
        test_text = ""
        test_phrase = ""
        for i in range(max_t_len):
            test_text += chr(random.randint(32, 34))
        for i in range(max_p_len):
            test_phrase += chr(random.randint(32, 34))
        slow = naive(test_text, test_phrase)
        fast = rabin_karp(test_text, test_phrase)
        if slow == fast:
            print("Success", fast)
        else:
            print("Fail")
            print("slow:", slow)
            print("fast:", fast)
            return








