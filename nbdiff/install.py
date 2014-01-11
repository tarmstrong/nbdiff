from __future__ import print_function
from . import __path__ as NBDIFF_PATH
import subprocess
import re
import os
import shutil
import sys


def install():
    profile_name = 'nbdiff'
    create_cmd = ['ipython', 'profile', 'create', profile_name]
    message = subprocess.Popen(create_cmd, stderr=subprocess.PIPE)
    message_str = message.stderr.read()
    re_msgline = \
        re.compile(r'^.ProfileCre.*u\'(?P<profilepath>.*)ipython_config\.py.$')
    profile_paths = [
        re_msgline.match(line).groups()[0]
        for line in message_str.splitlines()
        if re_msgline.match(line)
    ]
    if len(profile_paths) == 0:
        sys.stderr.write(
            "It looks like creating the ipython profile "
            "didn't work. Maybe you've already installed it?\n"
        )
        sys.exit(-1)

    profile_path = profile_paths[0]
    extension_copy_from = os.path.join(NBDIFF_PATH[0], 'extension/static')
    extension_copy_dest = os.path.join(profile_path, 'static')
    shutil.copytree(extension_copy_from, extension_copy_dest)
    print("Finished installing NBDiff extension in profile `nbdiff`.")
