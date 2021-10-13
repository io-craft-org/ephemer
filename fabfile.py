# encoding: utf-8

"""
Fabfile to drive development and deployment of ephemer

authors : raphael.marvie@beta.gouv.fr, guillaume.libersat@beta.gouv.fr
created : 2021-06-01 09:54:36 CEST
"""

import os
from distutils.core import run_setup

import pytest
from fabric import task

import ephemer

PACKAGE = f"ephemer-{ephemer.VERSION}.tar.gz"

# TODO make target folder being
# - prod if branch == main,
# - develop if branch == develop, and
# - error otherwise.


@task
def upgrade(cnx, site=None):
    """Upgrade requirements to last version on server for site"""
    if site not in ["production", "development"]:
        print("Usage: fab upgrade --site={production,development} --hosts=...")
        return
    cnx.put(
        "./requirements.txt",
        remote=f"./www/ephemer-{site}/requirements.txt",
    )
    cnx.run(
        f"cd www/ephemer-{site} " "&& env/bin/pip install --upgrade -r requirements.txt"
    )


@task
def deploy(cnx, site=None):
    """Deploy new version of project to server for site"""
    if site not in ["production", "development"]:
        print("Usage: fab deploy --site={production,development} --hosts=...")
        return
    run_setup("setup.py", script_args=["sdist"])
    cnx.put(
        f"./dist/{PACKAGE}",
        remote=f"./www/ephemer-{site}/dist/{PACKAGE}",
    )
    cnx.run(
        f"cd www/ephemer-{site} "
        f"&& ./env/bin/pip install ./dist/{PACKAGE}"
        "&& ./manage.py migrate"
        # "&& env/bin/python3 manage.py compilescss"
        "&& ./manage.py collectstatic --noinput"
    )


# eof
