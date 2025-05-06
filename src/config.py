import os

# 路径配置
URLS_FILE = 'urls.txt'
ZHIHU_LOGIN_URL = 'https://www.zhihu.com/signin'
TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src", "templates")
VOTE_IMAGE_PATH = os.path.join(TEMPLATES_DIR, 'vote_button.png')

# 浏览器配置
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
LOGGED_IN_SELECTOR = 'header .AppHeader-profile'
LOGIN_TIMEOUT = 120000  # 毫秒
NAVIGATION_TIMEOUT = 30000  # 毫秒

# 视觉处理配置
CONFIDENCE_THRESHOLD = 0.7  # 匹配置信度阈值
CLICK_OFFSET_RANGE = (-3, 3)  # 随机点击偏移范围
WAIT_AFTER_NAV = 3  # 导航后等待秒数
WAIT_BETWEEN_ACTIONS = 3  # 操作间隔等待秒数
CLICK_DURATION_RANGE = (0.15, 0.4)  # 点击持续时间范围，单位秒

# 环境验证
def validate_paths():
    """验证必要的文件和目录是否存在"""
    if not os.path.exists(TEMPLATES_DIR):
        os.makedirs(TEMPLATES_DIR)
        print(f"已创建模板目录: {TEMPLATES_DIR}")
        
    if not os.path.exists(VOTE_IMAGE_PATH):
        print(f"警告: 点赞按钮模板图像不存在，请在运行前添加: {VOTE_IMAGE_PATH}")
        
    if not os.path.exists(URLS_FILE):
        with open(URLS_FILE, 'w', encoding='utf-8') as f:
            f.write("# 每行一个知乎URL\n")
        print(f"已创建URL文件: {URLS_FILE}，请添加知乎链接")

# 初始化时验证路径
validate_paths() 