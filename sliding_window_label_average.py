#!/usr/bin/env python


from __future__ import division

"""
This script combines BioNano Genomics optical mapping and 
CRISPR-Cas9 labeling (in place of BspQI/BssSI/etc.).
Find megabase regions where average of 7 labels in 100kb windows for 
specified gRNA/Endonuclease.

Example input file:
1   0-100000    0
1   100000-200000   1
1   200000-300000   2
1   300000-400000   4

Column 1 is chromosome (int).
Column 2 is 100kb window.
Column 3 is frequency of label in corresponding window.

Currently running in Python 2.7.10

TODO:
-Testing.
-Improve formatting.

Current Issues:
-Many: specific input format.
-Does not handle headers in input (or any other formats).
-Col2 is explicitly handled as '-' delimited.

Example use:
python sliding_window_label_average.py -i <tsv_text>

Example output file:
Avg Start   End     chr range           count
7.2 800000  1800000 1   800000-900000   2 ...
"""

# Standard library imports.
from itertools import islice
import csv
import argparse

parser = argparse.ArgumentParser(description='Opens TSV frequency table and \
                                finds average over window of specified length.')
parser.add_argument("-i", required=True, dest="infile", 
                   help="Input file containing 3 columns: first is chromosome int, \
                   second is ranges (100kb), and third is frequency of labels in \
                   this 100kb window.")
parser.add_argument("-n", required=True, dest="num",
                   help="Sliding window size (int).")
parser.add_argument("-o", required=True, dest="outfile",
                   help="Output file containing mean labels across n region of 100 \
                   kb windows.")
args = parser.parse_args()

def sliding_window(seq, n):
    """
    Source:
    https://stackoverflow.com/questions/6822725/rolling-or-sliding-window-
    iterator-in-python

    "Returns a sliding window (of width n) over data from the iterable:
    s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ..."
    """
    iteration = iter(seq)
    result = tuple(islice(iteration, n))
    if len(result) == n:
        yield result
    for elem in iteration:
        result = result[1:] + (elem,)
        yield result

def find_mean_labels(infile, num, outfile):
    """
    Sliding window of n lines (n*100kb), finds average # labels above thresh.
    Average is across entire n length and threshold is based on this average.
    Output file: tsv with n*100kb segments >=7 label average.
    """
    with open(infile, 'rb') as f:
        reader = csv.reader(f, delimiter='\t')
        for line in sliding_window(reader, num): # num = num*100kb windows.
            labels = [int(col[2]) for col in line]
            label_avg = reduce(lambda x, y: x + y, labels) / len(labels)
            if label_avg >= 7.0:
                with open(outfile, "ab") as out:
                    writer = csv.writer(out, delimiter='\t', lineterminator="\n")
                    writer.writerow([label_avg] + [line[0][1].split('-')[0]] + 
                                   [line[9][1].split('-')[1]] + 
                                   [subrow for row in line for subrow in row])

def main():
    find_mean_labels(args.infile, int(args.num), args.outfile)

if __name__=="__main__": main()
