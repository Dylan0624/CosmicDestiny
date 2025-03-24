"""
Main application window
"""

import os
import sys
import logging
from datetime import datetime
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QTabWidget, 
                            QMessageBox, QFileDialog, QLabel)
from PyQt6.QtCore import Qt, QSettings
from PyQt6.QtGui import QIcon, QPixmap

from ui.input_tab import InputTab
from ui.result_tab import ResultTab
from ui.loading_overlay import LoadingOverlay
from analyzer import DestinyAnalyzer
from worker import AnalysisWorker
from config import APP_NAME, UI_WINDOW_WIDTH, UI_WINDOW_HEIGHT

class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        """Initialize the main window"""
        super().__init__()
        
        # Set up logging
        logging.basicConfig(level=logging.INFO, 
                           format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        
        # Initialize analyzer
        self.analyzer = DestinyAnalyzer()
        
        # Set up UI
        self.init_ui()
        
        # Connect signals
        self.connect_signals()
        
        # Load settings
        self.load_settings()
        
    def init_ui(self):
        """Initialize the user interface"""
        # Set window properties
        self.setWindowTitle(f"{APP_NAME} - 命理分析系統")
        self.setGeometry(100, 100, UI_WINDOW_WIDTH, UI_WINDOW_HEIGHT)
        self.setMinimumSize(800, 600)
        
        # Set application icon if available
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources', 'icon.png')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Add logo if available
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources', 'logo.png')
        if os.path.exists(logo_path):
            logo_label = QLabel()
            pixmap = QPixmap(logo_path)
            logo_label.setPixmap(pixmap.scaled(300, 100, Qt.AspectRatioMode.KeepAspectRatio))
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            main_layout.addWidget(logo_label)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Create input tab
        self.input_tab = InputTab()
        self.tab_widget.addTab(self.input_tab, "個人資料輸入")
        
        # Create result tab
        self.result_tab = ResultTab()
        self.tab_widget.addTab(self.result_tab, "命理分析結果")
        
        # Create loading overlay
        self.loading_overlay = LoadingOverlay(self)
        
    def connect_signals(self):
        """Connect UI signals to slots"""
        # Connect generate button to analysis function
        self.input_tab.generate_btn.clicked.connect(self.start_analysis)
        
        # Connect save button to save function
        self.result_tab.save_btn.clicked.connect(self.save_result)
        
    def start_analysis(self):
        """Start the analysis process in a separate thread"""
        # Validate input
        if not self.input_tab.chinese_name.text():
            QMessageBox.warning(self, "缺少資訊", "請輸入您的中文姓名")
            return
            
        # Collect user data
        user_data = self.input_tab.get_user_data()
        
        # Switch to results tab
        self.tab_widget.setCurrentIndex(1)
        
        # Show loading overlay
        self.loading_overlay.start_loading("正在生成命理分析結果，請稍候...")
        
        # Create worker thread for analysis
        self.worker = AnalysisWorker(self.analyzer, user_data)
        self.worker.analysis_complete.connect(self.on_analysis_complete)
        self.worker.analysis_error.connect(self.on_analysis_error)
        self.worker.start()
        
    def on_analysis_complete(self, result):
        """Handle the completion of analysis"""
        # Stop loading animation
        self.loading_overlay.stop_loading()
        
        # Set result text
        self.result_tab.set_result(result)
        
        # Log completion
        self.logger.info("Analysis completed successfully")
        
    def on_analysis_error(self, error_message):
        """Handle analysis errors"""
        # Stop loading animation
        self.loading_overlay.stop_loading()
        
        # Set error message
        self.result_tab.set_result(f"分析過程中發生錯誤：\n\n{error_message}\n\n請確認 Ollama 服務已啟動並載入相應模型。")
        
        # Log error
        self.logger.error(f"Analysis error: {error_message}")
        
    def save_result(self):
        """Save the analysis result to a file"""
        # Get current timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Get the name for the filename
        name = self.input_tab.chinese_name.text()
        if not name:
            name = "unnamed"
        
        # Default filename
        default_filename = f"{name}_命理分析_{timestamp}.txt"
        
        # Open file dialog
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(
            self, "儲存命理分析結果", default_filename,
            "Text Files (*.txt);;All Files (*)", options=options
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    # Write header
                    f.write(f"{APP_NAME} 命理分析報告\n")
                    f.write(f"生成日期：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("="*50 + "\n\n")
                    
                    # Write personal info
                    user_data = self.input_tab.get_user_data()
                    f.write("個人資料：\n")
                    f.write(f"- 姓名（中文）：{user_data['chinese_name']}\n")
                    f.write(f"- 姓名（英文）：{user_data['english_name']}\n")
                    f.write(f"- 性別：{user_data['gender']}\n")
                    f.write(f"- 生辰年月日：{user_data['birth_date']}\n")
                    f.write(f"- 出生時辰：{user_data['birth_time']}\n")
                    f.write(f"- 星座：{user_data['zodiac']}\n")
                    f.write(f"- 生肖：{user_data['chinese_zodiac']}\n")
                    f.write(f"- MBTI 人格：{user_data['mbti']}\n")
                    f.write(f"- 出生地：{user_data['birthplace']}\n\n")
                    
                    # Write analysis type
                    f.write(f"分析類型：{user_data['fortune_type']}\n")
                    f.write(f"分析重點：{user_data['focus_area']}\n\n")
                    
                    # Write life phases if selected
                    if user_data.get('life_phases'):
                        f.write("特別關注的人生階段：\n")
                        for phase in user_data['life_phases']:
                            f.write(f"- {phase}\n")
                        f.write("\n")
                    
                    # Write analysis result
                    f.write("命理分析結果：\n")
                    f.write("="*50 + "\n\n")
                    f.write(self.result_tab.result_text.toPlainText())
                    
                QMessageBox.information(self, "儲存成功", f"命理分析結果已成功儲存至：\n{filename}")
                
                # Save the directory for next time
                settings = QSettings(APP_NAME, APP_NAME)
                settings.setValue("last_save_directory", os.path.dirname(filename))
                
            except Exception as e:
                QMessageBox.critical(self, "儲存失敗", f"儲存命理分析結果時發生錯誤：\n{str(e)}")
                self.logger.error(f"Save error: {str(e)}")
    
    def load_settings(self):
        """Load application settings"""
        settings = QSettings(APP_NAME, APP_NAME)
        
        # Restore window geometry if available
        geometry = settings.value("window_geometry")
        if geometry:
            self.restoreGeometry(geometry)
    
    def closeEvent(self, event):
        """Handle window close event"""
        # Save window geometry
        settings = QSettings(APP_NAME, APP_NAME)
        settings.setValue("window_geometry", self.saveGeometry())
        
        # Accept the event
        event.accept()