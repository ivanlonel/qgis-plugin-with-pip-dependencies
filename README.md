# QGIS Minimalist Plugin Skeleton

Inspired by [this comment](https://github.com/qgis/QGIS-Enhancement-Proposals/issues/202#issuecomment-1997009497),
this simple QGIS plugin builds upon [wonder-sk/qgis-minimal-plugin](https://github.com/wonder-sk/qgis-minimal-plugin)
to serve as a proof of concept for installing python dependencies in runtime from QGIS plugins.
It installs [pip-install-test](https://pypi.org/project/pip-install-test/) when the plugin is first loaded.

## How to use it?

1. Create a new python plugin directory
    * e.g. Linux ```~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/minimal```
    * e.g. Windows ```C:\Users\USER\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\minimal```
    * e.g. macOS ```~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/minimal```
2. Copy ```metadata.txt```, ```requirements.txt```, ```minimal_plugin.py``` and ```__init__.py``` to that directory
3. Start QGIS and enable the plugin (menu Plugins > Manage and Install Plugins...)

Now you should see a "Go!" button in your "Plugins" toolbar (make sure it is enabled in menu Settings > Toolbars > Plugins).

Clicking the button shows a dialog with the path to ```pip-install-test```'s ```__init__.py``` file.
