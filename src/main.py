#!/usr/bin/env python3.9

from jaccard import ShingleSetGenerator, jaccard
from minhash import get_minforest, query
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
    forest = get_minforest(database['article'], 256)
    q = "Richard Krajicek ensured an all-Dutch final in the ATP's 600,000 dollar event here Sunday when he beat Omar Camporese of Italy 6-3, 7-5. Authorities arrested a close aide to Indonesia's most-wanted terrorist, police said Sunday, shooting the suspect in the leg as he tried to escape a raid on his hide-out. A car bomb claimed by dissident Republican paramilitaries cast a cloud Monday over the transfer of key powers from London to Northern Ireland. Billy Wilder's death on Wednesday snuffed out the last of cinema's great Austro-German brigade, a generation of filmmakers who brought to Hollywood a style and a set of attitudes we still feel even if we can't quite place the names. Murnau was the poetic one, von Stroheim in the A Bangladeshi with the same nickname as a murder suspect was mistakenly tried and given the death sentence for a crime he did not commit, his lawyers told a court Wednesday. If President Bush or Vice President Dick Cheney were ever to be impeached, their foes could cite this Independence Day as a milestone -- the day that the nation's first ``impeachment headquarters'' opened its doors. Negotiators for Hollywood actors and producers were meeting Saturday in an eleventh-hour effort to reach a new contract and avert what could be a crippling walkout for the TV and movie industry. Human rights group Amnesty International (AI) said Monday that it had sent a second delegation to Israel on a fact-finding mission to investigate violent clashes in Israel and the occupied territories."

    result = query(q, database, 256, 3, forest)
    print(result)
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
