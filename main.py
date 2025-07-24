import json
import sys
from DateUtils import DateUtils
from Dates import Dates
from EventProcessor import EventProcessor
from GlobalServices import Log, Notify
from TaskProcessor import TaskProcessor
from TaskService import TaskService

class MainProcessor:
    def switch_function(self, action, events):
        tasks = []
        file_params = {
            'check_sunday': {
                'file': '[...REACTED...]',
                'user': '[...REACTED...]',
                'col': 3,
                'max_row': 100,
                'date_col': 2,
                'max_offset': 15,
                'validator': Dates.is_valid_sunday,
                'parse_date_func': DateUtils.parse_date_sunday,
                'task_func': TaskService.find_task_for_sunday,
                'day_of_week': 6
            },
            'check_wednesday': {
                'file': '[...REACTED...]',
                'user': '[...REACTED...]',
                'col': 10,
                'max_row': 200,
                'date_col': 2,
                'max_offset': 35,
                'validator': Dates.is_valid_wednesday,
                'parse_date_func': DateUtils.parse_date_wednesday,
                'task_func': TaskService.find_task_for_wednesday,
                'day_of_week': 2
            },
            'check_zbiorki': {
                'file': '[...REACTED...]',
                'user': '[...REACTED...]',
                'col': 5,
                'max_row': 20,
                'date_col': 1,
                'max_offset': 1,
                'validator': Dates.is_valid_zbiorka,
                'parse_date_func': DateUtils.parse_date,
                'task_func': None,
                'task_default': '[...REACTED...]',
                'day_of_week': -1
            }
        }

        if action in file_params:
            params = file_params[action]
            task_processor = TaskProcessor(
                file = params['file'],
                user = params['user'],
                col = params['col'],
                max_row = params['max_row'],
                date_col = params['date_col'],
                max_offset = params['max_offset'],
                validator = params['validator'],
                parse_date_func = params['parse_date_func'],
                task_func = params.get('task_func'),
                task_default = params.get('task_default')
            )
            tasks = task_processor.process_schedule()
        else:
            Notify.add('error', 'Error', "I don't know what you actually want from me 🤷🏻‍♂️.")
            notify = Notify.get_notifies()
            print(json.dumps({'notify': notify, "only_in_events": [], "only_in_tasks": []}))
            return

        event_processor = EventProcessor(events)
        event_processor.process_events(file_params[action]['day_of_week'])

        # print(json.dumps(processor.events))

        result = event_processor.compare_events_and_tasks(tasks)
        result['only_in_tasks'] = TaskService.set_task_reminders(result['only_in_tasks'], params.get('day_of_week'))

        Notify.add('info', 'Info', f"Znaleziono {len(result['only_in_tasks'])} wydarzeń / nia do dodania")
        notify = Notify.get_notifies()

        print(json.dumps({'notify': notify, **result, 'tasks': tasks, 'events': event_processor.events}))

if __name__ == "__main__":
    if len(sys.argv) == 3:
        try:
            Log.add('debug', '---------- | START', '----------')
            action = sys.argv[1]
            params = sys.argv[2]
            Log.add('debug', 'Action', action)
            Log.add('debug', 'Params', params)
            processor = MainProcessor()
            processor.switch_function(action, params)
            Log.add('debug', '----------- | END', '-----------')
        except Exception as e:
            Log.add('debug', 'Main', f"main | Error: {e}")
            raise

        Log.save_logs()
        Notify.save_logs()
