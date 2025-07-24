import re
from datetime import datetime, timedelta, timezone
from GlobalServices import Log, Notify

class DateUtils:
    MONTHS_PL = [
        "styczeń", "luty", "marzec", "kwiecień", "maj", "czerwiec",
        "lipiec", "sierpień", "wrzesień", "październik", "listopad", "grudzień"
    ]

    MONTHS_PL_MAP = {
        "STYCZNIA": 1, "LUTEGO": 2, "MARCA": 3, "KWIETNIA": 4, "MAJA": 5, "CZERWCA": 6,
        "LIPCA": 7, "SIERPNIA": 8, "WRZEŚNIA": 9, "PAŹDZIERNIKA": 10, "LISTOPADA": 11, "GRUDNIA": 12
    }

    @staticmethod
    def get_next_three_months():
        """Zwraca listę poprzedniego, bieżącego i następnego miesiąca w formacie 'Miesiąc Rok'."""
        current_date = datetime.now()
        return [
            f"{DateUtils.MONTHS_PL[(current_date.month + i - 1) % 12]} {current_date.year + ((current_date.month + i - 1) // 12)}"
            for i in range(-1, 2)  # -1 to poprzedni, 0 to bieżący, 1 to następny
        ]

    @staticmethod
    def timestamp_to_datetime(timestamp: int) -> datetime:
        """Konwertuje znacznik czasu na obiekt datetime."""
        return datetime.fromtimestamp(timestamp, tz=timezone.utc)

    @staticmethod
    def string_to_timestamp(date_string: str) -> int:
        """Konwertuje ciąg znaków na znacznik czasu."""
        dt = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
        return int(dt.replace(tzinfo=timezone.utc).timestamp())

    @staticmethod
    def timestamp_ms_to_s(timestamp) -> int:
        return int(int(timestamp) / 1000)

    @staticmethod
    def parse_date(value, add_days: int = 0):
        """Parsuje datę z różnych formatów"""
        try:
            if isinstance(value, datetime):
                date_obj = value
            else:
                date_obj = datetime.strptime(value, "%Y-%m-%d")

            return int((date_obj.replace(tzinfo=timezone.utc) + timedelta(days=add_days)).timestamp())
        except (ValueError, TypeError):
            Notify.add('error', 'DateUtils | parse_date', f"Invalid date format: {value}")
            Log.add('error', 'DateUtils | parse_date', f"Invalid date format: {value}")
            return None

    @staticmethod
    def parse_date_offset(value, offset_days: int = 0):
        """Parsuje datę w formacie 'X MIESIĄC' i zwraca timestamp z przesunięciem."""
        match = re.match(r"^(\d{1,2})[-\s](?:\d{1,2}\s)?(\w+)(?:\s\d{4})?", value.upper())
        if not match:
            Notify.add('error', 'DateUtils | parse_date_offset', f"Invalid date format: {value}")
            Log.add('error', 'DateUtils | parse_date_offset', f"Invalid date format: {value}")
            return None

        day, month_str = match.groups()
        month = DateUtils.MONTHS_PL_MAP.get(month_str)
        if not month:
            Notify.add('error', 'DateUtils | parse_date_offset', f"Invalid month: {value}")
            Log.add('error', 'DateUtils | parse_date_offset', f"Invalid month: {value}")
            return None

        return DateUtils.calculate_date(int(day), month, offset_days)

    @staticmethod
    def calculate_date(day, month, offset_days=0):
        """Oblicza właściwy rok i konwertuje na timestamp."""
        current_date = datetime.now()
        year = current_date.year if month <= (current_date.month + 2) else current_date.year - 1

        try:
            return DateUtils.parse_date(datetime(year, month, day), add_days=offset_days)
        except ValueError:
            Notify.add('error', 'DateUtils | calculate_date', f"Invalid day, month: {day} {month}")
            Log.add('error', 'DateUtils | calculate_date', f"Invalid day, month: {day} {month}")
            return None

    @staticmethod
    def parse_date_wednesday(value):
        """Parsuje datę w formacie 'X MIESIĄC' i zwraca timestamp 2 dni później."""
        return DateUtils.parse_date_offset(value, offset_days=2)

    @staticmethod
    def parse_date_sunday(value):
        """Parsuje datę i zwraca timestamp dla niedzieli."""
        if isinstance(value, datetime):
            return DateUtils.parse_date(value)
        if isinstance(value, str):
            return DateUtils.parse_date_offset(value)

        Notify.add('error', 'DateUtils | parse_date_sunday', f"Invalid value: {value}")
        Log.add('error', 'DateUtils | parse_date_sunday', f"Invalid value: {value}")
        return None
