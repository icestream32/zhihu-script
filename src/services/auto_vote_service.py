import asyncio
import time
from src.services.browser_manager import BrowserManager
from src.utils.image_utils import ImageDetector
from src.utils.url_utils import UrlManager
from src.config import (
    URLS_FILE,
    VOTE_IMAGE_PATH,
    WAIT_BETWEEN_ACTIONS
)

class AutoVoteService:
    def __init__(self):
        self.browser_manager = BrowserManager()
        self.image_detector = ImageDetector()
        self.url_manager = UrlManager(URLS_FILE)
        
    async def start(self):
        """启动自动点赞服务"""
        # 启动浏览器
        start_success = await self.browser_manager.start()
        if not start_success:
            print("浏览器启动失败，程序退出")
            return False
            
        # 登录知乎
        login_success = await self.browser_manager.login_zhihu()
        if not login_success:
            print("登录失败，程序退出")
            await self.browser_manager.close()
            return False

        # 处理每个URL
        await self.process_urls()
        
        # 关闭浏览器
        await self.browser_manager.close()
        return True
    
    async def process_urls(self):
        """处理所有URL"""
        urls = self.url_manager.get_urls()
        
        if not urls:
            print("没有找到要处理的URL")
            return
            
        for url in urls:
            await self.process_single_url(url)
            
            # 在处理下一个URL前等待一段时间
            await asyncio.sleep(WAIT_BETWEEN_ACTIONS)
    
    async def process_single_url(self, url):
        """处理单个URL"""
        # 导航到URL
        nav_success = await self.browser_manager.navigate_to_url(url)
        if not nav_success:
            print(f"导航到 {url} 失败，跳过此URL")
            return False
            
        # 等待页面充分加载
        await asyncio.sleep(WAIT_BETWEEN_ACTIONS)
        
        # 先滚动到页面底部
        await self.browser_manager.scroll_to_bottom()
        await asyncio.sleep(1)
        
        # 从底部开始向上滚动，直到找到点赞按钮
        vote_success = False
        max_scroll_attempts = 10
        
        for _ in range(max_scroll_attempts):
            # 尝试寻找并点击点赞按钮
            vote_success = self.find_and_click_vote_button()
            if vote_success:
                break
                
            # 向上滚动一定距离
            await self.browser_manager.scroll_up()
            await asyncio.sleep(0.5)
        
        if not vote_success:
            print(f"在 {url} 中未找到点赞按钮")
            return False
            
        print(f"成功点赞: {url}")
        return True
    
    def find_and_click_vote_button(self):
        """寻找并点击点赞按钮"""
        # 查找点赞按钮
        vote_position = self.image_detector.find_template_on_screen(VOTE_IMAGE_PATH)
            
        if vote_position:
            # 点击点赞按钮
            return self.image_detector.click_at_position(vote_position)
            
        return False 