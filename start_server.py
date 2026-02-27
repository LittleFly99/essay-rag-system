"""
Web 应用启动脚本
"""
import os
import sys

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    import uvicorn
    from src.core.config import settings
    from src.api.main import app

    print(f"启动 RAG 作文教学系统 Web 服务...")
    print(f"访问地址: http://{settings.api_host}:{settings.api_port}")
    print(f"API 文档: http://{settings.api_host}:{settings.api_port}/docs")

    uvicorn.run(
        "src.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )
