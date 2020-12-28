#!/usr/bin/env python3.9

from minhash import create_minhash
from shingle import convert_shingles_to_bytes, Token

from datasketch import MinHash

from collections.abc import Callable, Iterable
from hashlib import sha1
from typing import TypeVar, Union


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
    bands: list[dict[bytes, int]]
    hash_function: Callable[[bytes], bytes]
    _next_doc_id: int

    def __init__(
        self,
        nr_bands: int,
        rows_per_band: int,
        hash_function: Callable[[bytes], bytes] = sha1,
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
        self.bands = [{} for _ in range(nr_bands * rows_per_band)]
        self.hash_function = hash_function
        self._next_doc_id = 0

    @property
    def nr_rows(self) -> int:
        """
        Returns the number of rows of the matrix.
        """
        return self.nr_bands * self.rows_per_band

    def add_document(self, minhash_values: Iterable[int]) -> int:
        """
        Adds a document to the matrix as a column. This function will compute
        the `self.nr_bands` hashes, one for each band, and add them to the end
        of the matrix rows.

        :param minhash_values: The hash values computed by the minhash
        algorithm. These are also a single column of the signature matrix M.
        Calls to this function of the same object should have hash values of the
        same minhash object/algorithm as well.

        :return: The document's ID within the LSH data structure. This is simply
        the column number (starting with 0) that contains the document's
        signature.
        """
        document_id = self._next_doc_id
        self._next_doc_id += 1

        for band in range(self.nr_bands):
            values = minhash_values[
                self.rows_per_band * band : self.rows_per_band * (band + 1)
            ]

            byte_string = b"".join(int(value).to_bytes(8, "big") for value in values)
            hash_value = self.hash_function(byte_string).digest()

            band_dict = self.bands[band]
            if hash_value not in band_dict:
                band_dict[hash_value] = {document_id}
            else:
                band_dict[hash_value].add(document_id)

        return document_id

    def query(self) -> set[tuple[int]]:
        """
        Returns the IDs of the similar documents.

        :return: A set of tuples of document IDs. Each tuple of IDs is a group
        of similar documents.
        """
        matches = set()

        for band in self.bands:
            for document_ids in band.values():
                if len(document_ids) > 1:
                    matches.add(tuple(sorted(document_ids)))

        return matches
