#!/usr/bin/env python3.9
from jaccard import ShingleSetGenerator, jaccard

from collections.abc import Generator, Iterable
from csv import reader
from re import split
from datasketch import MinHash, MinHashLSHForest
import time
import re
import numpy as np


def preprocess(text) -> list[str]:
    # Temporary
    text = re.sub(r'[^\w\s]','',text)
    tokens = text.lower()
    tokens = tokens.split()
    return tokens


def get_minforest(data, perm):
    """
    This function returns the Min LSH Forest of size perm
    :param data:
    :param perm:
    :return:
    """
    start = time.time()

    minhash = []
    for text in data:
        tokens = preprocess(text)
        m = MinHash(num_perm=perm)
        for shingle in tokens:
            m.update(shingle.encode('utf8'))
        minhash.append(m)
    minforest = MinHashLSHForest(num_perm=perm)
    for i, m in enumerate(minhash):
        minforest.add(i, m)

    minforest.index()
    print('It took %s seconds to build forest.' %(time.time()-start))
    return minforest


def query(text: str, db, perm, results, minforest):
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