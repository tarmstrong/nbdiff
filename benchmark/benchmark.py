import subprocess
import timeit

def run_diff_once():
    f1 = 'example-notebooks/0/before.ipynb'
    f2 = 'example-notebooks/0/after.ipynb'

    subprocess.call(['nbdiff', '--check', f1, f2])

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('commit')
    args = parser.parse_args()
    t = timeit.Timer('run_diff_once()', setup='from __main__ import run_diff_once')
    measurements = t.repeat(repeat=40, number=1)
    import csv
    import sys
    import arrow
    row = [args.commit, arrow.now().timestamp] + measurements
    csv.writer(sys.stdout).writerow(row)

