"""
Loading overlay with animation
"""

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QMovie, QFont

class LoadingOverlay(QWidget):
    """Semi-transparent loading overlay with animation"""
    
    def __init__(self, parent=None):
        """
        Initialize the loading overlay
        
        Args:
            parent (QWidget): Parent widget to overlay
        """
        super().__init__(parent)
        
        # Set up widget properties
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 150);")
        
        # Hide by default
        self.hide()
        
        # Initialize UI elements
        self.init_ui()
    
    def init_ui(self):
        """Set up the user interface"""
        # Create layout
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Create label for the loading animation
        self.animation_label = QLabel()
        self.animation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Initialize animation
        try:
            from importlib.resources import files
            # Try to load the resource from the package
            animation_path = str(files('resources') / 'loading.gif')
        except (ImportError, ModuleNotFoundError):
            # Fallback to a relative path
            import os
            animation_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), 
                'resources', 'loading.gif'
            )
        
        # Create movie for animation
        self.movie = QMovie(animation_path)
        if not self.movie.isValid():
            # If no animation file found, use simple text animation
            self.movie = None
            self.animation_label.setText("處理中...")
            self.animation_label.setStyleSheet("color: white; font-size: 16pt;")
        else:
            self.movie.setScaledSize(QSize(100, 100))
            self.animation_label.setMovie(self.movie)
        
        layout.addWidget(self.animation_label)
        
        # Create label for loading text
        self.text_label = QLabel()
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        
        # Set font and style
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.text_label.setFont(font)
        self.text_label.setStyleSheet("color: white;")
        
        layout.addWidget(self.text_label)
        
        # Initialize animation dots
        self.dots_count = 0
        self.dots_timer = QTimer(self)
        self.dots_timer.timeout.connect(self.update_dots)
    
    def start_loading(self, text="處理中"):
        """
        Start the loading animation with the specified text
        
        Args:
            text (str): Text to display while loading
        """
        # Set text
        self.text_label.setText(text)
        
        # Start animation
        if self.movie:
            self.movie.start()
        else:
            # If no movie, start dots animation
            self.dots_timer.start(500)  # Update every 500ms
        
        # Update size and position
        self.resize(self.parent().size())
        
        # Show the overlay
        self.show()
        self.raise_()
    
    def stop_loading(self):
        """Stop the loading animation and hide the overlay"""
        # Stop animation
        if self.movie:
            self.movie.stop()
        else:
            self.dots_timer.stop()
        
        # Hide the overlay
        self.hide()
    
    def update_dots(self):
        """Update the dots animation"""
        self.dots_count = (self.dots_count + 1) % 4
        dots = "." * self.dots_count
        self.animation_label.setText(f"處理中{dots}")
    
    def resizeEvent(self, event):
        """Handle resize events to ensure the overlay covers the parent widget"""
        # Resize the overlay to match the parent size
        if self.parent():
            self.resize(self.parent().size())
        super().resizeEvent(event)