#!/usr/bin/python3
"""
Fabric script that distributes an archive to web servers
"""

from datetime import datetime
from fabric.api import env, put, run, local
import os

env.user = 'ubuntu'
env.hosts = ['100.27.0.247', '100.26.162.119']


def do_pack():
    """
    Generate a .tgz archive from web_static

    Returns:
        str: Archive path if generated successfully, None otherwise
    """
    try:
        d = datetime.now().strftime("%Y%m%d%H%M%S")
        if not os.path.exists("versions"):
            local("mkdir versions")
        fn = "versions/web_static_{}.tgz".format(d)
        local("tar -cvzf {} web_static".format(fn))
        return fn
    except ValueError:
        return None


def do_deploy(archive_path):
    """
    Distribute an archive to web servers

    Args:
        archive_path (str): Path to the archive file

    Returns:
        bool: True if deployment successful, False otherwise
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload archive
        put(archive_path, "/tmp/")
        # Extract archive to releases folder
        archive_filename = os.path.basename(archive_path)
        release_path = "/data/web_static/releases/{}".format(
            archive_filename[:-4])
        run("mkdir -p {}".format(release_path))
        run("tar -xzf /tmp/{} -C {}".format(archive_filename, release_path))
        # Move files out of web_static folder
        run("mv {}/web_static/* {}".format(release_path, release_path))
        # Remove unnecessary web_static folder
        run("rm -rf {}/web_static".format(release_path))
        # Remove previous symbolic link
        run("rm -rf /data/web_static/current")
        # Create new symbolic link
        run("ln -s {} /data/web_static/current".format(release_path))
        print("New version deployed!")
        return True
    except ValueError:
        return False
