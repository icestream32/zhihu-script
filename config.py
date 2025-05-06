import os

# Path configuration
URLS_FILE = 'urls.txt'
ZHIHU_LOGIN_URL = 'https://www.zhihu.com/signin'
VOTE_IMAGE_PATH = 'vote_button_template.png'
LIKE_IMAGE_PATH = 'like_button_template.png'
# FAVORITE_IMAGE_PATH = 'favorite_button_template.png'

# Browser configuration
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
LOGGED_IN_SELECTOR = 'header .AppHeader-profile'
LOGIN_TIMEOUT = 120000  # milliseconds
NAVIGATION_TIMEOUT = 30000  # milliseconds

# Visual processing configuration
CONFIDENCE_THRESHOLD = 0.8
CLICK_OFFSET_RANGE = (-3, 3)
WAIT_AFTER_NAV = 3  # seconds
WAIT_BETWEEN_ACTIONS = 5  # seconds
CLICK_DURATION_RANGE = (0.15, 0.4)  # seconds

# Environment verification
def validate_paths():
    if not os.path.exists(VOTE_IMAGE_PATH):
        raise FileNotFoundError(f"Vote Image {VOTE_IMAGE_PATH} not found")
    if not os.path.exists(LIKE_IMAGE_PATH):
        raise FileNotFoundError(f"Like Image {LIKE_IMAGE_PATH} not found")
    if not os.path.exists(URLS_FILE):
        raise FileNotFoundError(f"Zhihu url File {URLS_FILE} not found")