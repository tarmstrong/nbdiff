'''
Entry points for the nbdiff package.
'''
from __future__ import print_function
import argparse
from .merge import notebook_merge
from .notebook_parser import NotebookParser
import json
import sys
from .notebook_diff import notebook_diff
from .adapter.git_adapter import GitAdapter
from .server.local_server import app
import threading
import webbrowser
import IPython.nbformat.current as nbformat


def diff():
    description = '''
    Produce a diffed IPython Notebook from before and after notebooks.

    If no arguments are given, nbdiff looks for modified notebook files in
    the version control system.

    The resulting diff is presented to the user in the browser at
    http://localhost:5000.
    '''
    usage = 'nbdiff [-h] [--browser=<browser] [before after]'
    parser = argparse.ArgumentParser(
        description=description,
        usage=usage,
    )
    # TODO share this code with merge()
    parser.add_argument(
        '--browser',
        '-b',
        default=None,
        help='Browser to launch nbdiff/nbmerge in',
    )
    parser.add_argument('before', nargs='?',
                        help='The notebook to diff against.')
    parser.add_argument('after', nargs='?',
                        help='The notebook to compare `before` to.')
    args = parser.parse_args()

    parser = NotebookParser()

    if args.before and args.after:
        notebook1 = parser.parse(open(args.before))
        notebook2 = parser.parse(open(args.after))

        result = notebook_diff(notebook1, notebook2)

    elif not (args.before or args.after):
        # No arguments have been given. Ask version control instead
        git = GitAdapter()

        modified_notebooks = git.get_modified_notebooks()

        if not len(modified_notebooks) == 0:
            current_notebook = parser.parse(modified_notebooks[0][0])
            head_version = parser.parse(modified_notebooks[0][1])

            result = notebook_diff(head_version, current_notebook)
        else:
            print("No modified files to diff.")
            return 0
    else:
        print ("Invalid number of arguments. Run nbdiff --help")
        return -1

    app.add_notebook(result)
    open_browser(args.browser)
    app.run(debug=False)


def merge():
    description = '''
    nbmerge is a tool for resolving merge conflicts in IPython Notebook
    files.

    If no arguments are given, nbmerge attempts to find the conflicting
    file in the version control system.

    Positional arguments are available for integration with version
    control systems such as Git and Mercurial.
    '''
    usage = 'nbmerge [-h] [--browser=<browser>] [local base remote [result]]'
    parser = argparse.ArgumentParser(
        description=description,
        usage=usage,
    )
    parser.add_argument('notebook', nargs='*')
    # TODO share this code with diff()
    parser.add_argument(
        '--browser',
        '-b',
        default=None,
        help='Browser to launch nbdiff/nbmerge in',
    )
    args = parser.parse_args()
    length = len(args.notebook)
    parser = NotebookParser()

    if length == 0:
        git = GitAdapter()

        unmerged_notebooks = git.get_unmerged_notebooks()

        if not len(unmerged_notebooks) == 0:
            nb_local = parser.parse(unmerged_notebooks[0][0])
            nb_base = parser.parse(unmerged_notebooks[0][1])
            nb_remote = parser.parse(unmerged_notebooks[0][2])

            filename = unmerged_notebooks[0][3]
        else:
            print("No unmerged files to diff.")
            return 0

    elif length == 3 or length == 4:
        nb_local = parser.parse(open(args.notebook[0]))
        nb_base = parser.parse(open(args.notebook[1]))
        nb_remote = parser.parse(open(args.notebook[2]))
    else:
        sys.stderr.write('Incorrect number of arguments. Quitting.\n')
        sys.exit(-1)

    pre_merged_notebook = notebook_merge(nb_local, nb_base, nb_remote)
    if length == 3:
        # TODO ignore non-.ipynb files.

        # hg usage:
        # $ hg merge -t nbmerge <branch>

        # Mercurial gives three arguments:
        # 1. Local / Result (the file in your working directory)
        # 2. Base
        # 3. Remote
        with open(args.notebook[0], 'w') as resultfile:
            resultfile.write(json.dumps(pre_merged_notebook, indent=2))
    elif length == 4:
        # You need to run this before git mergetool will accept nbmerge
        # $ git config mergetool.nbmerge.cmd \
        #        "nbmerge \$LOCAL \$BASE \$REMOTE \$MERGED"
        # and then you can invoke it with:
        # $ git mergetool -t nbmerge
        #
        # Git gives four arguments (these are configurable):
        # 1. Local
        # 2. Base
        # 3. Remote
        # 4. Result (the file in your working directory)
        with open(args.notebook[3], 'w') as resultfile:
            resultfile.write(json.dumps(pre_merged_notebook, indent=2))
    else:
        app.add_notebook(pre_merged_notebook)

        def save_notebook(notebook_result):
            parsed = nbformat.reads(notebook_result, 'json')
            with open(filename, 'w') as targetfile:
                nbformat.write(parsed, targetfile, 'ipynb')

        app.shutdown_callback(save_notebook)
        open_browser(args.browser)
        app.run(debug=False)


def open_browser(browser_exe):
    try:
        browser = webbrowser.get(browser_exe)
    except webbrowser.Error:
        browser = None
    if browser:
        b = lambda: browser.open("http://127.0.0.1:5000", new=2)
        threading.Thread(target=b).start()
