import os

class TUI:
    def __init__(self, db):
        self.db = db
        self.fields = ["title", "author", "year", "genre"]

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        print("=" * 50)
        print("IN-MEMORY DATABASE: БИБЛИОТЕКА")
        print("=" * 50)

    def print_menu(self):
        print("\nМЕНЮ:")
        print("1. Добавить книгу")
        print("2. Показать все книги")
        print("3. Найти книги")
        print("4. Обновить книгу")
        print("5. Удалить книгу")
        print("0. Выход")

    def print_records(self, records):
        if not records:
            print("\nЗаписей не найдено")
            return
        
        print(f"\n{'ID':<5} {'Название':<30} {'Автор':<20} {'Год':<6} {'Жанр':<15}")
        print("-" * 80)
        
        for record_id, record in records:
            print(f"{record_id:<5} {record.get('title', ''):<30} {record.get('author', ''):<20} "
                  f"{record.get('year', ''):<6} {record.get('genre', ''):<15}")

    def get_book_data(self):
        data = {}
        print("\nВведите данные книги:")
        data['title'] = input("Название: ").strip()
        data['author'] = input("Автор: ").strip()
        
        while True:
            try:
                year = input("Год издания: ").strip()
                if year:
                    data['year'] = int(year)
                break
            except ValueError:
                print("Ошибка: год должен быть числом")
        
        data['genre'] = input("Жанр: ").strip()
        return data

    def get_filters(self):
        filters = {}
        print("\nВведите критерии поиска (оставьте пустым для пропуска):")
        
        for field in self.fields:
            value = input(f"{field}: ").strip()
            if value:
                if field == "year":
                    try:
                        filters[field] = int(value)
                    except ValueError:
                        print(f"Ошибка: {field} должен быть числом, пропускаем фильтр")
                else:
                    filters[field] = value
        return filters

    def add_record(self):
        try:
            data = self.get_book_data()
            record_id = self.db.add_record(data)
            print(f"\nКнига добавлена с ID: {record_id}")
        except Exception as e:
            print(f"\nОшибка при добавлении: {e}")

    def show_all(self):
        records = self.db.get_all_records()
        self.print_records(records)

    def filter_records(self):
        try:
            filters = self.get_filters()
            if not filters:
                print("Не задано ни одного фильтра")
                return
            records = self.db.filter_records(filters)
            self.print_records(records)
        except Exception as e:
            print(f"\nОшибка при поиске: {e}")

    def update_record(self):
        try:
            record_id = input("\nВведите ID книги для обновления: ").strip()
            if not record_id.isdigit():
                print("Ошибка: ID должен быть числом")
                return
            
            record_id = int(record_id)
            current = self.db.get_record(record_id)
            print(f"\nТекущие данные: {current}")
            
            data = self.get_book_data()
            updated = self.db.update_record(record_id, data)
            print(f"\nКнига обновлена: {updated}")
        except KeyError as e:
            print(f"\nОшибка: {e}")
        except Exception as e:
            print(f"\nОшибка при обновлении: {e}")

    def delete_record(self):
        try:
            record_id = input("\nВведите ID книги для удаления: ").strip()
            if not record_id.isdigit():
                print("Ошибка: ID должен быть числом")
                return
            
            record_id = int(record_id)
            deleted = self.db.delete_record(record_id)
            print(f"\nКнига удалена: {deleted}")
        except KeyError as e:
            print(f"\nОшибка: {e}")
        except Exception as e:
            print(f"\nОшибка при удалении: {e}")

    def run(self):
        while True:
            self.clear_screen()
            self.print_header()
            self.print_menu()
            
            choice = input("\nВыберите действие: ").strip()
            
            if choice == '1':
                self.add_record()
            elif choice == '2':
                self.show_all()
            elif choice == '3':
                self.filter_records()
            elif choice == '4':
                self.update_record()
            elif choice == '5':
                self.delete_record()
            elif choice == '0':
                print("\nДо свидания!")
                break
            else:
                print("\nНеверный выбор. Попробуйте снова.")
            
            input("\nНажмите Enter для продолжения...")