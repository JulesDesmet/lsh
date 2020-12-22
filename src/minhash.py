#!/usr/bin/env python3.9
from jaccard import ShingleSetGenerator, jaccard

from collections.abc import Generator, Iterable
from csv import reader
from re import split
from datasketch import MinHash,MinHashLSH, MinHashLSHForest
import time
import re
import numpy as np


def preprocess(text) -> list[str]:
    # Temporary
    text = re.sub(r'[^\w\s]','',text)
    tokens = text.lower()
    tokens = tokens.split()
    return tokens


def create_minhash(data, perm):
    start = time.time()
    minhash = []
    for text in data:
        tokens = preprocess(text)
        m = MinHash(num_perm=perm)
        for shingle in tokens:
            m.update(shingle.encode('utf8'))
        minhash.append(m)
    print('It took %s seconds to build minhash.' % (time.time() - start))
    return minhash


def get_minforest(data, perm):
    """
    This function returns the Min LSH Forest of size perm
    :param data:
    :param perm:
    :return:
    """
    start = time.time()
    minhash = create_minhash(data, perm)
    minforest = MinHashLSHForest(num_perm=perm)
    for i, m in enumerate(minhash):
        minforest.add(i, m)
    minforest.index()
    print('It took %s seconds to build forest.' %(time.time()-start))
    return minforest


def minhash_lsh(data, treshhold, perm):
    start = time.time()
    minhash = create_minhash(data, perm)
    minLSH = MinHashLSH(threshold=treshhold, num_perm=perm)
    for i, m in enumerate(minhash):
        minLSH.insert(str(i), m)
    print('It took %s seconds to build LSH index.' % (time.time() - start))
    return minLSH


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


def query_lsh(text: str, db, lsh, perm):
    tokens = preprocess(text)
    m = MinHash(num_perm=perm)
    for shingle in tokens:
        m.update(shingle.encode('utf8'))
    index = lsh.query(m)
    print("This is the amount of results: {}".format(index))
    result = db.iloc[index]['article']
    return result
