from django.test import SimpleTestCase
from unittest.mock import patch
from django.core.management import call_command

@patch('django.db.utils.ConnectionHandler.__getitem__')
class CommandsTests(SimpleTestCase):
    
    # DB가 준비되었을 때 wait_for_db 잘
    def test_wait_for_db_ready(self):
        patched_getitem.return_value = True
        
        call_command('wait_for_db')
    
    def test_wait_for_db_delay(self):
        pass
