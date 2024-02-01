#!/usr/bin/python3
"""distributes an archive to your web servers"""
from fabric.api import *
from datetime import datetime
import os


env.hosts = ['100.25.162.17', '100.25.131.228']
env.user = "ubuntu"


def do_pack():
    """returns .tgz archive"""

    local("mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    archive = f"versions/web_static_{date}.tgz"

    zip_arch = local(f"tar -cvzf {archive} web_static")
    if zip_arch.succeeded:
        return archive
    else:
        return None
    
def do_deploy(archive_path):
    """Distributes an archive to your web servers"""

    if os.path.exists(archive_path):    
        put(archive_path, '/tmp/')
        archive_name = archive_path.split('/')[-1]
        folder_name = archive_name.split('.')[0]
        release_path = '/data/web_static/releases/'

        run(f'mkdir -p {release_path}{folder_name}')
        run(f'tar -xzf /tmp/{archive_name} -C {release_path}{folder_name}/')
        run(f'rm /tmp/{archive_name}')
        run('rm -rf /data/web_static/current')
        run(f'ln -s {release_path}{folder_name}/ /data/web_static/current')

        print('New version deployed!')
        return True
    else:
        return False
