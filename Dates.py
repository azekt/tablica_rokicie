import re
from GlobalServices import Log, Notify

class Dates:
    @staticmethod
    def find_date(sheet, col, from_row, max_offset, validator):
        """Wyszukuje pierwszą pasującą datę w arkuszu na podstawie walidatora."""
        to_row = max(1, from_row - max_offset)
        for row in range(from_row, to_row, -1):
            cell_value = sheet.cell(column=col, row=row).value
            if validator(cell_value):
                return cell_value

        """Nie znaleziono daty."""
        Notify.add('error', 'Dates | find_date', f"Date not found for col {col} row {row}")
        Log.add('error', 'Dates | find_date', f"Date not found for col {col} row {row}")
        return None

    @staticmethod
    def is_valid_wednesday(value):
        pattern = r"""
            ^(\d{1,2}-\d{1,2}|\d{1,2})   # Zakres dni (np. "6-12", "24")
            \s                           # Spacja
            \w+                          # Miesiąc (np. "STYCZNIA")
            (\s\d{4})?                   # Opcjonalny rok (np. "2025")
            (\sDO\s\d{1,2}               # Opcjonalne "DO X"
            (\s\w+)?                     # Opcjonalnie miesiąc po "DO"
            (\s\d{4})?)?                 # Opcjonalnie rok po "DO"
            (\s\|.*)?                    # Opcjonalnie "| PSALMY ..." lub inne teksty
            $
        """
        return bool(re.match(pattern, str(value).upper(), re.VERBOSE))

    @staticmethod
    def is_valid_sunday(value):
        pattern = r"""
            (^\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}$)|
            (^\d{1,2}\s\w+\s\d{4}(r\.)?)
        """
        return bool(re.match(pattern, str(value).upper(), re.VERBOSE))

    @staticmethod
    def is_valid_zbiorka(value):
        return True
