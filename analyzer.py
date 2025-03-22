"""
Core functionality for destiny analysis using LLM
"""

import requests
import json
import logging
from config import OLLAMA_API_URL, OLLAMA_MODEL, MODEL_SETTINGS

class DestinyAnalyzer:
    """Class to handle all destiny analysis operations"""
    
    def __init__(self):
        """Initialize the analyzer"""
        self.logger = logging.getLogger(__name__)
    
    def create_prompt(self, user_data):
        """
        Create a detailed prompt for the LLM based on user data
        
        Args:
            user_data (dict): Dictionary containing all user information
            
        Returns:
            str: The formatted prompt
        """
        # Extract user data
        chinese_name = user_data.get('chinese_name', '')
        english_name = user_data.get('english_name', '')
        birth_date = user_data.get('birth_date', '')
        birth_time = user_data.get('birth_time', '')
        zodiac = user_data.get('zodiac', '')
        chinese_zodiac = user_data.get('chinese_zodiac', '')
        mbti = user_data.get('mbti', '')
        birthplace = user_data.get('birthplace', '')
        fortune_type = user_data.get('fortune_type', '')
        focus_area = user_data.get('focus_area', '')
        life_phases = user_data.get('life_phases', [])
        gender = user_data.get('gender', '')
        
        # Format life phases for analysis if provided
        life_phases_text = ""
        if life_phases:
            life_phases_text = "特別關注以下人生階段:\n- " + "\n- ".join(life_phases)
        
        # Create comprehensive prompt
        prompt = f"""請以頂尖命理大師的專業角度，根據以下個人資料，進行全面的{fortune_type}，分析主題為「{focus_area}」：

個人資料：
- 姓名（中文）：{chinese_name}
- 姓名（英文）：{english_name}
- 性別：{gender}
- 生辰年月日：{birth_date}
- 出生時辰：{birth_time}
- 星座：{zodiac}
- 生肖：{chinese_zodiac}
- MBTI 人格：{mbti}
- 出生地：{birthplace}

{life_phases_text}

請提供深入全面的命理分析，內容需包含：

1. 命盤總論：
   - 八字四柱解析（天干地支、五行強弱）
   - 紫微斗數主星與輔星組合
   - 先天命盤特徵與關鍵命理指標

2. 人格特質與性格剖析：
   - 內在性格與外在表現
   - 思維模式與決策風格
   - 潛意識行為模式與心理傾向

3. 人生全程發展軌跡（依照不同年齡階段）：
   - 成長期關鍵發展
   - 事業高峰與低谷時期
   - 重要人生轉折點與契機

4. 專項深度分析：
   - 事業發展軌跡與職業適配性
   - 財富累積模式與理財特質
   - 感情關係模式與理想伴侶特質
   - 健康狀況預測與養生建議
   - 人際關係與社交網絡特徵

5. 命理衝突與人生挑戰：
   - 先天命盤衝突點
   - 人生潛在阻礙與困境
   - 各生命階段關鍵挑戰

6. 開運化解建議：
   - 五行能量平衡方案
   - 事業方向優化建議
   - 人際關係調和方法
   - 吉祥物與開運色彩建議

請以專業且通俗易懂的方式分析，深入解讀命理奧秘，但避免籠統空泛的內容。分析要基於傳統命理學與現代心理學的結合，並具有前瞻性的人生指導意義。

回答請使用繁體中文，內容需分段落、小標題清楚呈現，便於閱讀理解。
"""
        return prompt
    
    def analyze(self, user_data):
        """
        Perform destiny analysis by querying the LLM
        
        Args:
            user_data (dict): Dictionary containing all user information
            
        Returns:
            str: The analysis result
            
        Raises:
            Exception: If the API call fails
        """
        # Create the prompt
        prompt = self.create_prompt(user_data)
        
        # Prepare API request
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": MODEL_SETTINGS
        }
        
        headers = {"Content-Type": "application/json"}
        
        try:
            # Call the API
            self.logger.info("Calling Ollama API for analysis")
            response = requests.post(OLLAMA_API_URL, json=payload, headers=headers, timeout=2000)
            
            # Check for successful response
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "未能生成分析結果")
            else:
                error_msg = f"API 調用失敗：HTTP {response.status_code}\n{response.text}"
                self.logger.error(error_msg)
                raise Exception(error_msg)
                
        except requests.RequestException as e:
            error_msg = f"連接 Ollama API 失敗: {str(e)}"
            self.logger.error(error_msg)
            raise Exception(error_msg)
        
        except Exception as e:
            error_msg = f"分析過程中發生錯誤: {str(e)}"
            self.logger.error(error_msg)
            raise Exception(error_msg)