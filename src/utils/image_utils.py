import cv2
import numpy as np
import mss
import time
import random
import pyautogui
from src.config import CONFIDENCE_THRESHOLD, CLICK_OFFSET_RANGE, CLICK_DURATION_RANGE

class ImageDetector:
    def __init__(self):
        self.screen_shot = None
        self.sct = mss.mss()
    
    def capture_screen(self):
        """捕获当前屏幕"""
        monitor = self.sct.monitors[0]  # 捕获主屏幕
        self.screen_shot = np.array(self.sct.grab(monitor))
        # 将BGRA转换为BGR，OpenCV默认使用BGR格式
        self.screen_shot = cv2.cvtColor(self.screen_shot, cv2.COLOR_BGRA2BGR)
        return self.screen_shot
    
    def find_template_on_screen(self, template_path):
        """在屏幕上寻找模板图像"""
        # 捕获屏幕
        screen = self.capture_screen()
        
        # 读取模板图像
        template = cv2.imread(template_path)
        if template is None:
            raise FileNotFoundError(f"无法加载模板图像: {template_path}")
        
        # 获取模板的宽度和高度
        h, w = template.shape[:2]
        
        # 使用模板匹配
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        
        # 查找匹配位置
        locations = np.where(result >= CONFIDENCE_THRESHOLD)
        
        if len(locations[0]) == 0:
            return None
        
        # 获取最佳匹配位置
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val < CONFIDENCE_THRESHOLD:
            return None
        
        # 计算中心点
        center_x = max_loc[0] + w//2
        center_y = max_loc[1] + h//2
        
        return (center_x, center_y, max_val)
    
    @staticmethod
    def click_at_position(position):
        """在指定位置点击"""
        if position is None:
            return False
        
        x, y, confidence = position
        
        # 添加随机偏移以模拟人类行为
        offset_x = random.randint(CLICK_OFFSET_RANGE[0], CLICK_OFFSET_RANGE[1])
        offset_y = random.randint(CLICK_OFFSET_RANGE[0], CLICK_OFFSET_RANGE[1])
        
        # 计算实际点击位置
        click_x = x + offset_x
        click_y = y + offset_y
        
        # 随机点击持续时间
        duration = random.uniform(CLICK_DURATION_RANGE[0], CLICK_DURATION_RANGE[1])
        
        # 执行鼠标点击
        pyautogui.moveTo(click_x, click_y, duration=duration)
        pyautogui.click()

        # 点击后将鼠标复位到屏幕中心而不是角落
        screen_width, screen_height = pyautogui.size()
        pyautogui.moveTo(screen_width // 2, screen_height // 2)
        
        return True 