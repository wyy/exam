#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import math
import random
import time
import argparse

class options:
    freq = 0.1
    spread = 3.0
    os = random.randint(0, 256)
    duration = 12
    speed = 20.0
    animate = False

def rgb256(rgb):
    r, g, b = rgb
    gray_possible = True
    sep = 42.5
    while gray_possible:
        if r < sep or g < sep or b < sep:
            gray = r < sep and g < sep and b < sep
            gray_possible = False
        sep += 42.5
    if gray:
        i = 232 + int(sum(rgb)/33.0)
    else:
        i = 16 + sum([int(v / 256.0 * 6) * mod for v, mod in zip(rgb, [36, 6, 1])])
    return i

def rainbow(freq, i):
    r = math.sin(freq * i + 0) * 127 + 128
    g = math.sin(freq * i + 2 * math.pi / 3) * 127 + 128
    b = math.sin(freq * i + 4 * math.pi / 3) * 127 + 128
    return r, g, b

def print_plain(line):
    for i, c in enumerate(line):
        rgb = rainbow(options.freq, options.os + i / options.spread)
        fg = '\033[38;5;%dm' % rgb256(rgb)
        print(fg + c + '\033[0m', end='')

def print_ani(line):
    os = options.os
    print('\033[?25l', end='')
    for i in range(1, options.duration):
        options.os += options.spread
        print('\r', end='')
        print_plain(line)
        time.sleep(1 / options.speed)
    print('\033[?25h', end='')
    options.os = os

def run():
    for line in sys.stdin:
        line = line.rstrip()
        options.os += 1
        if options.animate:
            print_ani(line)
        else:
            print_plain(line)
        print()

def main():
    parser = argparse.ArgumentParser(description='Rainbow')
    parser.add_argument('-a', '--animate', action='store_true',
                        help='enable psychedelics')
    ar = parser.parse_args()
    options.animate = ar.animate
    run()

if __name__ == '__main__':
    main()
