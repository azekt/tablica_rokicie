import json
from DateUtils import DateUtils
from GlobalServices import Log, Notify
from typing import List, Tuple

class EventProcessor:
    def __init__(self, events_json):
        try:
            self.events = json.loads(events_json)
        except json.JSONDecodeError as e:
            Log.add('error', 'EventProcessor | process_events', f"Błąd parsowania JSON: {e}")
            raise

    def process_events(self, day_of_week: int):
        # Log.add('debug', 'EventProcessor | process_events', '---1---')
        result = []

        for event_str in self.events:
            timestamp, title = event_str.split(';')
            timestamp = DateUtils.timestamp_ms_to_s(timestamp)
            if (day_of_week != -1):
                dt = DateUtils.timestamp_to_datetime(timestamp)

            if (day_of_week == -1) or (dt.weekday() == day_of_week):
                result.append([timestamp, title])

        self.events = result

    def compare_events_and_tasks(self, tasks: list):
        # Log.add('debug', 'EventProcessor | compare_events_and_tasks', '---1---')
        return {
            "only_in_events": [item for item in self.events if item not in tasks],
            "only_in_tasks": [item for item in tasks if item not in self.events]
        }
