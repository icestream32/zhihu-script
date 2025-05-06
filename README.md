# 知乎自动点赞工具

这是一个基于OpenCV和鼠标自动点击的知乎自动点赞工具。工具会自动打开浏览器，访问指定的知乎链接，识别点赞按钮并模拟鼠标点击。

## 功能特点

- 自动打开浏览器并登录知乎
- 支持批量处理多个知乎链接
- 使用OpenCV模板匹配识别点赞按钮
- 模拟真实的鼠标移动和点击行为
- 记录已处理的链接，避免重复操作

## 使用前准备

1. 确保已安装所有依赖项：`pip install -r requirements.txt`
2. 在 `urls.txt` 文件中添加需要点赞的知乎链接（每行一个链接）
3. 在 `src/templates` 目录中添加点赞按钮的模板图像 (`vote_button.png`)
   - 提示：可以使用截图工具截取知乎点赞按钮的图像

## 使用方法

1. 运行程序：`python run.py`
2. 程序会打开浏览器并显示二维码登录页面
3. 使用知乎APP扫描二维码完成登录
4. 登录后，程序会自动处理所有链接并进行点赞操作

## 项目结构

```
zhihu-script/
├── run.py                  # 入口脚本
├── requirements.txt        # 依赖项
├── urls.txt                # 知乎链接列表
├── src/
│   ├── main.py             # 主程序
│   ├── config.py           # 配置文件
│   ├── services/
│   │   ├── browser_manager.py   # 浏览器管理器
│   │   └── auto_like_service.py # 自动点赞服务
│   ├── utils/
│   │   ├── image_utils.py       # 图像处理工具
│   │   └── url_utils.py         # URL处理工具
│   └── templates/
│       └── vote_button.png      # 点赞按钮模板图像
```
