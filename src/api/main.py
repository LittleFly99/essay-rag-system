"""
FastAPI 应用程序
提供 RESTful API 接口
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, List
from pydantic import BaseModel
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.models import EssayPrompt, RAGRequest, RAGResponse, EssayType, DifficultyLevel
from src.core.utils import setup_logger
from src.rag_system import RAGSystem
from loguru import logger

# 设置日志
setup_logger()

# 创建 FastAPI 应用
app = FastAPI(
    title="作文教学 RAG 系统",
    description="基于 RAG 架构的作文教学辅助系统",
    version="1.0.0"
)

# 添加 CORS 支持
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局 RAG 系统实例
rag_system = None


class EssayPromptRequest(BaseModel):
    """作文题目请求模型"""
    title: str
    description: str = ""
    essay_type: str = "narrative"
    difficulty_level: str = "middle"
    keywords: List[str] = []
    requirements: List[str] = []
    word_count: int = None
    user_requirements: str = ""


class MaterialRequest(BaseModel):
    """素材请求模型"""
    title: str
    content: str
    category: str = "用户添加"


class EssayRequest(BaseModel):
    """范文请求模型"""
    title: str
    content: str
    essay_type: str = "narrative"


@app.on_event("startup")
async def startup_event():
    """应用启动时初始化 RAG 系统"""
    global rag_system
    try:
        logger.info("初始化 RAG 系统...")
        rag_system = RAGSystem()
        rag_system.initialize()
        logger.info("RAG 系统初始化完成")
    except Exception as e:
        logger.error(f"RAG 系统初始化失败: {e}")


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "作文教学 RAG 系统",
        "version": "1.0.0",
        "status": "运行中"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    if rag_system is None:
        return {"status": "unhealthy", "message": "RAG 系统未初始化"}

    try:
        status = rag_system.get_system_status()
        return {
            "status": "healthy",
            "system_status": status
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "message": str(e)
        }


@app.post("/generate-guidance")
async def generate_guidance(request: EssayPromptRequest) -> Dict[str, Any]:
    """生成作文指导"""
    if rag_system is None:
        raise HTTPException(status_code=500, detail="RAG 系统未初始化")

    try:
        # 构建作文题目
        prompt = EssayPrompt(
            title=request.title,
            description=request.description,
            essay_type=EssayType(request.essay_type),
            difficulty_level=DifficultyLevel(request.difficulty_level),
            keywords=request.keywords,
            requirements=request.requirements,
            word_count=request.word_count
        )

        # 构建 RAG 请求
        rag_request = RAGRequest(
            prompt=prompt,
            user_requirements=request.user_requirements
        )

        # 处理请求
        response = rag_system.process_request(rag_request)

        return {
            "success": True,
            "guidance": {
                "theme_analysis": response.guidance.theme_analysis,
                "structure_suggestion": response.guidance.structure_suggestion,
                "writing_tips": response.guidance.writing_tips,
                "key_points": response.guidance.key_points,
                "reference_materials": [
                    {
                        "title": material.title,
                        "content": material.content,
                        "category": material.category
                    }
                    for material in response.guidance.reference_materials
                ],
                "sample_essays": [
                    {
                        "title": essay.title,
                        "content": essay.content,
                        "type": essay.essay_type.value,
                        "highlights": essay.highlights
                    }
                    for essay in response.guidance.sample_essays
                ]
            },
            "confidence_score": response.confidence_score,
            "retrieval_info": response.retrieval_info,
            "generation_info": response.generation_info
        }
    except Exception as e:
        logger.error(f"生成指导失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/add-material")
async def add_material(request: MaterialRequest) -> Dict[str, Any]:
    """添加写作素材"""
    if rag_system is None:
        raise HTTPException(status_code=500, detail="RAG 系统未初始化")

    try:
        success = rag_system.add_material(
            title=request.title,
            content=request.content,
            category=request.category
        )

        if success:
            return {
                "success": True,
                "message": f"成功添加素材: {request.title}"
            }
        else:
            return {
                "success": False,
                "message": "添加素材失败"
            }
    except Exception as e:
        logger.error(f"添加素材失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/add-essay")
async def add_essay(request: EssayRequest) -> Dict[str, Any]:
    """添加范文"""
    if rag_system is None:
        raise HTTPException(status_code=500, detail="RAG 系统未初始化")

    try:
        success = rag_system.add_essay(
            title=request.title,
            content=request.content,
            essay_type=request.essay_type
        )

        if success:
            return {
                "success": True,
                "message": f"成功添加范文: {request.title}"
            }
        else:
            return {
                "success": False,
                "message": "添加范文失败"
            }
    except Exception as e:
        logger.error(f"添加范文失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/search-materials")
async def search_materials(query: str, top_k: int = 5) -> Dict[str, Any]:
    """搜索写作素材"""
    if rag_system is None:
        raise HTTPException(status_code=500, detail="RAG 系统未初始化")

    try:
        materials = rag_system.search_materials(query, top_k)

        return {
            "success": True,
            "query": query,
            "count": len(materials),
            "materials": [
                {
                    "id": material.id,
                    "title": material.title,
                    "content": material.content,
                    "category": material.category,
                    "keywords": material.keywords
                }
                for material in materials
            ]
        }
    except Exception as e:
        logger.error(f"搜索素材失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/search-essays")
async def search_essays(query: str, top_k: int = 3) -> Dict[str, Any]:
    """搜索范文"""
    if rag_system is None:
        raise HTTPException(status_code=500, detail="RAG 系统未初始化")

    try:
        essays = rag_system.search_essays(query, top_k)

        return {
            "success": True,
            "query": query,
            "count": len(essays),
            "essays": [
                {
                    "id": essay.id,
                    "title": essay.title,
                    "content": essay.content,
                    "type": essay.essay_type.value,
                    "difficulty": essay.difficulty_level.value,
                    "score": essay.score,
                    "highlights": essay.highlights
                }
                for essay in essays
            ]
        }
    except Exception as e:
        logger.error(f"搜索范文失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/system-status")
async def get_system_status() -> Dict[str, Any]:
    """获取系统状态"""
    if rag_system is None:
        return {
            "initialized": False,
            "error": "RAG 系统未初始化"
        }

    try:
        return rag_system.get_system_status()
    except Exception as e:
        logger.error(f"获取系统状态失败: {e}")
        return {
            "initialized": False,
            "error": str(e)
        }


if __name__ == "__main__":
    import uvicorn
    from src.core.config import settings

    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )
