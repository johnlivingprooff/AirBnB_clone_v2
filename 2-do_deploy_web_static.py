#!/usr/bin/python3
"""Distribution module"""
from fabric.api import *
import os
env.hosts = ['100.25.162.17', '100.25.131.228']
env.user = "ubuntu"


def do_deploy(archive_path):
    """Distributes an archive to your web servers"""

    if not os.path.exists(archive_path):
        return False

    with warn_only():
        err = put(archive_path, '/tmp/')
        if err.failed:
            return False
        archive_name = os.path.basename(archive_path)
        dirN = os.path.splitext(archive_name)[0]
        release_path = f'/data/web_static/releases/{dirN}'

        err = run(f'mkdir -p {release_path}{dirN}')
        if err.failed:
            return False
        err = run(f'tar -xzf /tmp/{archive_name} -C {release_path}/')
        if err.failed:
            return False
        err = run(f'rm /tmp/{archive_name}')
        if err.failed:
            return False
        err = run(f'mv {release_path}/web_static/* {release_path}/')
        if err.failed:
            return False
        err = run(f'rm -rf {release_path}/web_static')
        if err.failed:
            return False
        err = run('rm -rf /data/web_static/current')
        if err.failed:
            return False
        err = run(f'ln -s {release_path}/ /data/web_static/current')
        if err.failed:
            return False

    return True
