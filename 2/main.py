#!/usr/bin/env python3
import math
from io import BytesIO
from typing import IO, TextIO
import click
import numpy as np
from collections import Counter

@click.group()
def cli():
    ...

@cli.command()
@click.argument('file', type=click.File('r'))
def freq(file: TextIO):
    cntr = Counter(file.read().lower())
    for char, count in cntr.most_common():
        if char.isspace():
            continue
        print(f'{char}: {count}')

@cli.command()
@click.argument('file', type=click.File('rb'))
def ent(file: BytesIO):
    data = file.read()
    cntr = Counter(data)
    ent = -sum(((Pi := v/len(data))*math.log2(Pi) for v in cntr.values()))
    print(f'{ent:.02}')


if __name__ == '__main__':
    cli()