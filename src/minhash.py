#!/usr/bin/env python3.9
from jaccard import ShingleSetGenerator, jaccard

from collections.abc import Generator, Iterable
from csv import reader
from re import split
from datasketch import MinHash, MinHashLSH, MinHashLSHForest
import time
import re
import numpy as np

# All functions here are based on https://github.com/ekzhu/datasketch


# Should be replaced with Shingle Generator, currently only able to generate unigrams
def preprocess(text) -> list[str]:
    """
    :param text: A string we want to split up in n-grams
    :return: Returns a list of the different n-grams
    """
    text = re.sub(r'[^\w\s]','',text)
    tokens = text.lower()
    tokens = tokens.split()
    return tokens


def create_minhash(data, perm):
    """
    :param data: The database, a collection of all the strings (articles/documents) we want to minhash
    :param perm: The amount of permutations we want to use to create the minhash
    :return: Returns a datasketch minhash structure
    """
    start = time.time()
    minhash = []
    for text in data:
        tokens = preprocess(text)
        m = MinHash(num_perm=perm)
        # We add each shingle in the minhash structure
        for shingle in tokens:
            m.update(shingle.encode('utf8'))
        minhash.append(m)
    print('It took %s seconds to build minhash.' % (time.time() - start))
    return minhash

# This function can be used to query top k-results but is currently not needed, may be interesting to use for analysis
def get_minforest(data, perm):
    """
    This function returns the Min LSH Forest of size perm
    :param data: The database, a collection of all the strings (articles/documents) we want to minhash
    :param perm: The amount of permutations we want to use to create the minhash
    :return: Returns a minforest structure which can be used for querying top k-results
    """
    start = time.time()
    minhash = create_minhash(data, perm)
    minforest = MinHashLSHForest(num_perm=perm)
    for i, m in enumerate(minhash):
        minforest.add(i, m)
    minforest.index()
    print('It took %s seconds to build forest.' %(time.time()-start))
    return minforest


def minhash_lsh(data, treshhold, perm, bands, rows):
    """
    LSH function that uses the datasketch LSH functionality, may be useful for comparing with own LSH algorithm
    :param data: Data
    :param treshhold: Threshhold to compare the Jaccard indices with
    :param perm: Amount of random permutations we use for the LSH algorithm
    :param bands: The amount of bands
    :param rows: The amount of rows
    :return: Returns a LSH structure based on MinHash which we can use to query
    """
    start = time.time()
    minhash = create_minhash(data, perm)
    minLSH = MinHashLSH(threshold=treshhold, num_perm=perm, params=(bands, rows))
    for i, m in enumerate(minhash):
        minLSH.insert(str(i), m)
    print('It took %s seconds to build LSH index.' % (time.time() - start))
    return minLSH


def query(text: str, db, perm, results, minforest):
    """
    :param text: The query
    :param db: The databse we can use to retrieve the results of our query
    :param perm: The amount of random permutations
    :param results: The amount of results we want to get from querying in our database, (k)
    :param minforest: The minforest structure to compare the query with
    :return: Top k-results
    """
    # Create shingles of our query
    tokens = preprocess(text)
    # Create a MinHash
    m = MinHash(num_perm=perm)
    for shingle in tokens:
        m.update(shingle.encode('utf8'))
    index = np.array(minforest.query(m, results))
    if len(index)==0:
        return None
    result = db.iloc[index]['article']
    return result


def query_lsh(text: str, db, lsh, perm):
    """
    :param text: The query (the string we want to check for duplicates)
    :param db: The database we want to retrieve our results from
    :param lsh: LSH structure
    :param perm: Amount of random permutations
    :return: Returns all results which are greater than the jaccard index specified in LSH
    """
    tokens = preprocess(text)
    m = MinHash(num_perm=perm)
    for shingle in tokens:
        m.update(shingle.encode('utf8'))
    index = lsh.query(m)
    print("This is the amount of results: {}".format(index))
    result = db.iloc[index]['article']
    return result
