"""
Input tab for user data collection
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QDateEdit, QComboBox, QPushButton, 
                            QGroupBox, QFormLayout, QRadioButton, QScrollArea,
                            QCheckBox, QGridLayout)
from PyQt6.QtCore import Qt, QDate
from config import (CHINESE_ZODIACS, WESTERN_ZODIACS, MBTI_TYPES, 
                  FORTUNE_TYPES, FOCUS_AREAS, LIFE_PHASES)

class InputTab(QWidget):
    """Tab for collecting user information"""
    
    def __init__(self):
        """Initialize the input tab"""
        super().__init__()
        
        # Initialize UI
        self.init_ui()
    
    def init_ui(self):
        """Set up the user interface"""
        # Main layout with scrollable area
        main_layout = QVBoxLayout(self)
        
        # Create scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)
        
        # Create scroll content widget
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(10, 10, 10, 10)
        scroll_layout.setSpacing(15)
        
        # Add form groups
        scroll_layout.addWidget(self.create_personal_info_group())
        scroll_layout.addWidget(self.create_fortune_type_group())
        scroll_layout.addWidget(self.create_life_phases_group())
        
        # Generate Button
        self.generate_btn = QPushButton("生成命理分析")
        self.generate_btn.setMinimumHeight(50)
        self.generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a7dff;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #3a6eee;
            }
            QPushButton:pressed {
                background-color: #2a5fdd;
            }
        """)
        scroll_layout.addWidget(self.generate_btn)
        
        # Set scroll area widget
        scroll_area.setWidget(scroll_content)
        
    def create_personal_info_group(self):
        """Create the personal information group box"""
        # Group box
        group_box = QGroupBox("個人基本資料")
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        
        # Chinese name
        self.chinese_name = QLineEdit()
        self.chinese_name.setPlaceholderText("請輸入您的中文姓名")
        form_layout.addRow("姓名 (中文):", self.chinese_name)
        
        # English name
        self.english_name = QLineEdit()
        self.english_name.setPlaceholderText("請輸入您的英文姓名")
        form_layout.addRow("姓名 (英文):", self.english_name)
        
        # Gender
        gender_layout = QHBoxLayout()
        self.gender_male = QRadioButton("男")
        self.gender_female = QRadioButton("女")
        self.gender_male.setChecked(True)
        gender_layout.addWidget(self.gender_male)
        gender_layout.addWidget(self.gender_female)
        gender_layout.addStretch()
        form_layout.addRow("性別:", gender_layout)
        
        # Birth date
        self.birth_date = QDateEdit()
        self.birth_date.setDisplayFormat("yyyy-MM-dd")
        self.birth_date.setDate(QDate.currentDate().addYears(-30))  # Default to 30 years ago
        self.birth_date.setCalendarPopup(True)
        form_layout.addRow("生辰年月日:", self.birth_date)
        
        # Birth time
        self.birth_time_combo = QComboBox()
        for hour in range(24):
            self.birth_time_combo.addItem(f"{hour:02d}:00 - {hour:02d}:59")
        form_layout.addRow("出生時辰:", self.birth_time_combo)
        
        # Zodiac
        self.zodiac_combo = QComboBox()
        self.zodiac_combo.addItems(WESTERN_ZODIACS)
        form_layout.addRow("星座:", self.zodiac_combo)
        
        # Chinese Zodiac
        self.chinese_zodiac_combo = QComboBox()
        self.chinese_zodiac_combo.addItems(CHINESE_ZODIACS)
        form_layout.addRow("生肖:", self.chinese_zodiac_combo)
        
        # MBTI
        self.mbti_combo = QComboBox()
        self.mbti_combo.addItems(MBTI_TYPES)
        form_layout.addRow("MBTI 人格:", self.mbti_combo)
        
        # Birthplace
        self.birthplace = QLineEdit()
        self.birthplace.setPlaceholderText("請輸入您的出生地點")
        form_layout.addRow("出生地:", self.birthplace)
        
        group_box.setLayout(form_layout)
        return group_box
    
    def create_fortune_type_group(self):
        """Create the fortune type group box"""
        # Group box
        group_box = QGroupBox("命理分析類型")
        layout = QVBoxLayout()
        
        # Fortune Type
        type_form = QFormLayout()
        self.fortune_type_combo = QComboBox()
        self.fortune_type_combo.addItems(FORTUNE_TYPES)
        type_form.addRow("分析方式:", self.fortune_type_combo)
        layout.addLayout(type_form)
        
        # Analysis Focus
        focus_form = QFormLayout()
        self.focus_combo = QComboBox()
        self.focus_combo.addItems(FOCUS_AREAS)
        focus_form.addRow("分析重點:", self.focus_combo)
        layout.addLayout(focus_form)
        
        group_box.setLayout(layout)
        return group_box
    
    def create_life_phases_group(self):
        """Create the life phases group box"""
        # Group box
        group_box = QGroupBox("人生階段選擇")
        layout = QVBoxLayout()
        
        # Description
        description = QLabel("選擇您希望重點分析的人生階段（可多選）：")
        layout.addWidget(description)
        
        # Grid for checkboxes
        grid = QGridLayout()
        self.life_phase_checks = []
        
        for i, phase in enumerate(LIFE_PHASES):
            checkbox = QCheckBox(phase)
            self.life_phase_checks.append(checkbox)
            row = i // 2
            col = i % 2
            grid.addWidget(checkbox, row, col)
        
        layout.addLayout(grid)
        group_box.setLayout(layout)
        return group_box
    
    def get_user_data(self):
        """
        Collect all user input data
        
        Returns:
            dict: A dictionary containing all user inputs
        """
        # Get gender
        gender = "男" if self.gender_male.isChecked() else "女"
        
        # Get selected life phases
        selected_phases = []
        for checkbox in self.life_phase_checks:
            if checkbox.isChecked():
                selected_phases.append(checkbox.text())
        
        # Build data dictionary
        user_data = {
            'chinese_name': self.chinese_name.text(),
            'english_name': self.english_name.text(),
            'gender': gender,
            'birth_date': self.birth_date.date().toString("yyyy-MM-dd"),
            'birth_time': self.birth_time_combo.currentText(),
            'zodiac': self.zodiac_combo.currentText(),
            'chinese_zodiac': self.chinese_zodiac_combo.currentText(),
            'mbti': self.mbti_combo.currentText(),
            'birthplace': self.birthplace.text(),
            'fortune_type': self.fortune_type_combo.currentText(),
            'focus_area': self.focus_combo.currentText(),
            'life_phases': selected_phases
        }
        
        return user_data