#!/usr/bin/env python3.9

from shingle import convert_to_bytes

from datasketch import MinHash

from collections.abc import Callable, Iterable
from typing import Union, TypeVar


class LSH:
    """
    An implementation of LSH, i.e. Locality-Sensitive Hashing. This technique
    partitions a signature matrix M into b bands of r rows. Then, a hash value
    is computed for each intersection of a column and a band. This means that
    for each column b hash values will be calculated. Near duplicate columns are
    (most likely) the ones that hash to the same buckets.
    """

    nr_bands: int
    rows_per_band: int
    matrix: list[list[bytes]]

    def __init__(
        self,
        nr_bands: int,
        rows_per_band: int,
        hash_function: Callable[[bytes], bytes] = hash,
    ) -> None:
        """
        Initialises the data structure.

        :param nr_bands: The number of bands of rows of the matrix M (i.e. the
        parameter b) used for LSH.

        :param rows_per_band: The number of rows r in each band. Combined with
        `nr_bands` the number of rows of the matrix M can be determined.

        :param hash_function: The hash function that is used in the algorithm.
        """
        self.nr_bands = nr_bands
        self.rows_per_band = rows_per_band
        self.matrix = [[] for _ in range(nr_bands * rows_per_band)]
        self.hash_function = hash_function

    @property
    def nr_rows(self) -> int:
        """
        Returns the number of rows of the matrix.
        """
        return self.nr_bands * self.rows_per_band

    def add_document(self, shingles: Iterable[tuple[Union[str, bytes, int]]]) -> None:
        """
        Adds a document to the matrix as a column. This function will compute
        the `self.nr_bands` hashes, one for each band, and add them to the end
        of the matrix rows.

        :param shingles: The list/set/... of shingles, which can be given as
        integers, strings, or bytes.
        """
        shingle_iterator = iter(shingles)
        shingle = next(shingle_iterator)

        try:
            minhash = MinHash(self.nr_rows)
            while True:
                for shingle in shingles:
                    shingle_bytes = convert_to_bytes(shingle)
                    minhash.update(shingle_bytes)
                minhash_values = minhash.hashvalues

                shingle = next(shingle_iterator)

        except StopIteration:
            pass

    def query(self):
        """"""
