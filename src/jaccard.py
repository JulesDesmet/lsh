#!/usr/bin/env python3.9

from typing import TypeVar


Shingle = TypeVar("Shingle")


def jaccard(set_1: set[Shingle], set_2: set[Shingle]) -> float:
    """
    Computes the Jaccard similarity between two sets.

    :param set_1:
    :param set_2: The sets for which the similarity should be computed.

    :return: The Jaccard similarity, which is computed as
    `|set_1 ∩ set_2| / |set_1 ∪ set_2|`.
    """
    if not set_1 and not set_2:
        return 0.0
    return len(set_1 & set_2) / len(set_1 | set_2)
