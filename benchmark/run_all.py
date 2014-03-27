import git2json as g
import subprocess as s


BENCH_REPO = '/home/tavish/capstone/nbdiff/.git'
check_added = '1f52ff8b5acaa408948d7a73b07b9dd2554e863a'

HEAD = check_added

commits = g.parse_commits(g.run_git_log(extra_args=[HEAD + '..', '--']).read())
i = 0
for commit in commits:
    if i % 5 == 0:
        s.call(('git --git-dir=' + BENCH_REPO + ' checkout ' + commit).split())
        benchmark_output = s.check_output(['python', 'benchmark.py', commit])
        with open('results.csv', 'a') as out:
            out.write(benchmark_output)
    i += 1
