#!/usr/bin/env python3
"""A module for Fabric script that generates a .tgz archive."""
import os
from datetime import datetime
from invoke import task, run  # Change 'local' to 'run'

@task
def do_pack(context):
    """Archives the static files."""
    if not os.path.isdir("versions"):
        os.mkdir("versions")
    d_time = datetime.now()
    output = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        d_time.year,
        d_time.month,
        d_time.day,
        d_time.hour,
        d_time.minute,
        d_time.second
    )
    try:
        print("Packing web_static to {}".format(output))
        run("tar -cvzf {} web_static".format(output))
        size = os.stat(output).st_size
        print("web_static packed: {} -> {} Bytes".format(output, size))
    except Exception:
        output = None
    return output

