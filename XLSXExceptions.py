class XLSXError(Exception):
    """Bazowy wyjątek dla operacji XLSX"""
    pass

class XLSXFileNotFoundError(XLSXError):
    """Plik XLSX nie został znaleziony"""
    pass

class XLSXSheetNotFoundError(XLSXError):
    """Arkusz nie został znaleziony"""
    pass

class XLSXDataError(XLSXError):
    """Błąd w danych XLSX"""
    pass