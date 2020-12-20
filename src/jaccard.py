#!/usr/bin/env python3.9

from collections.abc import Generator, Iterable


def get_ngrams(text: Iterable[str], n: int) -> Generator[tuple[str, ...], None, None]:
    """
    Returns a generator that yields the n-grams from a piece of text.

    :param text: The input text as a list of words.

    :param n: The length of the n-grams

    :return: A generator object generating all of the n-grams in the text.
    """
    if n == 1:
        yield from ((word,) for word in text)
        return None

    iterator = iter(text)
    previous = [next(iterator) for _ in range(n - 1)]
    for word in iterator:
        previous.append(word)
        yield tuple(previous)
        del previous[0]


class ShingleGenerator:
    """
    """

    #
    text: Iterable[Iterable[str]]
    # 
    n: int
    # 
    ngrams: list[tuple[str, ...]]
    # 
    inverse_ngrams: dict[tuple[str, ...], int]

    def __init__(self, text: Iterable[Iterable[str]], n: int) -> None:
        """
        """
        self.text = text
        self.n = n
        self.ngrams = []
        self.inverse_ngrams = {}

    def __iter__(self) -> Generator[set[int], None, None]:
        """
        """
        for entry in self.text:
            shingles = set()
            for ngram in get_ngrams(entry, self.n):

                if ngram not in self.inverse_ngrams:
                    fingerprint = len(self.ngrams)
                    self.inverse_ngrams[ngram] = fingerprint
                    self.ngrams.append(ngram)
                    shingles.add(fingerprint)

                else:
                    shingles.add(self.inverse_ngrams[ngram])

            yield shingles
