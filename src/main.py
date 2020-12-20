#!/usr/bin/env python3.9

from jaccard import ShingleSetGenerator

from collections.abc import Generator, Iterable
from csv import reader
from re import split


def read_csv(filename: str) -> Generator[dict[str, str], None, None]:
    """
    Reads a file as a CSV file, assuming that the first row is the header.

    :param filename: The name of the CSV file.

    :return: A generator that yields each row of the CSV file, excluding the
    header, as a dictionary. The keys of this dictionary are the column names
    taken from the header row.
    """
    with open(filename) as csv_file:
        csv_reader = reader(csv_file)

        header = next(csv_reader)
        for row in csv_reader:
            yield dict(zip(header, row))


def read_data(data: Iterable[dict[str, str]]) -> Generator[list[str], None, None]:
    """
    Extracts the required data from the data rows read from the CSV file.

    :param data: An iterable of dictionary objects. These dictionaries should
    contain the keys `"News_ID"` and `"article"`. Other keys will be ignored.

    :return: A `Generator` object that yields the data as lists of strings.
    """
    for entry in data:
        text = entry["article"]
        words = split(r"\W+", text)
        yield [word.lower() for word in words]


if __name__ == "__main__":
    filename = "data/news_articles_small.csv"
    csv_reader = read_csv(filename)

    shingle_gen = ShingleSetGenerator(read_data(csv_reader), 2)
    for shingle_set in shingle_gen:
        print("[", " ".join(str(v) for v in list(shingle_set)[:20]), "..." if len(shingle_set) > 20 else "", "]")
    print(len(shingle_gen.shingles))
