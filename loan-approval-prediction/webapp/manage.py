#!/usr/bin/env python
"""Службовий файл Django: через нього запускаються всі команди (runserver, migrate тощо)."""
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "loan_site.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
