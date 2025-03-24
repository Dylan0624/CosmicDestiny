#!/usr/bin/env python3
"""
CosmicDestiny - 全方位人生命理分析系統
Main application entry point
"""

import sys
import os
import logging
from PyQt6.QtWidgets import QApplication
from cosmic_destiny.ui.main_window import MainWindow
from cosmic_destiny.config import APP_NAME

def setup_logging():
    """Configure application logging"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("cosmic_destiny.log", encoding="utf-8")
        ]
    )

def main():
    """Main application entry point"""
    # Setup logging
    setup_logging()
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    
    # Set stylesheet if exists
    style_path = os.path.join(os.path.dirname(__file__), "cosmic_destiny", "ui", "style.qss")
    if os.path.exists(style_path):
        with open(style_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Run application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

