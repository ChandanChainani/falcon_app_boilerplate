from glob import glob
from os.path import dirname
from re import sub as re_sub
from importlib import import_module

FOLDER_PATH = "resources/"

import falcon

app = falcon.App()

for module in glob(f"{FOLDER_PATH}**/routes.py", recursive=True):
    module_path = re_sub(".py$", "", module)
    module = import_module(module_path.replace("/", "."))

    routes = getattr(module, "urls", None)
    if routes:
        route_base = "/" + re_sub(f"^{FOLDER_PATH}", "", dirname(module_path))
        for route in routes:
            route_path = route_base + route['path']
            app.add_route(route_path, route['handler'])
