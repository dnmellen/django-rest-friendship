# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from importlib import import_module


def import_from_string(val, setting_name):
    """
    Attempt to import a class from a string representation.

    From https://github.com/encode/django-rest-framework/blob/master/rest_framework/settings.py
    """
    try:
        # Nod to tastypie's use of importlib.
        parts = val.split('.')
        module_path, class_name = '.'.join(parts[:-1]), parts[-1]
        module = import_module(module_path)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        msg = "Could not import '%s' for API setting '%s'. %s: %s." % (val, setting_name, e.__class__.__name__, e)
        raise ImportError(msg)
