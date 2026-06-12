import pytest

from src.db.backend.file_db import FileDB


@pytest.fixture
def db(tmp_path):
    filename = tmp_path / "test_db.json"
    return FileDB(filename)


class TestFileDB:

    def test_add_record_success(self, db):
        data = {"title": "1984", "author": "Orwell"}
        record_id = db.add_record(data)

        assert record_id == 1
        assert db.records[1] == data

    def test_add_record_with_invalid_data_type(self, db):
        with pytest.raises(TypeError, match="Данные должны быть словарем"):
            db.add_record("not a dict")

    def test_add_record_multiple_records(self, db):
        id1 = db.add_record({"title": "Book1"})
        id2 = db.add_record({"title": "Book2"})
        id3 = db.add_record({"title": "Book3"})

        assert id1 == 1
        assert id2 == 2
        assert id3 == 3
        assert len(db.records) == 3

    def test_get_all_records_empty(self, db):
        records = db.get_all_records()
        assert records == []

    def test_get_all_records_with_data(self, db):
        db.add_record({"title": "Book1"})
        db.add_record({"title": "Book2"})

        records = db.get_all_records()

        assert len(records) == 2
        assert records[0][0] == 1
        assert records[1][0] == 2

    def test_get_record_success(self, db):
        db.add_record({"title": "1984", "author": "Orwell"})

        record = db.get_record(1)

        assert record == {"title": "1984", "author": "Orwell"}

    def test_get_record_not_found(self, db):
        with pytest.raises(KeyError, match="Запись с ID 999 не найдена"):
            db.get_record(999)

    def test_filter_records_success_single_filter(self, db):
        db.add_record({"title": "1984", "author": "Orwell", "year": 1949})
        db.add_record({"title": "Brave New World", "author": "Huxley", "year": 1932})
        db.add_record({"title": "Animal Farm", "author": "Orwell", "year": 1945})

        result = db.filter_records({"author": "Orwell"})

        assert len(result) == 2

    def test_filter_records_success_multiple_filters(self, db):
        db.add_record({"title": "1984", "author": "Orwell", "year": 1949})
        db.add_record({"title": "Animal Farm", "author": "Orwell", "year": 1945})
        db.add_record({"title": "Brave New World", "author": "Huxley", "year": 1932})

        result = db.filter_records({"author": "Orwell", "year": 1945})

        assert len(result) == 1
        assert result[0][1]["title"] == "Animal Farm"

    def test_filter_records_no_match(self, db):
        db.add_record({"title": "1984", "author": "Orwell"})

        result = db.filter_records({"author": "Nonexistent"})

        assert result == []

    def test_filter_records_empty_filters(self, db):
        db.add_record({"title": "1984"})

        result = db.filter_records({})

        assert len(result) == 1

    def test_filter_records_invalid_filters_type(self, db):
        with pytest.raises(TypeError, match="Фильтры должны быть словарем"):
            db.filter_records("not a dict")

    def test_update_record_success(self, db):
        db.add_record({"title": "1984", "author": "Orwell"})

        updated = db.update_record(1, {"year": 1949})

        assert updated == {
            "title": "1984",
            "author": "Orwell",
            "year": 1949,
        }

    def test_update_record_not_found(self, db):
        with pytest.raises(KeyError, match="Запись с ID 999 не найдена"):
            db.update_record(999, {"year": 2000})

    def test_delete_record_success(self, db):
        db.add_record({"title": "1984"})

        deleted = db.delete_record(1)

        assert deleted == {"title": "1984"}
        assert 1 not in db.records
        assert len(db.records) == 0

    def test_delete_record_not_found(self, db):
        with pytest.raises(KeyError, match="Запись с ID 999 не найдена"):
            db.delete_record(999)

    def test_update_record_partial_update(self, db):
        db.add_record(
            {
                "title": "1984",
                "author": "Orwell",
                "year": 1949,
            }
        )

        db.update_record(1, {"year": 1950})

        record = db.get_record(1)

        assert record["title"] == "1984"
        assert record["author"] == "Orwell"
        assert record["year"] == 1950

    def test_filter_records_case_sensitive(self, db):
        db.add_record({"title": "1984", "author": "orwell"})
        db.add_record({"title": "Animal Farm", "author": "Orwell"})

        result = db.filter_records({"author": "Orwell"})

        assert len(result) == 1
        assert result[0][1]["title"] == "Animal Farm"

    def test_file_created_after_add(self, tmp_path):
        filename = tmp_path / "test_db.json"
        db = FileDB(filename)

        db.add_record({"title": "1984"})

        assert filename.exists()

    def test_data_persistence(self, tmp_path):
        filename = tmp_path / "test_db.json"
        db = FileDB(filename)

        db.add_record(
            {
                "title": "1984",
                "author": "Orwell",
            }
        )

        new_db = FileDB(filename)

        record = new_db.get_record(1)

        assert record["title"] == "1984"
        assert record["author"] == "Orwell"

    def test_load_invalid_json(self, tmp_path):
        filename = tmp_path / "test_db.json"

        with open(filename, "w", encoding="utf-8") as file:
            file.write("{ invalid json")

        with pytest.raises(RuntimeError):
            FileDB(filename)

    def test_update_persistence(self, tmp_path):
        filename = tmp_path / "test_db.json"
        db = FileDB(filename)

        db.add_record(
            {
                "title": "1984",
                "author": "Orwell",
            }
        )

        db.update_record(1, {"year": 1949})

        new_db = FileDB(filename)

        record = new_db.get_record(1)

        assert record["year"] == 1949

    def test_delete_persistence(self, tmp_path):
        filename = tmp_path / "test_db.json"
        db = FileDB(filename)

        db.add_record({"title": "1984"})

        db.delete_record(1)

        new_db = FileDB(filename)

        assert new_db.get_all_records() == []
