"""Data serialization for forest analysis"""
from utils.file_io import FileHandler

class ForestSerializer:
    @staticmethod
    def save(data: list, filename: str, format_type: str):
        if format_type.lower() == 'csv':
            FileHandler.save_csv(data, filename)
        elif format_type.lower() == 'pickle':
            FileHandler.save_pickle(data, filename)
        else:
            raise ValueError("Unsupported format. Use 'csv' or 'pickle'")

    @staticmethod
    def load(filename: str, format_type: str) -> list:
        if format_type.lower() == 'csv':
            return FileHandler.load_csv(filename)
        elif format_type.lower() == 'pickle':
            return FileHandler.load_pickle(filename)
        else:
            raise ValueError("Unsupported format. Use 'csv' or 'pickle'")