#!/usr/bin/env python

"""
Reads tsv line by line and slides 100kb to count labels and retain
only n kb segments consisting of all 100kb windows >= 7 labels
(i.e., >= n*7 labels).

Example:
python filter_by_consecutive_labels.py -i hg38.counts.txt -n 5 -c 3 -o output.txt

n is number of 100kb windows.
c is column with labels (1-based).
"""


# Standard library imports.
import csv
import argparse
from itertools import islice


parser = argparse.ArgumentParser(description="Opens TSV and filters by >= 7 labels \
        across n 100kb windows.")
parser.add_argument("-i", required=True, dest="infile", \
        help="Input tsv with column containing labels over ranges to filter.")
parser.add_argument("-n", required=True, dest="num", \
        help="Integer value, number of sliding windows.")
parser.add_argument("-c", required=True, dest="col", \
        help="Column containing labels (1-based).")
parser.add_argument("-o", required=True, dest="outfile", \
        help="Output file containing filtered n 100kb segments.")
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

def filter_labels_hundred(infile, num, col, outfile):
    """
    Opens TSV, reads line by line, filters >= 7 labels
    per 100kb window (EACH >= 7 labels).
    Outputs tsv with rows meeting filter criteria.
    """
    with open(infile, 'rb') as f:
        reader = csv.reader(f, delimiter='\t')
        for line in sliding_window(reader, num):
            if all([int(row[col-1]) >= 7 for row in line]):
                with open(outfile, 'ab') as out:
                    writer = csv.writer(out, delimiter='\t', 
                                       lineterminator="\n")
                    writer.writerow(line)

def main():
    filter_labels_hundred(args.infile, int(args.num), int(args.col), args.outfile)

if __name__=="__main__": main()
