from .backend.memory import InMemoryDB
from .tui import TUI

def main():
    try:
        db = InMemoryDB()
        ui = TUI(db)
        ui.run()
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем")
    except Exception as e:
        print(f"\nКритическая ошибка: {e}")

if __name__ == "__main__":
    main()