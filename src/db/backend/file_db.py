import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from .base import BaseDB


class FileDB(BaseDB):
    """Файловая база данных с хранением в JSON."""
    
    def __init__(self, filename: str = "library.json") -> None:
        self.filename = Path(filename)
        self.records: Dict[int, Dict[str, Any]] = {}
        self.next_id: int = 1

        self._load()

    def _load(self) -> None:
        if not self.filename.exists():
            return

        try:
            with self.filename.open("r", encoding="utf-8") as file:
                data = json.load(file)

            self.next_id = data.get("next_id", 1)

            self.records = {
                int(record_id): record
                for record_id, record in data.get("records", {}).items()
            }

        except (json.JSONDecodeError, OSError):
            print("Ошибка загрузки файла, создана пустая база данных")
            self.records = {}
            self.next_id = 1

    def _save(self) -> None:
        data = {
            "next_id": self.next_id,
            "records": self.records,
        }

        with self.filename.open("w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4
            )

    def add_record(self, data: Dict[str, Any]) -> int:
        if not isinstance(data, dict):
            raise TypeError("Данные должны быть словарем")

        record_id = self.next_id
        self.records[record_id] = data.copy()
        self.next_id += 1

        self._save()

        return record_id

    def get_all_records(self) -> List[Tuple[int, Dict[str, Any]]]:
        return [
            (record_id, record.copy())
            for record_id, record in self.records.items()
        ]

    def get_record(self, record_id: int) -> Dict[str, Any]:
        if record_id not in self.records:
            raise KeyError(f"Запись с ID {record_id} не найдена")

        return self.records[record_id].copy()

    def filter_records(
        self,
        filters: Dict[str, Any]
    ) -> List[Tuple[int, Dict[str, Any]]]:
        if not isinstance(filters, dict):
            raise TypeError("Фильтры должны быть словарем")

        result = []

        for record_id, record in self.records.items():
            match = True

            for key, value in filters.items():
                if key not in record or record[key] != value:
                    match = False
                    break

            if match:
                result.append((record_id, record.copy()))

        return result

    def update_record(
        self,
        record_id: int,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        if record_id not in self.records:
            raise KeyError(f"Запись с ID {record_id} не найдена")

        if not isinstance(data, dict):
            raise TypeError("Данные должны быть словарем")

        self.records[record_id].update(data)

        self._save()

        return self.records[record_id].copy()

    def delete_record(self, record_id: int) -> Dict[str, Any]:
        if record_id not in self.records:
            raise KeyError(f"Запись с ID {record_id} не найдена")

        deleted = self.records.pop(record_id)

        self._save()

        return deleted.copy()
