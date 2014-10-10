'''
Entry points for the nbdiff package.
'''
from __future__ import print_function
import argparse
from .merge import notebook_merge
from .notebook_parser import NotebookParser
import sys
from .notebook_diff import notebook_diff
from .adapter.git_adapter import GitAdapter
from .adapter.hg_adapter import HgAdapter
from .adapter.vcs_adapter import NoVCSError
from .server.local_server import app
import threading
import webbrowser
import IPython.nbformat.current as nbformat
import IPython.nbformat.reader
try:
    NotJSONError = IPython.nbformat.current.NotJSONError
except AttributeError:
    NotJSONError = IPython.nbformat.reader.NotJSONError


def diff():
    description = '''
    Produce a diffed IPython Notebook from before and after notebooks.

    If no arguments are given, nbdiff looks for modified notebook files in
    the version control system.

    The resulting diff is presented to the user in the browser at
    http://localhost:5000.
    '''
    usage = 'nbdiff [-h] [--check] [--debug] ' +\
            '[--browser=<browser] [before after]'
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
    parser.add_argument(
        '--check',
        '-c',
        action='store_true',
        default=False,
        help='Run nbdiff algorithm but do not display the result.',
    )
    parser.add_argument(
        '--debug',
        '-d',
        action='store_true',
        default=False,
        help='Pass debug=True to the Flask server to ease debugging.',
    )
    parser.add_argument('before', nargs='?',
                        help='The notebook to diff against.')
    parser.add_argument('after', nargs='?',
                        help='The notebook to compare `before` to.')
    args = parser.parse_args()

    parser = NotebookParser()

    if args.before and args.after:
        invalid_notebooks = []

        try:
            notebook1 = parser.parse(open(args.before))
        except NotJSONError:
            invalid_notebooks.append(args.before)

        try:
            notebook2 = parser.parse(open(args.after))
        except NotJSONError:
            invalid_notebooks.append(args.after)

        if (len(invalid_notebooks) == 0):
            result = notebook_diff(notebook1, notebook2)

            filename_placeholder = "{} and {}".format(args.before, args.after)
            app.add_notebook(result, filename_placeholder)
            if not args.check:
                open_browser(args.browser)
                app.run(debug=args.debug)

        else:
            print('The notebooks could not be diffed.')
            print('There was a problem parsing the following notebook '
                  + 'files:\n' + '\n'.join(invalid_notebooks))
            return -1

    elif not (args.before or args.after):
        # No arguments have been given. Ask version control instead
        #  Try hg and git in this order.
        # The order is important because when GitAdapter fails, it sends an
        # annoying message to stdout, which is impossible to suppress.
        #  We don't want to see this message when we have a Hg repository.

        # Hg:
        try:
            vcs = HgAdapter()
        except NoVCSError as hg_err:
            # Git:
            #  use a nested try block to make sure the GitAdapter
            # is only created if the HgAdapter has failed.
            try:
                vcs = GitAdapter()
            except NoVCSError:
                #  Now we're sure we are not inside a supported repo.
                #  The GitAdapter error message has already been printed
                # and we print the HgAdapter error message
                print(hg_err.value)
                sys.exit(-1)

        modified_notebooks = vcs.get_modified_notebooks()

        if not len(modified_notebooks) == 0:
            invalid_notebooks = []
            for nbook in modified_notebooks:
                try:
                    filename = nbook[2]

                    current_notebook = parser.parse(nbook[0])
                    head_version = parser.parse(nbook[1])

                    result = notebook_diff(head_version, current_notebook)
                    app.add_notebook(result, filename)

                except NotJSONError:
                    invalid_notebooks.append(filename)

            if (len(invalid_notebooks) > 0):
                print('There was a problem parsing the following notebook '
                      + 'files:\n' + '\n'.join(invalid_notebooks))

            if (len(modified_notebooks) == len(invalid_notebooks)):
                print("There are no valid notebooks to diff.")
                return -1

            if not args.check:
                open_browser(args.browser)
                app.run(debug=False)
        else:
            print("No modified files to diff.")
            return 0
    else:
        print ("Invalid number of arguments. Run nbdiff --help")
        return -1


