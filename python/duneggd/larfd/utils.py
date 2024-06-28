import os
import sys

def resource_file_path(filename):
    """ Search for filename in the list of directories specified in the
    PYTHONPATH environment
    """
    pythonpath = os.environ.get("PYTHONPATH")
    if not pythonpath:
        pythonpath='./'

    for d in pythonpath.split(os.pathsep):
        filepath = os.path.join(d, filename)
        if os.path.isfile(filepath):
            return filepath

    return None
