"""Shared file operations"""
import csv
import pickle
import zipfile
from pathlib import Path

class FileHandler:
    @staticmethod
    def save_csv(data: list, filename: str) -> None:
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

    @staticmethod
    def load_csv(filename: str) -> list:
        with open(filename, 'r') as f:
            return list(csv.DictReader(f))

    @staticmethod
    def save_pickle(data: object, filename: str) -> None:
        with open(filename, 'wb') as f:
            pickle.dump(data, f)

    @staticmethod
    def load_pickle(filename: str) -> object:
        with open(filename, 'rb') as f:
            return pickle.load(f)

    @staticmethod
    def create_zip(source: str, zipname: str) -> None:
        with zipfile.ZipFile(zipname, 'w') as zipf:
            zipf.write(source)

    @staticmethod
    def read_text(filename: str) -> str:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def save_text(content: str, filename: str) -> None:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)