"""
Configuration settings for the application
"""

# Application name
APP_NAME = "CosmicDestiny"

# Ollama API settings
OLLAMA_API_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "deepseek-r1:14b"

# Model settings
MODEL_SETTINGS = {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 40,
    "max_tokens": 4000
}

# UI settings
UI_WINDOW_WIDTH = 1000
UI_WINDOW_HEIGHT = 700
UI_TABS = ["個人資料輸入", "命理分析結果"]

# Analysis types
FORTUNE_TYPES = [
    "紫微斗數命盤分析",
    "姓名八字命盤分析", 
    "五行能量配置分析",
    "八字四柱命盤詳解",
    "綜合命理系統分析"
]

# Analysis focus areas
FOCUS_AREAS = [
    "人生整體命運藍圖",
    "先天性格特質分析",
    "事業發展與財富軌跡",
    "感情姻緣與家庭關係",
    "健康狀況與壽命預測",
    "學業成就與智慧發展",
    "人際關係與社交網絡",
    "精神信仰與心靈成長"
]

# Chinese zodiac signs
CHINESE_ZODIACS = [
    "鼠 (Rat)", 
    "牛 (Ox)", 
    "虎 (Tiger)", 
    "兔 (Rabbit)", 
    "龍 (Dragon)", 
    "蛇 (Snake)", 
    "馬 (Horse)", 
    "羊 (Goat)", 
    "猴 (Monkey)", 
    "雞 (Rooster)", 
    "狗 (Dog)", 
    "豬 (Pig)"
]

# Western zodiac signs
WESTERN_ZODIACS = [
    "白羊座 (Aries)", 
    "金牛座 (Taurus)", 
    "雙子座 (Gemini)", 
    "巨蟹座 (Cancer)", 
    "獅子座 (Leo)", 
    "處女座 (Virgo)", 
    "天秤座 (Libra)", 
    "天蠍座 (Scorpio)", 
    "射手座 (Sagittarius)", 
    "摩羯座 (Capricorn)", 
    "水瓶座 (Aquarius)", 
    "雙魚座 (Pisces)"
]

# MBTI types
MBTI_TYPES = [
    "INTJ", "INTP", "ENTJ", "ENTP", 
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ", 
    "ISTP", "ISFP", "ESTP", "ESFP"
]

# Life phases for analysis
LIFE_PHASES = [
    "童年期 (0-12歲)",
    "青少年期 (13-18歲)",
    "成年早期 (19-30歲)",
    "成年中期 (31-45歲)",
    "成年後期 (46-60歲)",
    "老年期 (61歲以上)"
]