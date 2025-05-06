from browser_manager import BrowserManager
import asyncio

async def main():
    try:
        print("Starting browser...")
        browser_manager = BrowserManager()
        
        start_success = await browser_manager.start()
        
        if not start_success:
            print("Browser startup failed, program exiting")
            return
            
        print("Browser is ready")
        # Add subsequent business logic here
        await browser_manager.login_zhihu()
        # Close the browser when finished
        print("Closing browser...")
        await browser_manager.close()
        print("Program ended normally")
    except Exception as e:
        print(f"Program encountered an unexpected error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())

