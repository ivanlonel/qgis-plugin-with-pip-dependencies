# -----------------------------------------------------------
# Copyright (C) 2015 Martin Dobias
# -----------------------------------------------------------
# Licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# ---------------------------------------------------------------------

import subprocess
from pathlib import Path


def setup_user_site() -> tuple[str, Path, dict[str, str]]:
    import os
    import sys

    from qgis.core import QgsApplication
    from qgis.PyQt.QtCore import QStandardPaths

    python = QStandardPaths.findExecutable("python")

    env = os.environ.copy()
    env.setdefault(
        "PYTHONUSERBASE",
        str(Path(QgsApplication.qgisSettingsDirPath()) / "python"),
    )

    # get exact location of the usersite (for the current QGIS interpreter version)
    site_packages = Path(
        subprocess.run(
            (python, "-m", "site", "--user-site"),
            env=env,
            shell=True,
            capture_output=True,
            check=True,
        )
        .stdout.decode()
        .split()[0]
    )

    # raise exception if it's not a subpath
    site_packages.relative_to(env["PYTHONUSERBASE"])

    # set the priority to our custom user site
    site_packages.mkdir(parents=True, exist_ok=True)
    sys.path.insert(1, str(site_packages))

    return python, site_packages, env


def install_dependencies(python: str, site_packages: Path, env: dict[str, str]) -> None:
    from configparser import ConfigParser

    plugin_dir = Path(__file__).parent

    requirements_txt = plugin_dir / "requirements.txt"
    if not requirements_txt.is_file():
        return

    config = ConfigParser(allow_no_value=True)
    config.read(plugin_dir / "metadata.txt")
    metadata = dict(config["general"])

    log_file = site_packages.parent / f"{metadata['name']}.log"
    with log_file.open("a") as output:
        subprocess.run(
            (python, "-m", "pip", "install", "--user", "-r", str(requirements_txt)),
            env=env,
            shell=True,
            stdout=output,
            stderr=subprocess.STDOUT,
            check=True,
        )


def classFactory(iface):
    context = setup_user_site()

    try:
        from .minimal_plugin import MinimalPlugin
    except ImportError:
        install_dependencies(*context)
        from .minimal_plugin import MinimalPlugin

    return MinimalPlugin(iface)
