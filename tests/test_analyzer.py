"""
分析模組的基本測試
"""

import unittest
from cosmic_destiny.analyzer import DestinyAnalyzer

class TestAnalyzer(unittest.TestCase):
    """DestinyAnalyzer 類的測試用例"""
    
    def setUp(self):
        """設置測試用例"""
        self.analyzer = DestinyAnalyzer()
        
    def test_prompt_creation(self):
        """測試提示是否正確創建"""
        # 樣本用戶數據
        user_data = {
            "chinese_name": "測試",
            "english_name": "Test",
            "gender": "男",
            "birth_date": "2000-01-01",
            "birth_time": "12:00 - 12:59",
            "zodiac": "摩羯座 (Capricorn)",
            "chinese_zodiac": "龍 (Dragon)",
            "mbti": "INTJ",
            "birthplace": "台北",
            "fortune_type": "紫微斗數命盤分析",
            "focus_area": "事業發展與財富軌跡",
            "life_phases": ["成年早期 (19-30歲)", "成年中期 (31-45歲)"]
        }
        
        # 創建提示
        prompt = self.analyzer.create_prompt(user_data)
        
        # 基本驗證
        self.assertIsInstance(prompt, str)
        self.assertIn(user_data["chinese_name"], prompt)
        self.assertIn(user_data["fortune_type"], prompt)
        self.assertIn(user_data["focus_area"], prompt)
        
if __name__ == "__main__":
    unittest.main()

