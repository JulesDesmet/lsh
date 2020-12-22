#!/usr/bin/env python3.9

from jaccard import ShingleSetGenerator, jaccard
from minhash import get_minforest, query, minhash_lsh, query_lsh
from collections.abc import Generator, Iterable
from csv import reader
from re import split
import pandas as pd


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
    # Panda version of database
    database = pd.read_csv('data/news_articles_small.csv')
    csv_reader = read_csv(filename)
    shingle_gen = ShingleSetGenerator(read_data(csv_reader), 2)
    shingle_sets = list(shingle_gen)
    #forest = get_minforest(database['article'], 256)
    lsh = minhash_lsh(database['article'], 0.3, 256)

    q = "The dollar tumbled to record lows against the yen and German mark Tuesday as currency markets were roiled by the Mexican economic crisis and investors shunned the greenback as a ""safe haven"" currency. There is no alien world behind the virtual reality gear, just a modestly decorated living room that can be seen without the video goggles. Chinese Internet portal Tencent Holdings said it will acquire a 10.26 percent stake in Digital Sky Technologies Ltd (DST), a Russian Internet investment firm and Facebook shareholder. Clearly Buhner, who spent 14 years with the Mariners, felt the love from a Safeco Field crowd of 40,805 -- and reciprocated. European countries were urged Thursday ""not to wait for another Madrid or Beslan"" and to take urgent, concrete steps to fight global terrorism. Japan has warned leaders of the House of Representatives that serious, long-term damage to Japanese-U.S. relations is likely if the House passes a resolution demanding an official apology from Japan for its wartime policy of forcing women to become sex slaves for Japanese soldiers. AMF Bowling Worldwide, the world's largest operator of bowling centers, filed for bankruptcy protection Tuesday under a plan that would allow it to repay debt and restructure its operations. China has recently set up a special work group to coordinate its efforts in cracking down on the crimes of producing and selling shoddy and fake products."


    #result = query(q, database, 256, 3, forest)
    result_lsh = query_lsh(q, database, lsh, 256)
    print(result_lsh)
    #print(result)
    result_matrix = []
"""
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
"""