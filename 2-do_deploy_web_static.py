#!/usr/bin/env python3
"""
Invoke script that distributes an archive to your web servers
"""

from datetime import datetime
from invoke import task
import os

hosts = ["52.91.121.146", "3.85.136.181"]
user = "ubuntu"


@task
def do_pack(ctx):
    """
    Return the archive path if archive has generated correctly.
    """
    ctx.run("mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    archived_f_path = "versions/web_static_{}.tgz".format(date)
    t_gzip_archive = ctx.run("tar -cvzf {} web_static".format(archived_f_path))

    if t_gzip_archive.ok:
        return archived_f_path
    else:
        return None


@task
def do_deploy(ctx, archive_path):
    """
    Distribute archive.
    """
    if os.path.exists(archive_path):
        archived_file = archive_path[9:]
        newest_version = "/data/web_static/releases/" + archived_file[:-4]
        archived_file = "/tmp/" + archived_file
        ctx.run("sudo mkdir -p {}".format(newest_version))
        ctx.run("sudo tar -xzf {} -C {}/".format(archived_file, newest_version))
        ctx.run("sudo rm {}".format(archived_file))
        ctx.run("sudo mv {}/web_static/* {}".format(newest_version, newest_version))
        ctx.run("sudo rm -rf {}/web_static".format(newest_version))
        ctx.run("sudo rm -rf /data/web_static/current")
        ctx.run("sudo ln -s {} /data/web_static/current".format(newest_version))

        print("New version deployed!")
        return True

    else:
        print("Error: Archive not found at {}".format(archive_path))
        return False

# Uncomment the line below to test the deployment
# do_deploy(do_pack())

