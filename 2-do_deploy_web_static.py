#!/usr/bin/python3

"""
Invoke script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""

from invoke import task
from os.path import exists

@task
def do_deploy(c, archive_path):
    """Distributes an archive to the web servers"""
    if not exists(archive_path):
        return False

    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        
        # Upload the archive
        c.put(archive_path, "/tmp/")

        # Create the necessary directories and extract the archive
        c.run('mkdir -p {}{}/'.format(path, no_ext))
        c.run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))

        # Clean up
        c.run('rm /tmp/{}'.format(file_n))
        c.run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        c.run('rm -rf {}{}/web_static'.format(path, no_ext))
        c.run('rm -rf /data/web_static/current')
        c.run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))

        return True
    except Exception as e:
        print("Deployment failed:", str(e))
        return False

