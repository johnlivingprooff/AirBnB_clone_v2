#!/usr/bin/python3
"""clean out old archives"""
from fabric.api import *
env.hosts = ['100.25.162.17', '100.25.131.228']


def do_clean(number=0):
    """
    Deletes out-of-date archives except for the most recent ones.
    Args: @number - number of archives not to delete
    """

    # server clean up
    vers_dir = "/data/web_static/releases/"
    with cd(vers_dir), hide('running', 'stdout'), hide('warnings'):
        ws_dirs = run('ls -tr').splitlines()

    to_keep = max(number, 1)
    to_del = ws_dirs[to_keep:]

    for dirs in to_del:
        run(f'rm -rf {vers_dir}{dirs}')

    # local clean up
    local_dirs = local('ls -tr versions/').splitlines()
    l_to_del = local_dirs[to_keep:]

    for l_dir in l_to_del:
        local(f'rm -fr versions/{l_dir}')
