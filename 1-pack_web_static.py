#!/usr/bin/python3
"""generates a .tgz archive from the contents of the web_static"""
from fabric.api import local
from datetime import datetime


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
