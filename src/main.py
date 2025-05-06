import asyncio
from src.services.auto_vote_service import AutoVoteService
import sys
import os
import signal

# 确保能够导入src目录
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

async def main():
    auto_vote_service = None
    try:
        # 启动自动点赞服务
        auto_vote_service = AutoVoteService()
        success = await auto_vote_service.start()
        
        if success:
            print("程序正常结束")
        else:
            print("程序运行中止")
    except Exception as e:
        print(f"程序遇到意外错误: {str(e)}")
        return False
    finally:
        # 确保浏览器资源被释放
        if auto_vote_service and auto_vote_service.browser_manager:
            await auto_vote_service.browser_manager.close()
    
    return True

def close_event_loop():
    loop = asyncio.get_event_loop()
    pending = asyncio.all_tasks(loop)
    for task in pending:
        task.cancel()
    
    # 给任务一些时间来取消
    loop.run_until_complete(asyncio.sleep(0.1))
    loop.close()

if __name__ == "__main__":
    if sys.platform != "win32":
        signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))
    
    try:
        result = asyncio.run(main())
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    finally:
        # 尝试清理所有资源
        try:
            close_event_loop()
        except Exception as e:
            pass