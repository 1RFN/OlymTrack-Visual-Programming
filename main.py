import sys
import os
from PySide6.QtWidgets import QApplication
from ui.main_window import OlymTrackMain
from logic.app_controller import AppController  
from database.db_handler import initialize_db

def main():
    initialize_db()
    app = QApplication(sys.argv)

    qss_path = os.path.join("assets", "style.qss")
    if os.path.exists(qss_path):
        with open(qss_path, "r") as f:
            app.setStyleSheet(f.read())
    else:
        print(f"Peringatan: File {qss_path} tidak ditemukan! Aplikasi berjalan tanpa styling.")

    window = OlymTrackMain()
    
    window.controller = AppController(window)

    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()