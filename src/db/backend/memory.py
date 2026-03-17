class InMemoryDB:
    def __init__(self):
        self.records = {}
        self.next_id = 1

    def add_record(self, data):
        if not isinstance(data, dict):
            raise TypeError("Данные должны быть словарем")
        record_id = self.next_id
        self.records[record_id] = data
        self.next_id += 1
        return record_id

    def get_all_records(self):
        return list(self.records.items())

    def filter_records(self, filters):
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
                result.append((record_id, record))
        return result

    def get_record(self, record_id):
        if record_id not in self.records:
            raise KeyError(f"Запись с ID {record_id} не найдена")
        return self.records[record_id]

    def update_record(self, record_id, data):
        if record_id not in self.records:
            raise KeyError(f"Запись с ID {record_id} не найдена")
        self.records[record_id].update(data)
        return self.records[record_id]

    def delete_record(self, record_id):
        if record_id not in self.records:
            raise KeyError(f"Запись с ID {record_id} не найдена")
        return self.records.pop(record_id)