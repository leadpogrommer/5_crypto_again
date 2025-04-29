#!/usr/bin/env python3

import click
from PIL import Image
from io import BytesIO
import numpy as np

@click.group()
def cli():
    ...





def insert_bits_into_arr(arr: np.array, data: bytes):
    data = len(data).to_bytes(4, byteorder='little', signed=False) + data
    bitgen = ((byte >> i)&1 for byte in data for i in range(8))
    for i, bit in enumerate(bitgen):
        arr.flat[i] = (arr.flat[i] & 0b11111110) | bit


def read_bytes_from_arr(arr: np.array, n: int, offset: int) -> bytes:
    bitgen = (b & 1 for b in arr.flat[offset*8:])
    res = bytes()
    for byte_n in range(n):
        cv = 0
        for bit_n in range(8):
            cv |= (next(bitgen) << bit_n)
        res += bytes([cv])
    return res


@cli.command()
@click.argument('input', type=click.File('rb'))
@click.argument('output', type=click.File('wb'))
@click.argument('data', type=click.File('rb'))
def hide(input: BytesIO, output: BytesIO, data: BytesIO):
    in_img = Image.open(input)
    arr = np.array(in_img)
    insert_bits_into_arr(arr, data.read())
    out_img = Image.fromarray(arr)
    out_img.save(output)

@cli.command()
@click.argument('input', type=click.File('rb'))
@click.argument('output', type=click.File('wb'))
def reveal(input: BytesIO, output: BytesIO):
    in_img = Image.open(input)
    arr = np.array(in_img)
    l = int.from_bytes(read_bytes_from_arr(arr, 4, 0), byteorder='little', signed=False)
    print(f'Payload length: {l}')
    payload = read_bytes_from_arr(arr, l, 4)
    output.write(payload)






if __name__ == '__main__':
    cli()