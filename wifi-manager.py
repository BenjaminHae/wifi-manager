#!/usr/bin/python3
from curses import wrapper
import curses
import csv

i = 0

def dataWidth(csv):
    return 50

def dataLength(csv):
    return 10

def dataShow(csv, add):
    global i
    i = i+1
    add(i,str(i))

def main(stdscr):
    # Clear screen
    stdscr.clear()

    csv = 0

    pad = curses.newpad(dataLength(0),dataWidth(0))
    pad.scrollok(True)
    dataShow(csv, lambda line, data: pad.addstr(line,0,data))
    pad.addstr(1,1,'blafnanf', curses.A_UNDERLINE)
    pad.refresh(0,0, 0,1, curses.LINES - 1, curses.COLS - 1)
    
    #stdscr.refresh()
    stdscr.getkey()

if __name__ =='__main__':
    wrapper(main)
