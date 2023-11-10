import argparse, os, re, sys
import pandas as pd
import numpy as np
from Bio import SeqIO

def import_homopolymers(seq_d, loci):
    l = []
    for locus in loci:
        s = str(seq_d[locus].seq)
        test = re.findall("(A{8,}|T{8,}|G{8,}|C{8,})",s)
        if len(test) > 0:
            l.append(True)
        else:
            l.append(False)
    return l
