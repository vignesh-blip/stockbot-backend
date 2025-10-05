# wsgi.py — robust loader that works no matter the working directory
import os, sys, importlib.util

BASE = os.path.dirname(__file__)
MAIN_FILE = os.path.join(BASE, "main.py")

# Ensure both repo root and /main are importable (harmless if not used)
sys.path.insert(0, BASE)
sys.path.insert(0, os.path.join(BASE, "main"))

# Load main.py by absolute file path
spec = importlib.util.spec_from_file_location("main_module", MAIN_FILE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

# Expose the Flask app for Gunicorn
app = getattr(mod, "app", None)
if app is None and hasattr(mod, "create_app"):
    app = mod.create_app()
if app is None:
    raise RuntimeError("Neither `app` nor `create_app()` found in main.py")

