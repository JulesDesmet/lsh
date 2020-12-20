#!/usr/bin/env python3.9

from csv import reader
from typing import Generator


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


if __name__ == "__main__":
    for row in read_csv("data/news_articles_small.csv"):
        print(f"{row['News_ID']:>5} {row['article'][:100]}")