def merge():
    description = '''
    nbmerge is a tool for resolving merge conflicts in IPython Notebook
    files.

    If no arguments are given, nbmerge attempts to find the conflicting
    file in the version control system.

    Positional arguments are available for integration with version
    control systems such as Git and Mercurial.
    '''
    usage = (
        'nbmerge [-h] [--check] [--debug] [--browser=<browser>]'
        '[local base remote [result]]'
    )
    parser = argparse.ArgumentParser(
        description=description,
        usage=usage,
    )
    parser.add_argument('notebook', nargs='*')
    # TODO share this code with diff()
    parser.add_argument(
        '--check',
        '-c',
        action='store_true',
        default=False,
        help='Run nbmerge algorithm but do not display the result.',
    )
    parser.add_argument(
        '--debug',
        '-d',
        action='store_true',
        default=False,
        help='Pass debug=True to the Flask server to ease debugging.',
    )
    parser.add_argument(
        '--browser',
        '-b',
        default=None,
        help='Browser to launch nbdiff/nbmerge in',
    )
    args = parser.parse_args()
    length = len(args.notebook)
    parser = NotebookParser()
    valid_notebooks = False

    # only 'nbmerge' - no files specified with command
    if length == 0:
        try:
            vcs = HgAdapter()
        except NoVCSError as hg_err:
            # Git:
            #  use a nested try block to make sure the GitAdapter
            # is only created if the HgAdapter has failed.
            try:
                vcs = GitAdapter()
            except NoVCSError:
                #  Now we're sure we are not inside a supported repo.
                #  The GitAdapter error message has already been printed
                # and we print the HgAdapter error message
                print(hg_err.value)
                sys.exit(-1)

        unmerged_notebooks = vcs.get_unmerged_notebooks()

        if not len(unmerged_notebooks) == 0:
            invalid_notebooks = []

            for nbook in unmerged_notebooks:
                try:
                    filename = nbook[3]

                    nb_local = parser.parse(nbook[0])
                    nb_base = parser.parse(nbook[1])
                    nb_remote = parser.parse(nbook[2])

                    pre_merged_notebook = notebook_merge(nb_local,
                                                         nb_base, nb_remote)
                    app.add_notebook(pre_merged_notebook, filename)

                except NotJSONError:
                    invalid_notebooks.append(filename)

            if (len(invalid_notebooks) > 0):
                print('There was a problem parsing the following notebook '
                      + 'files:\n' + '\n'.join(invalid_notebooks))

            if (len(unmerged_notebooks) == len(invalid_notebooks)):
                print("There are no valid notebooks to merge.")
                return -1
            else:
                valid_notebooks = True

        else:
            print('There are no files to be merged.')
            return -1

    # files specified with nbmerge command
    elif length == 3 or length == 4:
        invalid_notebooks = []

        if length == 3:
            # hg usage:
            # $ hg merge -t nbmerge <branch>

            # Mercurial gives three arguments:
            # 1. Local / Result (the file in your working directory)
            # 2. Base
            # 3. Remote
            filename = args.notebook[0]  # filename for saving

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
            filename = args.notebook[3]   # filename for saving

        try:
            nb_local = parser.parse(open(args.notebook[0]))
        except NotJSONError:
            invalid_notebooks.append(args.notebook[0])

        try:
            nb_base = parser.parse(open(args.notebook[1]))
        except NotJSONError:
            invalid_notebooks.append(args.notebook[1])

        try:
            nb_remote = parser.parse(open(args.notebook[2]))
        except NotJSONError:
            invalid_notebooks.append(args.notebook[2])

        # local, base and remote are all valid notebooks
        if (len(invalid_notebooks) == 0):
            pre_merged_notebook = notebook_merge(nb_local, nb_base, nb_remote)
            app.add_notebook(pre_merged_notebook, filename)
            valid_notebooks = True

        elif (len(invalid_notebooks) > 0):
                print('There was a problem parsing the following notebook '
                      + 'files:\n' + '\n'.join(invalid_notebooks))
                print("There are no valid notebooks to merge.")
                return -1

    else:
        sys.stderr.write('Incorrect number of arguments. Quitting.\n')
        sys.exit(-1)

    def save_notebook(notebook_result, filename):
        parsed = nbformat.reads(notebook_result, 'json')
        with open(filename, 'w') as targetfile:
            nbformat.write(parsed, targetfile, 'ipynb')

    if (valid_notebooks):
        if not args.check:
            app.shutdown_callback(save_notebook)
            open_browser(args.browser)
            app.run(debug=args.debug)


def open_browser(browser_exe):
    try:
        browser = webbrowser.get(browser_exe)
    except webbrowser.Error:
        browser = None
    if browser:
        b = lambda: browser.open("http://127.0.0.1:5000/0", new=2)
        threading.Thread(target=b).start()
