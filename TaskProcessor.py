from DateUtils import DateUtils
from Dates import Dates
from ExcelService import ExcelService
from GlobalServices import Log, Notify
from TaskService import TaskService

class TaskProcessor:
    def __init__(self, file, user, col, max_row, date_col, max_offset, validator, parse_date_func=DateUtils.parse_date, task_func=None, task_default=None, reminder=None):
        self.excel = ExcelService(file);
        self.user = user
        self.col = col
        self.max_row = max_row
        self.date_col = date_col
        self.max_offset = max_offset
        self.validator = validator
        self.parse_date_func = parse_date_func
        self.task_func = task_func
        self.task_default = task_default
        self.reminder = reminder

    def process_schedule(self):
        result = []
        for month in DateUtils.get_next_three_months():
            try:
                Log.add('debug', 'TaskProcessor | process_schedule', '---1---')
                Log.add('debug', 'TaskProcessor | process_schedule', f"Szukanie w arkuszu '{month}':")
                sheet = self.excel.get_sheet(month)
                if sheet is not None:
                    found = self.excel.find_user_in_sheet(sheet, self.user, self.col, self.max_row)
                    if found:
                        for find in found:
                            date = Dates.find_date(sheet, self.date_col, find[2], self.max_offset, self.validator)
                            timestamp = self.parse_date_func(date)
                            task = TaskService.convert_task_name(self.task_func(sheet, find[2])) if self.task_func else self.task_default
                            result.append([timestamp, task])
                    else:
                        Log.add('debug', 'TaskProcessor | process_schedule', 'Nie znaleziono w arkuszu')
            except ValueError as e:
                Log.add('error', 'TaskProcessor | process_schedule', e)
                raise
        self.tasks = result
        return result
