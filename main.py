import sys
import os
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from config import APP_NAME

def main():
    """Main application entry point"""
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    
    # Set stylesheet if exists
    style_path = os.path.join(os.path.dirname(__file__), 'ui', 'style.qss')
    if os.path.exists(style_path):
        with open(style_path, 'r', encoding='utf-8') as f:
            app.setStyleSheet(f.read())
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Run application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()