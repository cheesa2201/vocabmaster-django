#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

<<<<<<< HEAD
def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
=======

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vocabmaster.settings')
>>>>>>> fa8bf4865547a8d716a22e762087a632b9dc0d72
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

<<<<<<< HEAD
if __name__ == '__main__':
    main()
=======

if __name__ == '__main__':
    main()
>>>>>>> fa8bf4865547a8d716a22e762087a632b9dc0d72
