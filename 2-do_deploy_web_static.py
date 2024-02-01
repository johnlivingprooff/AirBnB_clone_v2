#!/usr/bin/python3
"""combines do_pack() with do_deply()"""
from fabric.api import *
import os
env.hosts = ['100.25.162.17', '100.25.131.228']
env.user = "ubuntu"


def do_deploy(archive_path):
    """Distributes an archive to your web servers"""

    if not os.path.exists(archive_path):
        return False


    b = put(archive_path, '/tmp/')
    if b.failed:
        return False
    archive_name = os.path.basename(archive_path)
    dirN = os.path.splitext(archive_name)[0]
    release_path = f'/data/web_static/releases/{dirN}'

    b = run(f'mkdir -p {release_path}{dirN}')
    if b.failed:
        return False
    b = run(f'tar -xzf /tmp/{archive_name} -C {release_path}/')
    if b.failed:
        return False
    b = run(f'rm /tmp/{archive_name}')
    if b.failed:
        return False
    b = run(f'mv {release_path}/web_static/* {release_path}/')
    if b.failed:
        return False
    b = run(f'rm -rf {release_path}/web_static')
    if b.failed:
        return False
    b = run('rm -rf /data/web_static/current')
    if b.failed:
        return False
    b = run(f'ln -s {release_path}/ /data/web_static/current')
    if b.failed:
        return False

    print('New version deployed!')
    return True
