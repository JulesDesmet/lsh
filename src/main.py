#!/usr/bin/env python3.9

from jaccard import jaccard
from lsh import LSH
from minhash import create_minhash
from shingle import ShingleSetGenerator, convert_shingles_to_bytes

from collections.abc import Generator, Iterable
from csv import reader
from re import split

import time

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
    Extracts the required data from the data rows read from the CSV file, and
    applies some preprocessing to the text.

    :param data: An iterable of dictionary objects. These dictionaries should
    contain the keys `"News_ID"` and `"article"`. Other keys will be ignored.

    :return: A `Generator` object that yields the data as lists of strings.
    """
    for entry in data:
        text = entry["article"]
        words = split(r"\W+", text)
        yield [word.lower() for word in words]


def generate_histogram(data: list[set[int]], nr_bars: int = 10) -> list[int]:
    """
    Generates histogram data for the Jaccard similarities between the data sets.
    Each bar of the histogram is equal in width.

    :param data: The shingle sets representing the documents. Each shingle
    should be represented by an integer, i.e. as returned by the
    `ShingleSetGenerator`.

    :param nr_bars: The number of bars the histogram will consist of. This also
    determines the width of each bar, and their represented range. For example,
    `nr_bars=10` means that each bar will be `0.1` wide, with the first bar
    representing the range `[0.0, 0.1[`. The range of each bar is a half-open
    interval (e.g. `[0.0, 0.1[`), except for the last one which is a closed
    interval (e.g. `[0.9, 1.0]`).

    :return: The counts for each bar of the histogram. The values in this list
    are ordered by increasing interval starts (e.g. first `[0.0, 0.1[`, then
    `[0.1, 0.2[`, ..., and finally `[0.9, 1.0]`).
    """
    buckets = [0 for _ in range(nr_bars)]
    for index_1, document_1 in enumerate(data):
        for document_2 in data[:index_1]:
            similarity = jaccard(document_1, document_2)

            # Computing bucket number by computing `floor(nr_bars * similarity)`
            # Using `min()` to put similarities of 1.0 in the last bucket
            bucket = min(int(nr_bars * similarity), nr_bars - 1)
            buckets[bucket] += 1
    return buckets


if __name__ == "__main__":
    start = time.time()
    filename = "data/news_articles_small.csv"

    csv_reader = read_csv(filename)
    data_reader = read_data(csv_reader)
    shingle_set_generator = ShingleSetGenerator(data_reader, 2)

    # buckets = generate_histogram(list(shingle_set_generator), 10)
    # for index, count in enumerate(buckets):
    #     print(f"[{index / 10}, {(1 + index) / 10}{']' if index == 9 else '['} :", count)

    byte_string_generator = (
       convert_shingles_to_bytes(shingle_set) for shingle_set in shingle_set_generator
    )

    nr_bands = 5
    rows_per_band = 20

    lsh = LSH(nr_bands, rows_per_band)
    for minhash in create_minhash(byte_string_generator, nr_bands*rows_per_band):
       lsh.add_document(minhash.hashvalues)
    print('It took %s seconds to build LSH.' % (time.time() - start))
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    specifity = 0
    for group, similarity in lsh.query().items():
        if any(x > 1000 for x in group):
            if any(x > 1050 for x in group):

                if similarity >= 0.8:
                    false_positive+=1
                else:
                    true_negative+=1
            else:
                if similarity >= 0.8:
                    true_positive+=1
                else:
                    false_negative+=1
    specificity = 0
    if (true_negative+false_positive)==0:
        specificity="None"
    else:
        specificity = true_negative/(true_negative+false_positive)
    precision = true_positive/(true_positive+false_positive)
    sensitivity = true_positive/(true_positive+false_negative)
    print("Specificity {}, Precision {}, Sensitivity {}".format(specificity,precision,sensitivity))
