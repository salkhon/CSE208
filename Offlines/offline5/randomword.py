from typing import List
import string
import random


def random_word(word_len: int, alphabet: List[str] = None) -> str:
    if alphabet is None:
        alphabet = list(string.ascii_letters)
    
    rand_word = ""
    for letter in range(word_len):
        letter = alphabet[random.randint(0, len(alphabet) - 1)]
        rand_word += letter
    
    return rand_word