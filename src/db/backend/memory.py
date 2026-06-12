from typing import Any, Dict, List, Tuple

from .base import BaseDB


class InMemoryDB(BaseDB):
    """База данных в оперативной памяти."""
    
    def __init__(self) -> None:
        self.records: Dict[int, Dict[str, Any]] = {}
        self.next_id: int = 1
        self.schema: List[str] = ["title", "author", "year", "genre"]

    def add_record(self, data: Dict[str, Any]) -> int:
        if not isinstance(data, dict):
            raise TypeError("Данные должны быть словарем")

        for key in data:
            if key not in self.schema:
                raise ValueError(
                    f"Поле {key} отсутствует в схеме"
                )

        record_id = self.next_id
        self.records[record_id] = data.copy()
        self.next_id += 1

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
        for key in filters:
            if key not in self.schema:
                raise ValueError(
                    f"Поле {key} отсутствует в схеме"
                )

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
        for key in data:
            if key not in self.schema:
                raise ValueError(
                    f"Поле {key} отсутствует в схеме"
                )

        self.records[record_id].update(data)

        return self.records[record_id].copy()

    def delete_record(self, record_id: int) -> Dict[str, Any]:
        if record_id not in self.records:
            raise KeyError(f"Запись с ID {record_id} не найдена")

        return self.records.pop(record_id).copy()
