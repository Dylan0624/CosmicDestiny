import sys
import json
import requests
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QDateEdit, 
                            QComboBox, QPushButton, QTextEdit, QGridLayout,
                            QGroupBox, QFormLayout, QMessageBox, QTabWidget)
from PyQt6.QtCore import Qt, QDate


class FortuneApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('紫微斗數與姓名八字命理分析')
        self.setGeometry(100, 100, 900, 700)
        
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        
        # Create tab widget
        tab_widget = QTabWidget()
        
        # Create tabs
        input_tab = QWidget()
        result_tab = QWidget()
        
        # Set up layouts for tabs
        input_layout = QVBoxLayout(input_tab)
        result_layout = QVBoxLayout(result_tab)
        
        # Add tabs to tab widget
        tab_widget.addTab(input_tab, "輸入資料")
        tab_widget.addTab(result_tab, "命理分析結果")
        
        # --- Input Tab ---
        # Personal Info Group
        personal_group = QGroupBox("個人基本資料")
        personal_layout = QFormLayout()
        
        # Chinese name
        self.chinese_name = QLineEdit()
        personal_layout.addRow("姓名 (中文):", self.chinese_name)
        
        # English name
        self.english_name = QLineEdit()
        personal_layout.addRow("姓名 (英文):", self.english_name)
        
        # Birth date
        self.birth_date = QDateEdit()
        self.birth_date.setDisplayFormat("yyyy-MM-dd")
        self.birth_date.setDate(QDate.currentDate())
        self.birth_date.setCalendarPopup(True)
        personal_layout.addRow("生辰年月日:", self.birth_date)
        
        # Birth time
        self.birth_time_combo = QComboBox()
        for hour in range(24):
            self.birth_time_combo.addItem(f"{hour:02d}:00 - {hour:02d}:59")
        personal_layout.addRow("出生時辰:", self.birth_time_combo)
        
        # Zodiac
        self.zodiac_combo = QComboBox()
        zodiacs = ["白羊座 (Aries)", "金牛座 (Taurus)", "雙子座 (Gemini)", 
                  "巨蟹座 (Cancer)", "獅子座 (Leo)", "處女座 (Virgo)", 
                  "天秤座 (Libra)", "天蠍座 (Scorpio)", "射手座 (Sagittarius)", 
                  "摩羯座 (Capricorn)", "水瓶座 (Aquarius)", "雙魚座 (Pisces)"]
        self.zodiac_combo.addItems(zodiacs)
        personal_layout.addRow("星座:", self.zodiac_combo)
        
        # Chinese Zodiac
        self.chinese_zodiac_combo = QComboBox()
        chinese_zodiacs = ["鼠 (Rat)", "牛 (Ox)", "虎 (Tiger)", "兔 (Rabbit)", 
                          "龍 (Dragon)", "蛇 (Snake)", "馬 (Horse)", "羊 (Goat)", 
                          "猴 (Monkey)", "雞 (Rooster)", "狗 (Dog)", "豬 (Pig)"]
        self.chinese_zodiac_combo.addItems(chinese_zodiacs)
        personal_layout.addRow("生肖:", self.chinese_zodiac_combo)
        
        # MBTI
        self.mbti_combo = QComboBox()
        mbti_types = ["INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP",
                     "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP"]
        self.mbti_combo.addItems(mbti_types)
        personal_layout.addRow("MBTI 人格:", self.mbti_combo)
        
        # Birthplace
        self.birthplace = QLineEdit()
        personal_layout.addRow("出生地:", self.birthplace)
        
        personal_group.setLayout(personal_layout)
        input_layout.addWidget(personal_group)
        
        # Fortune Type Group
        fortune_group = QGroupBox("命理分析類型")
        fortune_layout = QVBoxLayout()
        
        self.fortune_type_combo = QComboBox()
        fortune_types = ["紫微斗數命盤分析", "姓名八字命盤分析", "綜合分析 (紫微斗數和八字)"]
        self.fortune_type_combo.addItems(fortune_types)
        fortune_layout.addWidget(self.fortune_type_combo)
        
        fortune_group.setLayout(fortune_layout)
        input_layout.addWidget(fortune_group)
        
        # Analysis Focus Group
        focus_group = QGroupBox("分析重點")
        focus_layout = QVBoxLayout()
        
        self.focus_combo = QComboBox()
        focus_areas = ["整體運勢概述", "事業運勢分析", "財富命盤解析", 
                      "感情姻緣分析", "健康狀況分析", "性格特質分析"]
        self.focus_combo.addItems(focus_areas)
        focus_layout.addWidget(self.focus_combo)
        
        focus_group.setLayout(focus_layout)
        input_layout.addWidget(focus_group)
        
        # Generate Button
        self.generate_btn = QPushButton("生成命理分析")
        self.generate_btn.setMinimumHeight(50)
        self.generate_btn.clicked.connect(self.generate_fortune)
        input_layout.addWidget(self.generate_btn)
        
        # --- Result Tab ---
        # Result Display
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        result_layout.addWidget(self.result_text)
        
        # Save Button
        save_btn = QPushButton("儲存分析結果")
        save_btn.clicked.connect(self.save_result)
        result_layout.addWidget(save_btn)
        
        # Add tab widget to main layout
        main_layout.addWidget(tab_widget)
        
        # Set the central widget
        self.setCentralWidget(main_widget)
        
    def generate_fortune(self):
        # Switch to results tab
        for i in range(self.centralWidget().layout().count()):
            if isinstance(self.centralWidget().layout().itemAt(i).widget(), QTabWidget):
                tab_widget = self.centralWidget().layout().itemAt(i).widget()
                tab_widget.setCurrentIndex(1)  # Switch to results tab
        
        # Get input values
        chinese_name = self.chinese_name.text()
        english_name = self.english_name.text()
        birth_date = self.birth_date.date().toString("yyyy-MM-dd")
        birth_time = self.birth_time_combo.currentText()
        zodiac = self.zodiac_combo.currentText()
        chinese_zodiac = self.chinese_zodiac_combo.currentText()
        mbti = self.mbti_combo.currentText()
        birthplace = self.birthplace.text()
        fortune_type = self.fortune_type_combo.currentText()
        focus_area = self.focus_combo.currentText()
        
        # Check if essential fields are filled
        if not chinese_name:
            QMessageBox.warning(self, "缺少資訊", "請輸入您的中文姓名")
            return
        
        # Set a waiting message
        self.result_text.setText("正在生成命理分析結果，請稍候...")
        QApplication.processEvents()  # Update UI
        
        # Create prompt for the AI
        prompt = self.create_prompt(chinese_name, english_name, birth_date, birth_time,
                                  zodiac, chinese_zodiac, mbti, birthplace,
                                  fortune_type, focus_area)
        
        # Call API
        try:
            result = self.call_ollama_api(prompt)
            self.result_text.setText(result)
        except Exception as e:
            self.result_text.setText(f"發生錯誤: {str(e)}\n\n請確認 Ollama 服務已啟動並載入 deepseek-r1:14b 模型。")
    
    def create_prompt(self, chinese_name, english_name, birth_date, birth_time,
                     zodiac, chinese_zodiac, mbti, birthplace,
                     fortune_type, focus_area):
        # Format input data for the prompt
        prompt = f"""請以專業命理師的角度，根據以下個人資料，進行{fortune_type}，重點分析{focus_area}：

個人資料：
- 姓名（中文）：{chinese_name}
- 姓名（英文）：{english_name}
- 生辰年月日：{birth_date}
- 出生時辰：{birth_time}
- 星座：{zodiac}
- 生肖：{chinese_zodiac}
- MBTI 人格：{mbti}
- 出生地：{birthplace}

請提供詳細的命理分析，包含：
1. 八字命盤概述（天干地支、五行分析）
2. 紫微斗數星盤解析（主星、輔星解讀）
3. {focus_area}的詳細分析
4. 近期運勢預測
5. 改運與開運建議

請使用繁體中文回答，並以命理專業術語進行分析，但同時確保一般人也能理解。格式請分段落清楚呈現。
"""
        return prompt
    
    def call_ollama_api(self, prompt):
        """Call the Ollama API with the given prompt."""
        url = "http://localhost:11434/api/generate"
        
        payload = {
            "model": "deepseek-r1:14b",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "top_k": 40
            }
        }
        
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            try:
                result = response.json()
                return result.get("response", "No response generated")
            except:
                return "解析 API 回應時發生錯誤"
        else:
            return f"API 調用失敗：HTTP {response.status_code}\n{response.text}"
    
    def save_result(self):
        """Save the fortune telling result to a text file."""
        from PyQt6.QtWidgets import QFileDialog
        from datetime import datetime
        
        # Get current timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Get the name for the filename
        name = self.chinese_name.text()
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
                    f.write(f"命理分析報告\n")
                    f.write(f"生成日期：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("="*50 + "\n\n")
                    
                    # Write personal info
                    f.write("個人資料：\n")
                    f.write(f"- 姓名（中文）：{self.chinese_name.text()}\n")
                    f.write(f"- 姓名（英文）：{self.english_name.text()}\n")
                    f.write(f"- 生辰年月日：{self.birth_date.date().toString('yyyy-MM-dd')}\n")
                    f.write(f"- 出生時辰：{self.birth_time_combo.currentText()}\n")
                    f.write(f"- 星座：{self.zodiac_combo.currentText()}\n")
                    f.write(f"- 生肖：{self.chinese_zodiac_combo.currentText()}\n")
                    f.write(f"- MBTI 人格：{self.mbti_combo.currentText()}\n")
                    f.write(f"- 出生地：{self.birthplace.text()}\n\n")
                    
                    # Write analysis type
                    f.write(f"分析類型：{self.fortune_type_combo.currentText()}\n")
                    f.write(f"分析重點：{self.focus_combo.currentText()}\n\n")
                    
                    # Write analysis result
                    f.write("命理分析結果：\n")
                    f.write("="*50 + "\n\n")
                    f.write(self.result_text.toPlainText())
                    
                QMessageBox.information(self, "儲存成功", f"命理分析結果已成功儲存至：\n{filename}")
            except Exception as e:
                QMessageBox.critical(self, "儲存失敗", f"儲存命理分析結果時發生錯誤：\n{str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FortuneApp()
    window.show()
    sys.exit(app.exec())