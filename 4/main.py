#!/usr/bin/env python3

import click
from Crypto.Cipher import AES
from io import BytesIO
import numpy as np

@click.group()
def cli():
    ...

BLOCK_SIZE_BYTES=16


def pad(data: bytes) -> bytes:
    to_add = (BLOCK_SIZE_BYTES - (len(data) + 1)) % BLOCK_SIZE_BYTES + 1
    return data + bytes([to_add]) * to_add

def unpad(data: bytes) -> bytes:
    to_remove = data[-1]
    return data[:-to_remove]


@cli.command()
@click.argument('key', type=click.File('rb'))
@click.argument('iv', type=click.File('rb'))
@click.argument('data', type=click.File('rb'))
@click.argument('output', type=click.File('wb'))
def encrypt(iv: BytesIO, key: BytesIO, data: BytesIO, output: BytesIO):
    key_bytes = key.read(16)
    iv_bytes = iv.read(16)
    data_bytes = pad(data.read())
    # print(len(data_bytes), len(data_bytes) % 16)
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv=iv_bytes)
    res_bytes = cipher.encrypt(data_bytes)
    output.write(res_bytes)

@cli.command()
@click.argument('key', type=click.File('rb'))
@click.argument('iv', type=click.File('rb'))
@click.argument('data', type=click.File('rb'))
@click.argument('output', type=click.File('wb'))
def decrypt(iv: BytesIO, key: BytesIO, data: BytesIO, output: BytesIO):
    key_bytes = key.read(16)
    iv_bytes = iv.read(16)
    data_bytes = data.read()
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv=iv_bytes)
    res_bytes = cipher.decrypt(data_bytes)
    output.write(unpad(res_bytes))







if __name__ == '__main__':
    cli()