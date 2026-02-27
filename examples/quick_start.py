"""
快速开始指南和使用示例
"""
import os
import sys

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.models import EssayPrompt, EssayType, DifficultyLevel, RAGRequest
from src.rag_system import RAGSystem


def quick_start_example():
    """快速开始示例"""
    print("=== RAG 作文教学系统 - 快速开始 ===\n")

    # 1. 创建和初始化系统
    print("1. 创建 RAG 系统...")
    rag_system = RAGSystem()

    print("2. 初始化系统（加载示例数据）...")
    if rag_system.initialize():
        print("   ✓ 系统初始化成功！")
    else:
        print("   ✗ 系统初始化失败")
        return

    # 2. 查看系统状态
    print("\n3. 检查系统状态...")
    status = rag_system.get_system_status()
    print(f"   - 素材数量: {status['knowledge_base']['materials_count']}")
    print(f"   - 范文数量: {status['knowledge_base']['essays_count']}")
    print(f"   - 向量数据库: {status['vector_store']['type']}")

    # 3. 创建作文题目
    print("\n4. 创建作文题目...")
    prompt = EssayPrompt(
        title="我最敬佩的人",
        description="写一篇记叙文，通过具体事例表现你最敬佩的人的品质",
        essay_type=EssayType.NARRATIVE,
        difficulty_level=DifficultyLevel.MIDDLE,
        keywords=["敬佩", "品质", "事例"],
        requirements=[
            "选择一个你最敬佩的人",
            "通过具体事例来表现人物品质",
            "语言要生动形象，情感要真挚"
        ],
        word_count=600
    )
    print(f"   题目: {prompt.title}")
    print(f"   类型: {prompt.essay_type.value}")
    print(f"   难度: {prompt.difficulty_level.value}")

    # 4. 生成写作指导
    print("\n5. 生成写作指导...")
    request = RAGRequest(
        prompt=prompt,
        user_requirements="希望重点突出人物的精神品质"
    )

    response = rag_system.process_request(request)

    print(f"   置信度分数: {response.confidence_score:.2f}")
    print(f"   找到相关素材: {response.retrieval_info.get('materials_count', 0)} 个")
    print(f"   找到相关范文: {response.retrieval_info.get('essays_count', 0)} 篇")

    # 5. 显示指导内容
    print("\n=== 生成的写作指导 ===")

    print("\n【主题分析】")
    print(response.guidance.theme_analysis)

    print("\n【结构建议】")
    for i, suggestion in enumerate(response.guidance.structure_suggestion, 1):
        print(f"{i}. {suggestion}")

    print("\n【写作技巧】")
    for tip in response.guidance.writing_tips:
        print(f"• {tip}")

    print("\n【要点提示】")
    for point in response.guidance.key_points:
        print(f"• {point}")

    if response.guidance.reference_materials:
        print("\n【参考素材】")
        for material in response.guidance.reference_materials[:2]:  # 只显示前2个
            print(f"• 【{material.category}】{material.title}")
            print(f"  {material.content[:100]}...")

    if response.guidance.sample_essays:
        print("\n【参考范文】")
        for essay in response.guidance.sample_essays[:1]:  # 只显示1篇
            print(f"• 【{essay.essay_type.value}】{essay.title}")
            if essay.highlights:
                print(f"  亮点: {', '.join(essay.highlights)}")

    print("\n=== 示例完成 ===")


