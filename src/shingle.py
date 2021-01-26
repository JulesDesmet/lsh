#!/usr/bin/env python3.9

from collections.abc import Generator, Iterable
from typing import Union, TypeVar


def get_ngrams(text: Iterable[str], n: int) -> Generator[tuple[str, ...], None, None]:
    """
    Returns a generator that yields the word n-grams (i.e. shingles) from a
    piece of text.

    :param text: The input text as a list of words.

    :param n: The length of the n-grams

    :return: A generator object generating all of the n-grams in the text.
    """
    if n <= 0:
        return None

    if n == 1:
        # (word,) is a tuple with just one element, without the comma it'd be a string
        yield from ((word,) for word in text)
        return None

    try:
        iterator = iter(text)
        previous = [next(iterator) for _ in range(n - 1)]
    except StopIteration:
        # If the text is shorter than the number of words per shingle, yield nothing
        return None

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


def convert_int_shingle_to_bytes(shingle: int) -> bytes:
    """
    Converts a shingle to a byte string.

    :param shingle: The shingle as an integer.

    :return: A byte string that represents the shingle.
    """
    return shingle.to_bytes(8, "big")


def convert_str_shingle_to_bytes(shingle: tuple[str, ...]) -> bytes:
    """
    Converts a shingle to a byte string.

    :param shingle: The shingle as a tuple of strings.

    :return: A byte string that represents the shingle. Each string is added to
    the byte string, with the null character \x00 as separator.
    """
    return "\x00".join(shingle).encode()


def convert_bytes_shingle_to_bytes(shingle: tuple[bytes, ...]) -> bytes:
    """
    Converts a shingle to a byte string.

    :param shingle: The shingle as a tuple of byte strings.

    :return: A byte string that represents the shingle. Each byte string is
    added to the byte string, with the null character \x00 as separator.
    """
    return b"\x00".join(shingle)


# A dictionary of converters for the possible token types
converters = {
    int: convert_int_shingle_to_bytes,
    str: convert_str_shingle_to_bytes,
    bytes: convert_bytes_shingle_to_bytes,
}


# A type variable that can be one of the possible token types
Token = TypeVar("Token", int, tuple[str, ...], tuple[bytes, ...])


def convert_shingles_to_bytes(
    shingles: Iterable[Union[int, tuple[str, ...], tuple[bytes, ...]]],
) -> Generator[bytes, None, None]:
    """
    Converts all shingles in an iterable to byte strings.

    :param shingles: The list of shingles, which should all be of the same type.
    This type must be either an integer, or a tuple of strings or byte strings.
    Only the type of the first shingle is checked, and thus all of the other
    shingles must have the same type to avoid errors.

    :return: A generator that yields the converted shingles.
    """
    convert = None
    for shingle in shingles:
        if convert is None:
            shingle_type = int if type(shingle) is int else type(shingle[0])
            convert = converters[shingle_type]
        yield convert(shingle)
