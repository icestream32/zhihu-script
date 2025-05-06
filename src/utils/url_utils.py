import os
from typing import List

class UrlManager:
    def __init__(self, urls_file: str):
        self.urls_file = urls_file
        self.urls = []
        self.load_urls()
    
    def load_urls(self) -> None:
        """从文件加载URL列表"""
        if not os.path.exists(self.urls_file):
            raise FileNotFoundError(f"URL文件不存在: {self.urls_file}")
        
        with open(self.urls_file, 'r', encoding='utf-8') as file:
            # 忽略空行和注释行（以#开头）
            self.urls = [line.strip() for line in file if line.strip() and not line.strip().startswith('#')]
        
        print(f"已加载 {len(self.urls)} 个URL")
    
    def get_urls(self) -> List[str]:
        """获取URL列表"""
        return self.urls
    
    def mark_as_processed(self, url: str) -> None:
        """将URL标记为已处理"""
        if url in self.urls:
            self.urls.remove(url)