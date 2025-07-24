from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler
import logging
import os

class FileLogService:
    _instance = None  # Singleton
    allowed_types = ('debug', 'info', 'error')

    @staticmethod
    def _get_instance():
        if FileLogService._instance is None:
            FileLogService._instance = FileLogService()
        return FileLogService._instance

    def __init__(self, max_lines=500, backup_count=3):
        load_dotenv()
        log_file = f"{os.getenv('mainPath')}app.log"

        if not hasattr(self, 'log'):
            self.buffered_logs = []

        # Konfiguracja loggera z rotacją
        if not hasattr(self, 'logger'):
            self.logger = logging.getLogger('FileLogService')
            self.logger.setLevel(logging.DEBUG)

            # Obliczenie maksymalnego rozmiaru na podstawie linii (~100 bajtów na linię)
            max_bytes = max_lines * 100

            handler = RotatingFileHandler(
                log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
            )
            handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

            self.logger.addHandler(handler)

    @staticmethod
    def add(type: str, title: str, text: str):
        log_service = FileLogService._get_instance()

        if type not in log_service.allowed_types:
            raise ValueError(f"Only {log_service.allowed_types} types are allowed!")

        log_service.buffered_logs.append((type, f"{title} | {text}"))

    @staticmethod
    def save_logs():
        log_service = FileLogService._get_instance()
        # Zapis logów do pliku na koniec działania
        for log_type, log_message in log_service.buffered_logs:
            if log_type == 'error':
                log_service.logger.error(log_message)
            elif log_type == 'info':
                log_service.logger.info(log_message)
            elif log_type == 'debug':
                log_service.logger.debug(log_message)

        log_service.buffered_logs.clear()
