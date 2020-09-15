from os import listdir
from glob import glob
import fileinput
import sys

def ls(expr = '*.*'):
    return glob(expr)
buff_buscar = []
palabra="edu"
link = ls('*.txt')
for linea in fileinput.input(link):
    if palabra in linea:
        print(linea)