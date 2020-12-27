#!/usr/bin/env python3.9

from shingle import get_ngrams

from unittest import TestCase


class ShingleTest(TestCase):
    """
    Tests for the functionality defined in the `shingle` module.
    """

    def test_get_ngrams(self) -> None:
        """
        Tests the `get_ngrams()` function.
        """
        string = ["test", "string", "for", "this", "function"]
        expected = [
            [],
            [("test",), ("string",), ("for",), ("this",), ("function",)],
            [
                ("test", "string"),
                ("string", "for"),
                ("for", "this"),
                ("this", "function"),
            ],
            [
                ("test", "string", "for"),
                ("string", "for", "this"),
                ("for", "this", "function"),
            ],
            [("test", "string", "for", "this"), ("string", "for", "this", "function")],
            [("test", "string", "for", "this", "function")],
            [],
        ]

        for words_per_ngram, expected_ngrams in enumerate(expected):
            with self.subTest(words_per_ngram=words_per_ngram):
                ngram_generator = get_ngrams(string, words_per_ngram)
                self.assertEqual(list(ngram_generator), expected_ngrams)

    def test_shingle_set_generator(self) -> None:
        """
        Tests the `ShingleSetGenerator` class.
        """
        string = []

    def test_convert_int_shingle_to_bytes(self) -> None:
        """
        Tests the `convert_int_shingle_to_bytes()` function.
        """

    def test_convert_str_shingle_to_bytes(self) -> None:
        """
        Tests the `convert_str_shingle_to_bytes()` function.
        """

    def test_convert_bytes_shingle_to_bytes(self) -> None:
        """
        Tests the `convert_bytes_shingle_to_bytes()` function.
        """

    def test_convert_shingles_to_bytes(self) -> None:
        """
        Tests the `convert_shingles_to_bytes()` function.
        """


if __name__ == "__main__":
    from unittest import main

    main(verbosity=2)
