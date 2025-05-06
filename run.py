import os
import sys
import asyncio

# 确保能够导入src目录
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入主程序
from src.main import main, close_event_loop

# 运行主程序
if __name__ == "__main__":
    try:
        result = asyncio.run(main())
        # 如果返回False，程序出错，设置非零退出码
        if not result:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n程序被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"程序遇到致命错误: {str(e)}")
        sys.exit(1)
    finally:
        # 尝试清理所有资源
        try:
            close_event_loop()
        except Exception:
            pass  # 忽略清理过程中的错误 