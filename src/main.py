#!/usr/bin/env python3.9

from jaccard import ShingleSetGenerator, jaccard

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
    shingle_sets = list(shingle_gen)

    result_matrix = []
    for index, set_1 in enumerate(shingle_sets):
        result_matrix.append([])

        for set_2 in shingle_sets[:index]:
            result_matrix[index].append(jaccard(set_1, set_2))

    with open("output_2.csv", "w") as output:
        size = len(result_matrix)
        for row in range(size):
            for col in range(row):
                output.write(f"{result_matrix[row][col]},")
            output.write("1.0")
            for col in range(row + 1, size):
                output.write(f",{result_matrix[col][row]}")
            output.write("\n")
