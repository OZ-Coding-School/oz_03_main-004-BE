from unittest.mock import patch

from django.core.management import call_command
from django.test import SimpleTestCase


@patch("django.db.utils.ConnectionHandler.__getitem__")
class CommandsTests(SimpleTestCase):
    def test_wait_for_db_ready(self):
        patched_getitem.return_value = True

        call_command("wait_for_db")

    def test_wait_for_db_delay(self):
        pass
