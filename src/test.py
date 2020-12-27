#!/usr/bin/env python3.9

from shingle import (
    convert_bytes_shingle_to_bytes,
    convert_int_shingle_to_bytes,
    convert_shingles_to_bytes,
    convert_str_shingle_to_bytes,
    get_ngrams,
    ShingleSetGenerator,
)

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
        text = [
            ["a", "b", "c", "d", "e"],
            ["b", "a", "b"],
            ["d", "e", "f"],
        ]
        generator = ShingleSetGenerator(text, 2)

        for index, shingle_set in enumerate(generator):
            ngrams = get_ngrams(text[index], 2)
            shingles = {generator.shingles[shingle_id] for shingle_id in shingle_set}
            self.assertEqual(set(ngrams), shingles)

        for index, shingle in enumerate(generator.shingles):
            self.assertIn(shingle, generator.inverse_shingles)
            self.assertEqual(index, generator.inverse_shingles[shingle])

    def test_convert_int_shingle_to_bytes(self) -> None:
        """
        Tests the `convert_int_shingle_to_bytes()` function.
        """
        shingles = [234, 654, 120398]

        for shingle in shingles:
            byte_string = convert_int_shingle_to_bytes(shingle)
            self.assertEqual(int.from_bytes(byte_string, "big") % (2 ** 63), shingle)

    def test_convert_str_shingle_to_bytes(self) -> None:
        """
        Tests the `convert_str_shingle_to_bytes()` function.
        """
        shingles = [("a", "b", "c"), ("test", "shingle"), ("123",)]

        for shingle in shingles:
            byte_string = convert_str_shingle_to_bytes(shingle)
            string = byte_string.decode()
            self.assertEqual(string.split("\x00"), list(shingle))

    def test_convert_bytes_shingle_to_bytes(self) -> None:
        """
        Tests the `convert_bytes_shingle_to_bytes()` function.
        """
        shingles = [(b"a", b"b", b"c"), (b"test", b"shingle"), (b"123",)]

        for shingle in shingles:
            byte_string = convert_bytes_shingle_to_bytes(shingle)
            self.assertEqual(byte_string.split(b"\x00"), list(shingle))

    def test_convert_shingles_to_bytes(self) -> None:
        """
        Tests the `convert_shingles_to_bytes()` function.
        """
        shingle_lists = [
            [3, 53, 678, 134, 785, 2534, 56],
            [("a", "b"), ("b", "c")],
            [(b"a", b"b"), (b"b", b"c")],
        ]
        expected_lists = [
            [convert_int_shingle_to_bytes(shingle) for shingle in shingle_lists[0]],
            [convert_str_shingle_to_bytes(shingle) for shingle in shingle_lists[1]],
            [convert_bytes_shingle_to_bytes(shingle) for shingle in shingle_lists[2]],
        ]

        for shingles, expected in zip(shingle_lists, expected_lists):
            byte_strings = list(convert_shingles_to_bytes(shingles))
            self.assertEqual(byte_strings, expected)


if __name__ == "__main__":
    from unittest import main

    main(verbosity=2)
