# !/usr/bin/env python
import os
import sys


def main():  
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
    # add bellow lines (10–12)
    if os.environ.get("RUN_MAIN") == "1":
        import debugpy
        debugpy.listen(("0.0.0.0", 3000))
        print("Waiting for debugger attach...")
        debugpy.wait_for_client()

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
