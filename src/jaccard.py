#!/usr/bin/env python3.9

from collections.abc import Generator


def generate_ngrams(text: list[str], n: int) -> Generator[list[str], None, None]:
    """
    Returns a generator that yields the n-grams from a piece of text.

    :param text: The input text as a list of words.

    :param n: The length of the n-grams

    :return: A generator object generating all of the n-grams in the text.
    """
    if n == 1:
        yield from ([word] for word in text)
        return None

    iterator = iter(text)
    previous = [next(iterator) for _ in range(n - 1)]
    for word in iterator:
        previous.append(word)
        yield previous
        del previous[0]
