from . import __path__ as NBDIFF_PATH
import subprocess
import re
import os
import shutil


def install():
    profile_name = 'nbdiff'
    create_cmd = ['ipython', 'profile', 'create', profile_name]
    message = subprocess.Popen(create_cmd, stderr=subprocess.PIPE)
    message_str = message.stderr.read()
    re_msgline = \
        re.compile(r'^.ProfileCre.*u\'(?P<profilepath>.*)ipython_config\.py.$')
    profile_path = [
        re_msgline.match(line).groups()[0]
        for line in message_str.splitlines()
        if re_msgline.match(line)
    ][0]
    extension_copy_from = os.path.join(NBDIFF_PATH[0], 'extension/static')
    extension_copy_dest = os.path.join(profile_path, 'static')
    print extension_copy_from
    print extension_copy_dest
    shutil.copytree(extension_copy_from, extension_copy_dest)
    print profile_path
