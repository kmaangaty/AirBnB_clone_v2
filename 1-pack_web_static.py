#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents
of the web_static folder of your AirBnB Clone repo
"""

from fabric.api import local
from datetime import datetime
import os

def do_pack():
    """
    Create a compressed archive from the contents of web_static folder
    """
    # Create the versions directory if it doesn't exist
    local("mkdir -p versions")

    # Generate the name of the archive
    archive_name = "web_static_" + datetime.utcnow().strftime("%Y%m%d%H%M%S") + ".tgz"

    # Create the archive using tar
    tar_command = "tar -cvzf versions/{} web_static".format(archive_name)
    result = local(tar_command, capture=True)

    if result.failed:
        return None
    else:
        archive_path = os.path.join("versions", archive_name)
        print("web_static packed: {} -> {}Bytes".format(archive_path, os.path.getsize(archive_path)))
        return archive_path
