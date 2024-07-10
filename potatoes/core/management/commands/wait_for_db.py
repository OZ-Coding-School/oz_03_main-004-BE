# wait_for_db => django가 db가 준비될 때까지 연결을 재시도하게 해주기 위해 필요
# => 하나의 도커 이미지에 각 컨테이너(app, db)가 존재하기 때문

from django.core.management.base import BaseCommand
from django.db import connections # db와 연결을 시도
import time

from django.db.utils import OperationalError
from psycopg2 import OperationalError as Psycopg2OperationalError

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Waiting for DB connection ... ')
        
        is_db_connected = None
        
        while not is_db_connected:
            try:
                is_db_connected = connections['default']
            except(OperationalError, Psycopg2OperationalError):
                self.stdout.write("Retry DB Connection ... ")
                time.sleep(1)
                
        self.stdout.write(self.style.SUCCESS('Success to PostgreSQL connection'))
        
        