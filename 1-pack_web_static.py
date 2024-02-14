#!/usr/bin/python3
# Generates a .tgz archive from the contents of the web_static folder.
from fabric.api import local
from datetime import datetime
from os.path import isdir

"""
    Fabric script for creating a compressed archive (.tgz) from the contents
    of the web_static folder in the AirBnB Clone repository.
"""

def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.

    Returns:
        str: The archive path if successfully created, otherwise None.
    """
    try:
        # Get the current timestamp
        now = datetime.now()
        formatted_time = now.strftime("%Y%m%d%H%M%S")

        # Define the archive path
        archive_path = "versions/web_static_{}.tgz".format(formatted_time)

        # Check if 'versions' directory exists, create if not
        if not isdir("versions"):
            local("mkdir -p versions")

        # Create the .tgz archive
        local("tar -cvzf {} web_static".format(archive_path))

        # Return the archive path if successful
        return archive_path
    except Exception as e:
        # Print and handle any exceptions
        print("Error:", e)
        return None
