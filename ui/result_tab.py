"""
Result tab for displaying analysis results with Markdown support
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTextBrowser, QPushButton, 
                            QHBoxLayout, QLabel, QFontComboBox, QComboBox,
                            QSpinBox, QFileDialog)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QColor, QTextOption, QIcon
import os

class ResultTab(QWidget):
    """Tab for displaying analysis results with Markdown support"""
    
    def __init__(self):
        """Initialize the result tab"""
        super().__init__()
        
        # Initialize UI
        self.init_ui()
    
    def init_ui(self):
        """Set up the user interface"""
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Create title label
        title_label = QLabel("命理分析結果")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)
        
        # Create font control toolbar
        font_toolbar = QHBoxLayout()
        
        # Font family selection
        self.font_family = QFontComboBox()
        self.font_family.setCurrentFont(QFont("Microsoft JhengHei UI"))
        self.font_family.currentFontChanged.connect(self.update_text_format)
        font_toolbar.addWidget(QLabel("字體:"))
        font_toolbar.addWidget(self.font_family)
        
        # Font size selection
        self.font_size = QSpinBox()
        self.font_size.setRange(8, 24)
        self.font_size.setValue(13)
        self.font_size.valueChanged.connect(self.update_text_format)
        font_toolbar.addWidget(QLabel("大小:"))
        font_toolbar.addWidget(self.font_size)
        
        # Color scheme selection
        self.color_scheme = QComboBox()
        self.color_scheme.addItems(["淺色模式", "深色模式", "暖色調", "護眼模式"])
        self.color_scheme.currentIndexChanged.connect(self.update_color_scheme)
        font_toolbar.addWidget(QLabel("主題:"))
        font_toolbar.addWidget(self.color_scheme)
        
        font_toolbar.addStretch()
        main_layout.addLayout(font_toolbar)
        
        # Create result text area with Markdown support
        self.result_text = QTextBrowser()
        self.result_text.setOpenExternalLinks(True)
        self.result_text.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse | 
            Qt.TextInteractionFlag.TextSelectableByKeyboard |
            Qt.TextInteractionFlag.LinksAccessibleByMouse
        )
        
        # Set word wrap mode
        self.result_text.setWordWrapMode(QTextOption.WrapMode.WrapAtWordBoundaryOrAnywhere)
        
        # Set initial formatting
        self.update_text_format()
        self.update_color_scheme()
        
        main_layout.addWidget(self.result_text)
        
        # Create buttons layout
        buttons_layout = QHBoxLayout()
        
        # Create save button
        self.save_btn = QPushButton("儲存分析結果")
        self.save_btn.setMinimumHeight(40)
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #4caf50;
                color: white;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        buttons_layout.addWidget(self.save_btn)
        
        # Create copy button
        self.copy_btn = QPushButton("複製到剪貼簿")
        self.copy_btn.setMinimumHeight(40)
        self.copy_btn.clicked.connect(self.copy_result)
        self.copy_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
            QPushButton:pressed {
                background-color: #0a6ebd;
            }
        """)
        buttons_layout.addWidget(self.copy_btn)
        
        # Create print button
        self.print_btn = QPushButton("列印分析結果")
        self.print_btn.setMinimumHeight(40)
        self.print_btn.clicked.connect(self.print_result)
        self.print_btn.setStyleSheet("""
            QPushButton {
                background-color: #607d8b;
                color: white;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #546e7a;
            }
            QPushButton:pressed {
                background-color: #455a64;
            }
        """)
        buttons_layout.addWidget(self.print_btn)
        
        # Create export PDF button
        self.export_pdf_btn = QPushButton("匯出 PDF")
        self.export_pdf_btn.setMinimumHeight(40)
        self.export_pdf_btn.clicked.connect(self.export_pdf)
        self.export_pdf_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff5722;
                color: white;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #e64a19;
            }
            QPushButton:pressed {
                background-color: #d84315;
            }
        """)
        buttons_layout.addWidget(self.export_pdf_btn)
        
        # Add buttons layout to main layout
        main_layout.addLayout(buttons_layout)
    
    def set_result(self, text):
        """
        Set the result text with markdown formatting
        
        Args:
            text (str): The analysis result text
        """
        # Process markdown formatting
        processed_text = self.process_markdown(text)
        
        # Set HTML content
        self.result_text.setHtml(processed_text)
    
    def process_markdown(self, text):
        """
        Convert markdown text to HTML for display
        
        Args:
            text (str): Markdown text
            
        Returns:
            str: HTML formatted text
        """
        # Simple markdown processing for headers, bold, italic, etc.
        lines = text.split('\n')
        html_lines = []
        
        in_list = False
        in_blockquote = False
        
        for line in lines:
            # Skip empty lines
            if not line.strip():
                if in_list:
                    html_lines.append("</ul>")
                    in_list = False
                if in_blockquote:
                    html_lines.append("</blockquote>")
                    in_blockquote = False
                html_lines.append("<p>&nbsp;</p>")
                continue
            
            # Headers
            if line.startswith('# '):
                line = f"<h1>{line[2:]}</h1>"
            elif line.startswith('## '):
                line = f"<h2>{line[3:]}</h2>"
            elif line.startswith('### '):
                line = f"<h3>{line[4:]}</h3>"
            elif line.startswith('#### '):
                line = f"<h4>{line[5:]}</h4>"
            elif line.startswith('##### '):
                line = f"<h5>{line[6:]}</h5>"
            elif line.startswith('###### '):
                line = f"<h6>{line[7:]}</h6>"
            
            # Lists
            elif line.strip().startswith('- '):
                if not in_list:
                    html_lines.append("<ul>")
                    in_list = True
                line = f"<li>{line.strip()[2:]}</li>"
            
            # Blockquotes
            elif line.strip().startswith('>'):
                if not in_blockquote:
                    html_lines.append("<blockquote>")
                    in_blockquote = True
                line = f"<p>{line.strip()[1:].strip()}</p>"
            
            # Close lists if next line is not a list item
            elif in_list:
                html_lines.append("</ul>")
                in_list = False
                
            # Close blockquotes if next line is not a blockquote
            elif in_blockquote:
                html_lines.append("</blockquote>")
                in_blockquote = False
                
            # Regular paragraph
            else:
                line = f"<p>{line}</p>"
            
            # Bold (**text**)
            line = line.replace('**', '<strong>', 1)
            while '**' in line:
                line = line.replace('**', '</strong>', 1)
            
            # Italic (*text*)
            line = line.replace('*', '<em>', 1)
            while '*' in line:
                line = line.replace('*', '</em>', 1)
            
            # Horizontal rule
            if line.strip() == '---':
                line = '<hr />'
            
            html_lines.append(line)
        
        # Close any open lists
        if in_list:
            html_lines.append("</ul>")
        
        # Close any open blockquotes
        if in_blockquote:
            html_lines.append("</blockquote>")
        
        # Combine all HTML lines
        html = '<div style="line-height: 1.5;">' + '\n'.join(html_lines) + '</div>'
        
        return html
    
    def update_text_format(self):
        """Update the text format based on selected font settings"""
        font = self.font_family.currentFont()
        font.setPointSize(self.font_size.value())
        self.result_text.setFont(font)
    
    def update_color_scheme(self):
        """Update the color scheme based on selected theme"""
        scheme = self.color_scheme.currentText()
        
        if scheme == "深色模式":
            self.result_text.setStyleSheet("""
                QTextBrowser {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                    border: 1px solid #444;
                    border-radius: 5px;
                    padding: 15px;
                    selection-background-color: #4a7dff;
                    selection-color: white;
                }
                QTextBrowser h1, QTextBrowser h2, QTextBrowser h3, 
                QTextBrowser h4, QTextBrowser h5, QTextBrowser h6 {
                    color: #bb86fc;
                }
                QTextBrowser a {
                    color: #03dac6;
                }
                QTextBrowser blockquote {
                    background-color: #3d3d3d;
                    border-left: 4px solid #bb86fc;
                    padding: 10px;
                    margin: 10px 0;
                }
            """)
        elif scheme == "暖色調":
            self.result_text.setStyleSheet("""
                QTextBrowser {
                    background-color: #fff8e1;
                    color: #5d4037;
                    border: 1px solid #e0e0e0;
                    border-radius: 5px;
                    padding: 15px;
                    selection-background-color: #ffb74d;
                    selection-color: #5d4037;
                }
                QTextBrowser h1, QTextBrowser h2, QTextBrowser h3, 
                QTextBrowser h4, QTextBrowser h5, QTextBrowser h6 {
                    color: #ff7043;
                }
                QTextBrowser a {
                    color: #ff5722;
                }
                QTextBrowser blockquote {
                    background-color: #ffecb3;
                    border-left: 4px solid #ff9800;
                    padding: 10px;
                    margin: 10px 0;
                }
            """)
        elif scheme == "護眼模式":
            self.result_text.setStyleSheet("""
                QTextBrowser {
                    background-color: #f0f7e6;
                    color: #2e7d32;
                    border: 1px solid #c5e1a5;
                    border-radius: 5px;
                    padding: 15px;
                    selection-background-color: #aed581;
                    selection-color: #33691e;
                }
                QTextBrowser h1, QTextBrowser h2, QTextBrowser h3, 
                QTextBrowser h4, QTextBrowser h5, QTextBrowser h6 {
                    color: #388e3c;
                }
                QTextBrowser a {
                    color: #1b5e20;
                }
                QTextBrowser blockquote {
                    background-color: #dcedc8;
                    border-left: 4px solid #8bc34a;
                    padding: 10px;
                    margin: 10px 0;
                }
            """)
        else:  # 淺色模式 (default)
            self.result_text.setStyleSheet("""
                QTextBrowser {
                    background-color: #ffffff;
                    color: #212121;
                    border: 1px solid #e0e0e0;
                    border-radius: 5px;
                    padding: 15px;
                    selection-background-color: #4a7dff;
                    selection-color: white;
                }
                QTextBrowser h1, QTextBrowser h2, QTextBrowser h3, 
                QTextBrowser h4, QTextBrowser h5, QTextBrowser h6 {
                    color: #1976d2;
                }
                QTextBrowser a {
                    color: #0277bd;
                }
                QTextBrowser blockquote {
                    background-color: #f5f5f5;
                    border-left: 4px solid #1976d2;
                    padding: 10px;
                    margin: 10px 0;
                }
            """)
    
    def copy_result(self):
        """Copy the result text to clipboard"""
        self.result_text.selectAll()
        self.result_text.copy()
        # Deselect text
        cursor = self.result_text.textCursor()
        cursor.clearSelection()
        self.result_text.setTextCursor(cursor)
    
    def print_result(self):
        """Print the analysis result"""
        from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
        
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        dialog = QPrintDialog(printer, self)
        
        if dialog.exec() == QPrintDialog.DialogCode.Accepted:
            self.result_text.print_(printer)
    
    def export_pdf(self):
        """Export the analysis result as PDF"""
        from PyQt6.QtPrintSupport import QPrinter
        from PyQt6.QtCore import QDateTime
        
        # Get the filename
        timestamp = QDateTime.currentDateTime().toString('yyyyMMdd_hhmmss')
        default_filename = f"命理分析_{timestamp}.pdf"
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "匯出為 PDF", default_filename, "PDF Files (*.pdf)"
        )
        
        if filename:
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(filename)
            self.result_text.print_(printer)