import subprocess
import timeit

def run_diff_once():
    f1 = 'example-notebooks/diff/0/before.ipynb'
    f2 = 'example-notebooks/diff/0/after.ipynb'

    subprocess.call(['nbdiff', '--check', f1, f2])


if __name__ == '__main__':
    t = timeit.Timer('run_diff_once()', setup='from __main__ import run_diff_once')
    print t.repeat(repeat=40, number=1)

