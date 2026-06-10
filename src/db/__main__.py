from .backend.memory import InMemoryDB
from .backend.file_db import FileDB
from .tui import TUI


def main() -> None:
    try:
        print("Выберите тип базы данных:")
        print("1. In-Memory")
        print("2. FileDB")

        choice = input("Ваш выбор: ").strip()

        if choice == "2":
            db = FileDB()
        else:
            db = InMemoryDB()

        ui = TUI(db)
        ui.run()

    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем")
    except Exception as e:
        print(f"\nКритическая ошибка: {e}")


if __name__ == "__main__":
    main()
