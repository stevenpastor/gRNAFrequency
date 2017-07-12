#!/usr/bin/env python

"""
Reads tsv line by line and filters by column value (int) above threshold.
"""


# Standard library imports.
import csv
import argparse


parser = argparse.ArgumentParser(description="Opens TSV and filters by column > n.")
parser.add_argument("-i", required=True, dest="infile", \
        help="Input tsv with column containing an int to filter.")
parser.add_argument("-n", required=True, dest="num", \
        help="Integer to filter rows by column.")
parser.add_argument("-c", required=True, dest="col", \
        help="Column to filter.")
parser.add_argument("-o", required=True, dest="outfile", \
        help="Output file containing filter rows.")
args = parser.parse_args()


def filter_tsv_greater(infile, n, col, outfile):
    """
    Opens TSV, reads line by line, filters > n.
    Outputs tsv with rows meeting filter criteria.
    """
    with open(infile, 'rb') as f:
        reader = csv.reader(f, delimiter='\t')
        filtered_rows = [line for line in reader if int(line[col-1]) > n]
    with open(outfile, 'wb') as out:
        writer = csv.writer(out, delimiter='\t', lineterminator="\n")
        writer.writerows(filtered_rows)

def main():
    filter_tsv_greater(args.infile, int(args.num), int(args.col), args.outfile)

if __name__=="__main__": main()
