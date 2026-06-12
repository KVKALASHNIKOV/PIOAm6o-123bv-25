import os
from datetime import datetime
from typing import List, Tuple, Dict, Any


class TUI:

    def __init__(
        self,
        db: Any,
        clear_enabled: bool = True
    ) -> None:
        self.db = db
        self.clear_enabled = clear_enabled
        self.fields: List[str] = ["title", "author", "year", "genre"]

    def clear_screen(self) -> None:
        if not self.clear_enabled:
            return

        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self) -> None:
        print("=" * 50)

        db_name = self.db.__class__.__name__

        if db_name == "FileDB":
            print("FILE DATABASE: БИБЛИОТЕКА")
        else:
            print("IN-MEMORY DATABASE: БИБЛИОТЕКА")

        print("=" * 50)

    def print_menu(self) -> None:
        print("\nМЕНЮ:")
        print("1. Добавить книгу")
        print("2. Показать все книги")
        print("3. Найти книги")
        print("4. Обновить книгу")
        print("5. Удалить книгу")
        print("0. Выход")

    def print_records(self, records: List[Tuple[int, Dict[str, Any]]]) -> None:
        if not records:
            print("\nЗаписей не найдено")
            return

        print(f"\n{'ID':<5} {'Название':<30} {'Автор':<20} {'Год':<6} {'Жанр':<15}")
        print("-" * 80)

        for record_id, record in records:
            title = record.get('title', '')[:30]
            author = record.get('author', '')[:20]
            year = record.get('year', '')
            genre = record.get('genre', '')[:15]
            print(f"{record_id:<5} {title:<30} {author:<20} {year:<6} {genre:<15}")

    def get_book_data(
        self,
        current_data: Dict[str, Any] | None = None
    ) -> Dict[str, Any]:
        print("\nВведите данные книги:")

        data = {}

        title = input(
            f"Название [{current_data.get('title', '')}]: "
        ).strip() if current_data else input("Название: ").strip()

        if title:
            data["title"] = title
        elif current_data is None:
            raise ValueError("Название книги не может быть пустым")

        author = input(
            f"Автор [{current_data.get('author', '')}]: "
        ).strip() if current_data else input("Автор: ").strip()

        if author:
            data["author"] = author
        elif current_data is None:
            raise ValueError("Автор не может быть пустым")

        while True:
            prompt = (
                f"Год издания [{current_data.get('year', '')}]: "
                if current_data
                else "Год издания: "
            )

            year_input = input(prompt).strip()

            if not year_input:
                break

            try:
                year = int(year_input)

                current_year = datetime.now().year

                if year < 0 or year > current_year:
                    print(f"Ошибка: год должен быть от 0 до {current_year}")
                    continue

                data["year"] = year
                break

            except ValueError:
                print("Ошибка: год должен быть числом")

        genre = input(
            f"Жанр [{current_data.get('genre', '')}]: "
        ).strip() if current_data else input("Жанр: ").strip()

        if current_data:
            if genre:
                data["genre"] = genre
        else:
            data["genre"] = genre

        return data

    def get_filters(self) -> Dict[str, Any]:
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

    def add_record(self) -> None:
        try:
            data = self.get_book_data()
            record_id = self.db.add_record(data)
            print(f"\nКнига добавлена с ID: {record_id}")
        except ValueError as e:
            print(f"\nОшибка ввода: {e}")
        except Exception as e:
            print(f"\nОшибка при добавлении: {e}")

    def show_all(self) -> None:
        records = self.db.get_all_records()
        self.print_records(records)

    def filter_records(self) -> None:
        try:
            filters = self.get_filters()
            if not filters:
                print("Не задано ни одного фильтра")
                return
            records = self.db.filter_records(filters)
            self.print_records(records)
        except Exception as e:
            print(f"\nОшибка при поиске: {e}")

    def update_record(self) -> None:
        try:
            record_id_input = input("\nВведите ID книги для обновления: ").strip()
            if not record_id_input.isdigit():
                print("Ошибка: ID должен быть числом")
                return

            record_id = int(record_id_input)
            current = self.db.get_record(record_id)
            print(f"\nТекущие данные: {current}")

            data = self.get_book_data(current)

            if not data:
                print("\nИзменения не внесены")
                return

            updated = self.db.update_record(record_id, data)
            print(f"\nКнига обновлена: {updated}")
        except KeyError as e:
            print(f"\nОшибка: {e}")
        except ValueError as e:
            print(f"\nОшибка ввода: {e}")
        except Exception as e:
            print(f"\nОшибка при обновлении: {e}")

    def delete_record(self) -> None:
        try:
            record_id_input = input("\nВведите ID книги для удаления: ").strip()
            if not record_id_input.isdigit():
                print("Ошибка: ID должен быть числом")
                return

            record_id = int(record_id_input)
            deleted = self.db.delete_record(record_id)
            print(f"\nКнига удалена: {deleted}")
        except KeyError as e:
            print(f"\nОшибка: {e}")
        except Exception as e:
            print(f"\nОшибка при удалении: {e}")

    def run(self) -> None:
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
