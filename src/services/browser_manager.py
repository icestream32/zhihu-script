from playwright.async_api import async_playwright
import asyncio
import time
from src.config import (
    USER_AGENT,
    LOGGED_IN_SELECTOR,
    LOGIN_TIMEOUT,
    NAVIGATION_TIMEOUT,
    ZHIHU_LOGIN_URL,
    WAIT_AFTER_NAV
)

class BrowserManager:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    async def start(self):
        try:
            # Initialize playwright
            self.playwright = await async_playwright().start()
            
            # Launch browser with additional parameters
            self.browser = await self.playwright.chromium.launch(
                headless=False,
                args=[
                    "--disable-gpu",
                    "--no-sandbox",
                    "--disable-blink-features=AutomationControlled",
                    "--disable-extensions",
                    "--disable-notifications",
                    "--disable-popup-blocking",
                    "--ignore-certificate-errors",
                ]
            )
            
            # Create browser context
            self.context = await self.browser.new_context(
                user_agent=USER_AGENT,
                viewport={"width": 1920, "height": 1080},
                ignore_https_errors=True
            )
            
            # Create new page
            self.page = await self.context.new_page()
            
            # Set timeouts
            self.page.set_default_timeout(LOGIN_TIMEOUT)
            self.page.set_default_navigation_timeout(NAVIGATION_TIMEOUT)
            return True
        except Exception as e:
            print(f"浏览器启动失败: {str(e)}")
            # 如果启动过程中出现异常，尝试关闭已创建的资源
            await self.close()
            return False
        
    async def login_zhihu(self):
        try:
            await self.page.goto(ZHIHU_LOGIN_URL, wait_until='networkidle')
            print("请扫描二维码登录...")
            
            # 等待登录成功
            await self.wait_for_login()
            print("登录成功!")
            return True
        except Exception as e:
            print(f"登录失败: {e}")
            return False

    async def check_login_status(self):
        """检查是否已登录知乎"""
        try:
            # 重试机制
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    # 检查顶部个人信息菜单是否存在
                    logged_in = await self.page.evaluate('''
                        () => document.querySelector('#root div.Popover.AppHeader-menu') !== null
                    ''')
                    return logged_in
                except Exception as e:
                    if "Execution context was destroyed" in str(e) and attempt < max_retries - 1:
                        # 如果是因为导航导致的执行上下文销毁，等待一下再重试
                        await asyncio.sleep(1)
                        continue
                    else:
                        # 其他错误或重试次数用完，抛出异常
                        raise
        except Exception as e:
            print(f"检查登录状态时出错: {str(e)}")
            # 如果无法检查登录状态，保守地返回False
            return False

    async def wait_for_login(self, check_interval=1):
        """等待用户完成登录"""
        print("等待登录中...")
        
        # 循环检查登录状态
        while True:
            logged_in = await self.check_login_status()
            
            if logged_in:
                return True
                
            # 短暂等待后再次检查
            await asyncio.sleep(check_interval)

    async def navigate_to_url(self, url):
        """导航到指定URL"""
        try:
            await self.page.goto(url, wait_until='networkidle')
            # 等待页面加载完成
            await asyncio.sleep(WAIT_AFTER_NAV)
            return True
        except Exception as e:
            print(f"导航失败: {str(e)}")
            return False

    async def close(self):
        try:
            if self.page:
                await self.page.close()
                self.page = None
                
            if self.context:
                await self.context.close()
                self.context = None
                
            if self.browser:
                await self.browser.close()
                self.browser = None
                
            if self.playwright:
                await self.playwright.stop()
                self.playwright = None
            
            # 清理异步IO资源
            await self.cleanup_asyncio_resources()
        except Exception as e:
            print(f"关闭浏览器时出错: {str(e)}")
            
    async def scroll_to_bottom(self):
        """滚动到页面底部"""
        try:
            await self.page.evaluate("""
                window.scrollTo({
                    top: document.body.scrollHeight,
                    behavior: 'smooth'
                });
            """)
            return True
        except Exception as e:
            print(f"滚动到页面底部时出错: {str(e)}")
            return False
            
    async def scroll_up(self, pixels=300):
        """向上滚动指定像素"""
        try:
            await self.page.evaluate(f"""
                window.scrollBy({{
                    top: -{pixels},
                    behavior: 'smooth'
                }});
            """)
            return True
        except Exception as e:
            print(f"向上滚动页面时出错: {str(e)}")
            return False
            
    async def cleanup_asyncio_resources(self):
        try:
            # 获取当前事件循环
            loop = asyncio.get_running_loop()
            
            # 关闭所有挂起的任务
            tasks = [task for task in asyncio.all_tasks(loop) if not task.done() and task is not asyncio.current_task()]
            if tasks:
                for task in tasks:
                    task.cancel()
                # 等待任务取消
                await asyncio.gather(*tasks, return_exceptions=True)
                
            # 等待一小段时间让资源释放
            await asyncio.sleep(0.1)
        except Exception as e:
            print(f"清理asyncio资源时出错: {str(e)}") 