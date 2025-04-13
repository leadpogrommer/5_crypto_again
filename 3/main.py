#!/usr/bin/env python3
import math
from io import BytesIO
from typing import IO, TextIO
import click
import numpy as np
from collections import Counter
import tty

@click.group()
def cli():
    ...

@cli.command()
@click.argument('data', type=click.File('rb'))
@click.argument('key', type=click.File('rb'))
@click.argument('output', type=click.File('wb'))
def xor(data: BytesIO, key: BytesIO, output: BytesIO):
    data = np.fromfile(data, dtype=np.uint8)
    key = np.fromfile(key, dtype=np.uint8)
    if data.shape != key.shape:
        print('Data and key must have the same length')
        exit(1)
    output.write((data ^ key).tobytes())


def randgen(key: np.array):
    S = np.arange(0, 256, 1, dtype=np.uint8)
    # print(S)
    l = key.shape[0]
    j = 0
    for i in range(0, 256):
        j = (j + S[i] + key[i % l])
        S[i], S[j] = S[j], S[i]
    i, j = 0, 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i])
        S[i], S[j] = S[j], S[i]
        t = (S[i] + S[j])
        yield S[t]


@cli.command()
@click.argument('data', type=click.File('rb'))
@click.argument('key', type=click.File('rb'))
@click.argument('output', type=click.File('wb'))
def rc4(data: BytesIO, key: BytesIO, output: BytesIO):
    key = np.fromfile(key, dtype=np.uint8)
    gen = randgen(key)
    np.seterr(over='ignore')
    while byte := data.read(1):
        output.write(bytes([next(gen) ^ byte[0]]))



if __name__ == '__main__':
    cli()