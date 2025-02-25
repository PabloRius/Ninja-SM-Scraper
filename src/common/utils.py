"""Common utils"""
from .config import DEBUG

def debug(what:str):
    """Debug printing"""
    if DEBUG:
        print(what)
