#!/usr/bin/env python3

from typing import IO, TextIO

import click
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

def c_encrypt(s: str, key: int) -> str:
    return "".join([(chr(  ((ord(c) - ord('a')) + key) % 26 + ord('a')  ) if c != ' ' else c)for c in s])
def c_decrypt(s: str, key: int) -> str:
    return c_encrypt(s, 26 - key)


def get_key(plaintext: str, cyphertext: str) -> int:
    if len(plaintext) != len(cyphertext):
        raise ValueError("plaintext and cyphertext must have same length")
    diffs = (np.fromstring(cyphertext, np.int8) - np.fromstring(plaintext, np.int8)) % 26
    ud = np.unique(diffs)
    if len(ud) != 1:
        raise ValueError("keys for individual symbols do not match")
    return ud[0]


@click.group()
def cli():
    ...

@cli.command()
@click.argument('plaintext', type=str)
@click.argument('key', type=int)
def encrypt(plaintext: str, key: int):
    print(c_encrypt(plaintext.lower(), key))

@cli.command()
@click.argument('cyphertext', type=str)
@click.argument('key',  type=int)
def decrypt(cyphertext: str, key: int):
    print(c_decrypt(cyphertext.lower(), key))

@cli.command()
@click.argument('plaintext', type=str)
@click.argument('cyphertext', type=str)
def plaintext_attack(plaintext: str, cyphertext: str):
    print(get_key(plaintext, cyphertext))

@cli.command()
@click.argument('cyphertext', type=str)
def cyphertext_attack(cyphertext: str):
    for key in range(1, 26):
        print(f'{key}: {c_decrypt(cyphertext.lower(), key)}')

@cli.command()
@click.argument('dictionary', type=click.File('r'))
@click.argument('cyphertext', type=str)
def dict_attack(cyphertext: str, dictionary: TextIO):
    mapped = map(lambda a: a.strip(), dictionary.readlines())
    dict_entries = set(filter(lambda a: len(a) > 0, mapped))
    encrypted_words = set(cyphertext.split(' '))
    for key in range(1, 26):
        decrypted_words = {c_decrypt(w, key) for w in encrypted_words}
        matched_words = {w for w in decrypted_words if w in dict_entries}
        if len(matched_words) != 0:
            print(f'{key=} {matched_words=}: {c_decrypt(cyphertext, key)}')

if __name__ == '__main__':
    cli()