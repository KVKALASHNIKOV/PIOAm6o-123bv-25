from .backend.file_db import FileDB
from .tui import TUI


def main() -> None:
    """Run the main application."""
    try:
        db = FileDB()
        ui = TUI(db)
        ui.run()
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем")
    except Exception as e:
        print(f"\nКритическая ошибка: {e}")


if __name__ == "__main__":
    main()
