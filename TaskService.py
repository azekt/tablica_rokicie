from GlobalServices import Log, Notify

class TaskService:
    @staticmethod
    def find_task_for_wednesday(sheet, row):
        # Log.add('debug', 'TaskService | find_task_for_wednesday', '---1---')
        cell = sheet.cell(column=9, row=row).value
        if cell:
            return cell
        cell = sheet.cell(column=3, row=row).value
        if cell:
            return cell
        return None

    @staticmethod
    def find_task_for_sunday(sheet, row):
        # Log.add('debug', 'TaskService | find_task_for_sunday', '---1---')
        cell = sheet.cell(column=2, row=row).value
        if cell:
            return cell
        return None

    @staticmethod
    def convert_task_name(key):
        # Log.add('debug', 'TaskService | convert_task_name', '---1---')
        conversion_map = {
            "audio/video": "Audio/Video",
            "lektor": "Lektor",
            "mikrofon 1 + scena": "Mikrofon",
            "mikrofon 2": "Mikrofon",
            "modlitwa": "Modlitwa",
            "pomocnik": "Pomocnik",
            "porządkowy (zoom)": "Porządkowy Zoom",
            "porządkowy (audytorium)": "Porządkowy sala",
            "porządkowy (wejście)": "Porządkowy wejście",
            "uczestnik": "Uczestnik"
        }

        orginal_key = key.strip().rstrip(':')
        key = orginal_key.lower()

        if key in conversion_map:
            return conversion_map[key]
        else:
            return "Punkt (" + orginal_key + ")"
            # raise ValueError(f"Nieznany klucz: {key}")

    @staticmethod
    def set_task_reminders(tasks: list, day_of_week):
        """Zwraca listę przypomnień dla zadań"""
        reminders = {
            6: {  # sunday
                'Audio/Video': [240, -540],
                'Lektor': [8100, 1740, -540],
                'Mikrofon': [240, -540],
                'Modlitwa': [240, -540],
                'Porządkowy Zoom': [240, -540],
                'Porządkowy sala': [240, -540],
                'Porządkowy wejście': [240, -540]
            },
            2: {  # wednesday
                'Audio/Video': [240, -900],
                'Lektor': [8100, 2340, -900],
                'Mikrofon': [240, -900],
                'Modlitwa': [240, -900],
                'Porządkowy Zoom': [240, -900],
                'Porządkowy sala': [240, -900],
                'Porządkowy wejście': [240, -900],
                'Uczestnik': [8100, -900]
            },
            -1: {  # zbiorka
                'Prowadzenie zbiórki zborowej': [8100, -840]
            }
        }

        for task in tasks:
            task.append(';'.join(map(
                str,
                reminders.get(day_of_week, {}).get(task[1], [8100, -900])  # default value
            )))
        return tasks
