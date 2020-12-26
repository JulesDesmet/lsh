#!/usr/bin/env python3.9


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

    def __init__(self, nr_bands: int, rows_per_band: int) -> None:
        """
        Initialises the data structure.

        :param nr_bands: The number of bands of rows of the matrix M (i.e. the
        parameter b) used for LSH.

        :param rows_per_band: The number of rows r in each band. Combined with
        `nr_bands` the number of rows of the matrix M can be determined.
        """
        self.nr_bands = nr_bands
        self.rows_per_band = rows_per_band

    def add_document(self) -> None:
        """
        """

    def query(self):
        """
        """
