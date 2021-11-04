from glob import glob
from re import sub as re_sub
from importlib import import_module

FOLDER_PATH = "resources/"

import falcon
app = falcon.App()

for module in glob(f"{FOLDER_PATH}**/*.py", recursive=True):
    module_path = re_sub("(.py)$", "", module)
    module = import_module(module_path.replace("/", "."))

    resource = getattr(module, "resource_instance", None)
    if resource:
        route_path = "/" + re_sub(f"^{FOLDER_PATH}", "", re_sub("(/index)$", "", module_path))
        app.add_route(route_path, resource)

