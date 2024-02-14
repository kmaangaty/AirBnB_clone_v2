#!/usr/bin/python3
"""
Fabric script that generates a tgz archive from the contents of the web_static
folder of the AirBnB Clone repo
"""

from os.path import isdir
from datetime import datetime
from fabric.api import local


def do_pack():
    """do_pack"""
    try:
        d = datetime.now().strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            local("mkdir versions")
        fn = "versions/web_static_{}.tgz".format(d)
        local("tar -cvzf {} web_static".format(fn))
        return fn
    except:
        return None
