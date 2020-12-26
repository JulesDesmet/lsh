#!/usr/bin/env python3.9

from collections.abc import Generator, Iterable
from typing import Union


def get_ngrams(text: Iterable[str], n: int) -> Generator[tuple[str, ...], None, None]:
    """
    Returns a generator that yields the word n-grams (i.e. shingles) from a
    piece of text.

    :param text: The input text as a list of words.

    :param n: The length of the n-grams

    :return: A generator object generating all of the n-grams in the text.
    """

    # I think this has to just be (word) without , ?
    if n == 1:
        yield from ((word,) for word in text)
        return None

    iterator = iter(text)
    previous = [next(iterator) for _ in range(n - 1)]
    for word in iterator:
        previous.append(word)
        yield tuple(previous)
        del previous[0]


class ShingleSetGenerator(Iterable):
    """
    A generator class that produces a set of shingles for each list of strings
    in a list of lists of strings. The object also keeps track of which numbers
    are used for which n-grams. (TODO remove this?)
    """

    # The input: an iterable of documents, which are iterables of strings
    _text: Iterable[Iterable[str]]
    # The size of the n-grams
    _n: int
    # A list of all of the n-grams, in order of insertion
    shingles: list[tuple[str, ...]]
    # A mapping of n-grams to their indices in `self.ngrams`
    inverse_shingles: dict[tuple[str, ...], int]

    def __init__(self, text: Iterable[Iterable[str]], n: int) -> None:
        """
        Initialises the object, but doesn't generate any shingles yet.

        :param text: The input data, as an iterable of documents, which are
        iterables of strings.

        :param n: The size of the n-grams.
        """
        self._text = text
        self._n = n
        self.shingles = []
        self.inverse_shingles = {}

    def __iter__(self) -> Generator[set[int], None, None]:
        """
        Returns a generator that yields the sets of shingles for our input data.
        This function adds new shingles it hasn't encountered before to the
        internal list of shingles and to the mapping of shingles to IDs.

        :return: A `Generator` object that yields sets of shingle IDs.
        """
        for entry in self._text:
            shingles = set()
            for ngram in get_ngrams(entry, self._n):

                if ngram not in self.inverse_shingles:
                    fingerprint = len(self.shingles)
                    self.inverse_shingles[ngram] = fingerprint
                    self.shingles.append(ngram)
                    shingles.add(fingerprint)
                else:
                    shingles.add(self.inverse_shingles[ngram])

            yield shingles


def convert_to_bytes(shingle: tuple[Union[int, str, bytes], ...]) -> bytes:
    """
    Converts a shingle to a single `bytes` object.

    :param shingle: The shingle, which can be a tuple of integers, strings, or
    bytes.

    :return: A `bytes` object containing the tokens from the shingle. For
    shingles consisting `str` and `bytes` tokens, the null character (`\x00`) is
    used as a separator. This means that tokens shouldn't contain the null
    character. For `int` tokens, there is no separator, but the integers should
    fit in 64 bits (as signed integers).
    """
    shingle_bytes: bytes = None
    shingle_type = type(shingle[0])

    if shingle_type is int:
        # Assuming the integers fit in 64 bits == 8 bytes
        temp_bytes = bytearray(8 * len(shingle))
        for index, value in enumerate(shingle):
            temp_bytes[8 * index : 8 * index + 8] = value.to_bytes(8, "big")
        shingle_bytes = bytes(temp_bytes)

    elif shingle_type is str:
        # Use a separator (e.g. null) to make sure shingles like (A, BC)
        # and (AB, C) don't produce the same value ABC for `shingle_bytes`
        # With a separator they produce different values: "A BC" and "AB C",
        # assuming that individual tokens don't contain the separator
        shingle_bytes = "\x00".join(token for token in shingle).encode()

    else:
        # The total size of the shingle's tokens, and 1 byte separators
        total_size = sum(len(token) for token in shingle) + len(shingle) - 1
        temp_bytes = bytearray(total_size)

        location = 0
        for token in shingle:
            temp_bytes[location : location + len(token)] = token
            location += len(token) + 1
        shingle_bytes = temp_bytes

    return shingle_bytes
