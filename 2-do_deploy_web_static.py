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

    try:
        put(archive_path, '/tmp/')
        archive_name = archive_path.split('/')[-1]
        dirN = archive_name.split('.')[0]
        release_path = '/data/web_static/releases/'

        run(f'sudo mkdir -p {release_path}{dirN}')
        run(f'sudo tar -xzf /tmp/{archive_name} -C {release_path}{dirN}/')
        run(f'sudo rm /tmp/{archive_name}')
        run(f'sudo mv {release_path}{dirN}/web_static/* {release_path}{dirN}/')
        run('sudo rm -rf /data/web_static/current')
        run(f'sudo ln -s {release_path}{dirN}/ /data/web_static/current')

        print('New version deployed!')
        return True

    except Exception as e:
        print(e)
        return False
