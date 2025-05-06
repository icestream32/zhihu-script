from playwright.async_api import async_playwright
from config import (
    USER_AGENT,
    LOGGED_IN_SELECTOR,
    LOGIN_TIMEOUT,
    NAVIGATION_TIMEOUT,
    ZHIHU_LOGIN_URL
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
            
            # Launch browser
            self.browser = await self.playwright.chromium.launch(
                headless=False  # Set to headful mode
            )
            
            # Create browser context
            self.context = await self.browser.new_context(
                user_agent=USER_AGENT,
                viewport={"width": 1920, "height": 1080}
            )
            
            # Create new page
            self.page = await self.context.new_page()
            
            # Set timeouts - using non-async method
            self.page.set_default_timeout(LOGIN_TIMEOUT)
            self.page.set_default_navigation_timeout(NAVIGATION_TIMEOUT)
            
            print("Browser started successfully")
            return True
        except Exception as e:
            print(f"Browser startup failed: {str(e)}")
            # If any exception occurs during startup, try to close the resources already created
            await self.close()
            return False
        
    async def login_zhihu(self):
        try:
            await self.page.goto(ZHIHU_LOGIN_URL, wait_until='networkidle')
            qr_tab_selector = '.SignFlow-tabs button:nth-child(2)'
            qr_code_image_selector = '.Qrcode-img'
            
            await self.page.wait_for_selector('.SignFlow-tabs', timeout=15000)
            if await self.page.is_visible(qr_tab_selector):
                await self.page.click(qr_tab_selector)
            await self.page.wait_for_selector(qr_code_image_selector, state='visible', timeout=10000)
            print("\nplease scan QR code to login...")
            await self.page.wait_for_selector(LOGGED_IN_SELECTOR, timeout=LOGIN_TIMEOUT)
            print("Check login...")
            return True
        except Exception as e:
            print(f"登录失败: {e}")
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
                
            print("Browser resources released")
        except Exception as e:
            print(f"Error while closing browser: {str(e)}")
        