def advanced_example():
    """高级使用示例"""
    print("=== 高级使用示例 ===\n")

    rag_system = RAGSystem()
    rag_system.initialize()

    # 添加自定义素材
    print("1. 添加自定义素材...")
    success = rag_system.add_material(
        title="科学家的坚持",
        content="居里夫人为了提炼纯镭，在简陋的实验室里坚持了四年，每天搅拌几十公斤的沥青铀矿渣。她的双手因为长期接触放射性物质而伤痕累累，但她从未放弃。最终，她成功提炼出了0.1克纯镭，为科学事业做出了巨大贡献。",
        category="科学故事"
    )
    print(f"   添加素材: {'成功' if success else '失败'}")

    # 添加自定义范文
    print("\n2. 添加自定义范文...")
    essay_content = """我最敬佩的人是我的爷爷。他虽然已经七十多岁了，但依然每天坚持晨练，身体硬朗，精神矍铄。

爷爷年轻时是一名医生。那时医疗条件很差，他经常要走很远的山路去给村民看病。有一次，一个孩子半夜突发高烧，爷爷二话不说，背起药箱就往山里赶。山路崎岖难行，爷爷摔了好几跤，膝盖都磨破了，但他咬牙坚持，终于及时赶到，救了那个孩子。

现在爷爷退休了，但他依然闲不住，经常免费为邻里乡亲诊病。他说："能帮助别人是我最大的快乐。"

爷爷用他的行动诠释了什么是医者仁心，什么是无私奉献。他是我最敬佩的人，也是我学习的榜样。"""

    success = rag_system.add_essay(
        title="我最敬佩的人——爷爷",
        content=essay_content,
        essay_type="narrative"
    )
    print(f"   添加范文: {'成功' if success else '失败'}")

    # 使用更复杂的题目
    print("\n3. 处理议论文题目...")
    prompt = EssayPrompt(
        title="谈科学精神的重要性",
        description="结合具体事例，论述科学精神在现代社会发展中的重要作用",
        essay_type=EssayType.ARGUMENTATIVE,
        difficulty_level=DifficultyLevel.HIGH,
        keywords=["科学精神", "重要性", "社会发展"],
        requirements=[
            "观点明确，论证充分",
            "举例典型，说服力强",
            "语言严谨，逻辑清晰",
            "体现时代特色"
        ],
        word_count=800
    )

    request = RAGRequest(
        prompt=prompt,
        user_requirements="希望结合现代科技发展的实例，体现科学精神的时代价值"
    )

    response = rag_system.process_request(request)

    print(f"   置信度分数: {response.confidence_score:.2f}")
    print("\n【主题分析】")
    print(response.guidance.theme_analysis)

    print("\n【结构建议】")
    for i, suggestion in enumerate(response.guidance.structure_suggestion, 1):
        print(f"{i}. {suggestion}")

    # 搜索功能演示
    print("\n4. 搜索功能演示...")
    materials = rag_system.search_materials("科学", top_k=3)
    print(f"   搜索'科学'相关素材: {len(materials)} 个")
    for material in materials:
        print(f"   • {material.title}")

    essays = rag_system.search_essays("敬佩", top_k=2)
    print(f"\n   搜索'敬佩'相关范文: {len(essays)} 篇")
    for essay in essays:
        print(f"   • {essay.title}")


def web_api_example():
    """Web API 使用示例"""
    print("=== Web API 使用示例 ===\n")

    print("启动 Web 服务器:")
    print("python start_server.py")
    print("\n访问以下地址:")
    print("• 主页: http://localhost:8000")
    print("• API 文档: http://localhost:8000/docs")
    print("• 健康检查: http://localhost:8000/health")

    print("\n主要 API 端点:")
    print("• POST /generate-guidance - 生成写作指导")
    print("• POST /add-material - 添加写作素材")
    print("• POST /add-essay - 添加范文")
    print("• GET /search-materials - 搜索素材")
    print("• GET /search-essays - 搜索范文")
    print("• GET /system-status - 系统状态")

    print("\n示例请求 (使用 curl):")
    print("""
curl -X POST "http://localhost:8000/generate-guidance" \\
     -H "Content-Type: application/json" \\
     -d '{
       "title": "我的老师",
       "description": "写一篇记叙文",
       "essay_type": "narrative",
       "difficulty_level": "middle",
       "keywords": ["老师", "品质"],
       "requirements": ["通过具体事例表现人物品质"]
     }'
""")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="RAG 作文教学系统使用示例")
    parser.add_argument("--example", choices=["quick", "advanced", "api"], default="quick",
                       help="选择示例类型")

    args = parser.parse_args()

    if args.example == "quick":
        quick_start_example()
    elif args.example == "advanced":
        advanced_example()
    elif args.example == "api":
        web_api_example()
