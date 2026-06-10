import os

import pytest

from src.db.backend.file_db import FileDB


class TestFileDB:

    def setup_method(self):
        self.filename = "test_db.json"

        if os.path.exists(self.filename):
            os.remove(self.filename)

        self.db = FileDB(self.filename)

    def teardown_method(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_add_record_success(self):
        data = {"title": "1984", "author": "Orwell"}
        record_id = self.db.add_record(data)

        assert record_id == 1
        assert self.db.records[1] == data

    def test_add_record_with_invalid_data_type(self):
        with pytest.raises(TypeError, match="Данные должны быть словарем"):
            self.db.add_record("not a dict")

    def test_add_record_multiple_records(self):
        id1 = self.db.add_record({"title": "Book1"})
        id2 = self.db.add_record({"title": "Book2"})
        id3 = self.db.add_record({"title": "Book3"})

        assert id1 == 1
        assert id2 == 2
        assert id3 == 3
        assert len(self.db.records) == 3

    def test_get_all_records_empty(self):
        records = self.db.get_all_records()
        assert records == []

    def test_get_all_records_with_data(self):
        self.db.add_record({"title": "Book1"})
        self.db.add_record({"title": "Book2"})

        records = self.db.get_all_records()

        assert len(records) == 2
        assert records[0][0] == 1
        assert records[1][0] == 2

    def test_get_record_success(self):
        self.db.add_record({"title": "1984", "author": "Orwell"})

        record = self.db.get_record(1)

        assert record == {"title": "1984", "author": "Orwell"}

    def test_get_record_not_found(self):
        with pytest.raises(KeyError, match="Запись с ID 999 не найдена"):
            self.db.get_record(999)

    def test_filter_records_success_single_filter(self):
        self.db.add_record({"title": "1984", "author": "Orwell", "year": 1949})
        self.db.add_record({"title": "Brave New World", "author": "Huxley", "year": 1932})
        self.db.add_record({"title": "Animal Farm", "author": "Orwell", "year": 1945})

        result = self.db.filter_records({"author": "Orwell"})

        assert len(result) == 2

    def test_filter_records_success_multiple_filters(self):
        self.db.add_record({"title": "1984", "author": "Orwell", "year": 1949})
        self.db.add_record({"title": "Animal Farm", "author": "Orwell", "year": 1945})
        self.db.add_record({"title": "Brave New World", "author": "Huxley", "year": 1932})

        result = self.db.filter_records({"author": "Orwell", "year": 1945})

        assert len(result) == 1
        assert result[0][1]["title"] == "Animal Farm"

    def test_filter_records_no_match(self):
        self.db.add_record({"title": "1984", "author": "Orwell"})

        result = self.db.filter_records({"author": "Nonexistent"})

        assert result == []

    def test_filter_records_empty_filters(self):
        self.db.add_record({"title": "1984"})

        result = self.db.filter_records({})

        assert len(result) == 1

    def test_filter_records_invalid_filters_type(self):
        with pytest.raises(TypeError, match="Фильтры должны быть словарем"):
            self.db.filter_records("not a dict")

    def test_update_record_success(self):
        self.db.add_record({"title": "1984", "author": "Orwell"})

        updated = self.db.update_record(1, {"year": 1949})

        assert updated == {
            "title": "1984",
            "author": "Orwell",
            "year": 1949,
        }

    def test_update_record_not_found(self):
        with pytest.raises(KeyError, match="Запись с ID 999 не найдена"):
            self.db.update_record(999, {"year": 2000})

    def test_delete_record_success(self):
        self.db.add_record({"title": "1984"})

        deleted = self.db.delete_record(1)

        assert deleted == {"title": "1984"}
        assert 1 not in self.db.records
        assert len(self.db.records) == 0

    def test_delete_record_not_found(self):
        with pytest.raises(KeyError, match="Запись с ID 999 не найдена"):
            self.db.delete_record(999)

    def test_update_record_partial_update(self):
        self.db.add_record(
            {
                "title": "1984",
                "author": "Orwell",
                "year": 1949,
            }
        )

        self.db.update_record(1, {"year": 1950})

        record = self.db.get_record(1)

        assert record["title"] == "1984"
        assert record["author"] == "Orwell"
        assert record["year"] == 1950

    def test_filter_records_case_sensitive(self):
        self.db.add_record({"title": "1984", "author": "orwell"})
        self.db.add_record({"title": "Animal Farm", "author": "Orwell"})

        result = self.db.filter_records({"author": "Orwell"})

        assert len(result) == 1
        assert result[0][1]["title"] == "Animal Farm"

    def test_file_created_after_add(self):
        self.db.add_record({"title": "1984"})

        assert os.path.exists(self.filename)

    def test_data_persistence(self):
        self.db.add_record(
            {
                "title": "1984",
                "author": "Orwell",
            }
        )

        new_db = FileDB(self.filename)

        record = new_db.get_record(1)

        assert record["title"] == "1984"
        assert record["author"] == "Orwell"

  def test_load_invalid_json(self):
        with open(self.filename, "w", encoding="utf-8") as file:
            file.write("{ invalid json")

        db = FileDB(self.filename)

        assert db.records == {}
        assert db.next_id == 1
