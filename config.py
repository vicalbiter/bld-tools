import os

_ROOT = os.path.dirname(os.path.abspath(__file__))

cfg = {}
cfg["logs_path"] = os.path.join(_ROOT, "logs")