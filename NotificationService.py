from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler
import logging
import os

class NotificationService:
    _instance = None  # Singleton
    allowed_types = ('debug', 'info', 'error')

    @staticmethod
    def _get_instance():
        if NotificationService._instance is None:
            NotificationService._instance = NotificationService()
        return NotificationService._instance

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(NotificationService, cls).__new__(cls)
        return cls._instance

    def __init__(self, max_lines=500, backup_count=3):
        load_dotenv()
        log_file = f"{os.getenv('mainPath')}notification.log"

        if not hasattr(self, 'log'):
            self.buffered_logs = []
            self.buffer = []

        # Konfiguracja loggera z rotacją
        if not hasattr(self, 'logger'):
            self.logger = logging.getLogger('NotificationService')
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
        notification_service = NotificationService._get_instance()

        if type not in notification_service.allowed_types:
            raise ValueError(f"Only {notification_service.allowed_types} types are allowed!")

        notification_service.buffer.append({'type': type, 'title': title, 'text': text})
        notification_service.buffered_logs.append((type, f"{title} | {text}"))

    def get_notifies():
        notification_service = NotificationService._get_instance()
        return notification_service.buffer

    def save_logs():
        notification_service = NotificationService._get_instance()
        # Zapis logów do pliku na koniec działania
        for log_type, log_message in notification_service.buffered_logs:
            if log_type == 'error':
                notification_service.logger.error(log_message)
            elif log_type == 'info':
                notification_service.logger.info(log_message)
            elif log_type == 'debug':
                notification_service.logger.debug(log_message)

        notification_service.buffered_logs.clear()
