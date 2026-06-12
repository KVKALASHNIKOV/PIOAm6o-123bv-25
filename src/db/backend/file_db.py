import json
from pathlib import Path
from typing import Dict, Any

from .base import BaseDB
from .table import Table


class FileDB(Table, BaseDB):
    """Файловая база данных с хранением в JSON."""

    def __init__(self, filename: str = "library.json") -> None:
        super().__init__()
        self.filename = Path(filename)
        self._load()

    def _load(self) -> None:
        if not self.filename.exists():
            return

        try:
            with self.filename.open("r", encoding="utf-8") as file:
                data = json.load(file)

            self.schema = data.get(
                "schema",
                ["title", "author", "year", "genre"]
            )

            self.next_id = data.get("next_id", 1)

            self.records = {
                int(record_id): record
                for record_id, record
                in data.get("records", {}).items()
            }

        except (json.JSONDecodeError, OSError) as error:
            raise RuntimeError(
                f"Файл базы данных поврежден: {error}"
            )

    def _save(self) -> None:
        data = {
            "schema": self.schema,
            "next_id": self.next_id,
            "records": self.records,
        }

        try:
            with self.filename.open("w", encoding="utf-8") as file:
                json.dump(
                    data,
                    file,
                    ensure_ascii=False,
                    indent=4
                )

        except OSError as error:
            raise RuntimeError(
                f"Ошибка сохранения базы данных: {error}"
            )

    def add_record(self, data: Dict[str, Any]) -> int:
        record_id = super().add_record(data)
        self._save()
        return record_id

    def update_record(
        self,
        record_id: int,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:

        updated = super().update_record(
            record_id,
            data
        )

        self._save()
        return updated

    def delete_record(
        self,
        record_id: int
    ) -> Dict[str, Any]:

        deleted = super().delete_record(
            record_id
        )

        self._save()
        return deleted
