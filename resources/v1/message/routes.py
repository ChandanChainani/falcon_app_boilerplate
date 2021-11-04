from .index import Index
from .show import Show

urls = [
    {
        "path": "",
        "handler": Index(),
    },
    {
        "path": "/{message_id:int(min=1)}",
        "handler": Show(),
    },
]
