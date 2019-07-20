#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import re
import argparse
import sys
import curses
import os
import lol
# import stat

def main():
    parser = argparse.ArgumentParser(description='Ce Shi')
    parser.add_argument('file', nargs='?', help='data file',
                        type=argparse.FileType('r'), default=sys.stdin)
    ar = parser.parse_args()
    
    b_isatty = sys.stdin.isatty()
    # print('isatty()', sys.stdin.isatty())
    # print('isfifo()', stat.S_ISFIFO(os.fstat(0).st_mode))
    a = []
    with ar.file as f:
        for line in f:
            line = line.strip().replace('\t', '    ')
            if not line: continue
            if (line[0] in "ABCD") and a:
                a[-1] += "\r\n    " + line
            else:
                a.append(line)
    lines = list(enumerate(a))
    random.shuffle(lines)
    
    if not b_isatty:
        sys.stdin = open('/dev/tty')
        os.dup2(sys.stdin.fileno(), 0)
    # print('isatty()', sys.stdin.isatty())
    # print('isfifo()', stat.S_ISFIFO(os.fstat(0).st_mode))
    stdscr = curses.initscr()
    stdscr.keypad(1)
    stdscr.refresh()
    # stdscr.timeout(0)
    # stdscr.getch()
    # stdscr.timeout(-1)
    status = '\x1b7' + '\033[%d;1H'%(curses.LINES) + \
             '\033[1;32m%d\033[0m-\033[1;31m%d\033[0m  %d/%d' + '\x1b8'
    clc_cs = '\033[H\033[2J'
    no = 0
    nx = 0
    r = re.compile('`([^`]+)`')
    # print('\x1b[?1049h')
    for index, line in lines:
        print(clc_cs + r.sub(' ______ ', line))
        print(status % (no, nx, no+nx, len(lines)))
        ans = r.findall(line)
        ans_p = ' '.join(list(map(lambda x: x.strip(), ans)))
        in_str = '\r\n \033[7m ans\033[0m: '
        if len(ans_p) == 1 and ans_p.upper() in 'ABCDOX':
            in_str += '(select ABCD or OX)'
            print(in_str, end='')
            c = stdscr.getch()
            ans_h = chr(c if c != 10 else 32)
        else:
            print(in_str, end='')
            ans_h = stdscr.getstr().decode('utf-8', 'ignore')
        if re.sub('[ ,　，]', '', ans_h).upper() == \
           re.sub('[ ,　，]', '', ans_p).upper():
            no += 1
            print(clc_cs + r.sub(' \033[1;42m \g<1> \033[0m ', line))
        else:
            nx += 1
            print(clc_cs + r.sub(' \033[1;41m \g<1> \033[0m ', line))
        print(status % (no, nx, no+nx, len(lines)))
        print(in_str + ans_h + '\r\n\r\n \033[7mnext\033[0m: ' + \
              '(press any key to continue, q to quit)', end='')
        c = stdscr.getch()
        if c == ord('q'): break
    # print('\x1b[?1049l', end='')
    stdscr.keypad(0)
    curses.endwin()
    lol.options.duration = 60
    lol.print_ani('%s: %d-%d' % (ar.file.name, no, nx))
    print()

if __name__ == '__main__':
    main()
