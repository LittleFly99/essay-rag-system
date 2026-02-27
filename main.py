"""
RAG 作文教学系统主程序
"""
import os
import sys

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core import setup_logger, EssayPrompt, EssayType, DifficultyLevel
from src.rag_system import RAGSystem
from loguru import logger


def main():
    """主函数演示"""
    # 设置日志
    setup_logger()

    logger.info("=== 作文教学 RAG 系统演示 ===")

    # 创建并初始化 RAG 系统
    logger.info("初始化 RAG 系统...")
    rag_system = RAGSystem()

    if not rag_system.initialize():
        logger.error("RAG 系统初始化失败")
        return

    # 显示系统状态
    status = rag_system.get_system_status()
    logger.info(f"系统状态: {status}")

    # 演示 1：处理记叙文题目
    logger.info("\n=== 演示 1：记叙文指导 ===")
    demo_narrative_essay()

    # 演示 2：处理议论文题目
    logger.info("\n=== 演示 2：议论文指导 ===")
    demo_argumentative_essay()

    # 演示 3：搜索功能
    logger.info("\n=== 演示 3：搜索功能 ===")
    demo_search_functionality()

    logger.info("\n=== 演示完成 ===")


def demo_narrative_essay():
    """演示记叙文指导生成"""
    from src.core.models import RAGRequest

    # 创建 RAG 系统
    rag_system = RAGSystem()
    rag_system.initialize()

    # 构建作文题目
    prompt = EssayPrompt(
        title="我的老师",
        description="写一篇关于老师的记叙文，要求通过具体事例表现老师的品质",
        essay_type=EssayType.NARRATIVE,
        difficulty_level=DifficultyLevel.MIDDLE,
        keywords=["老师", "品质", "事例"],
        requirements=[
            "通过具体事例表现人物品质",
            "语言生动形象",
            "情感真挚"
        ],
        word_count=600
    )

    # 构建请求
    request = RAGRequest(
        prompt=prompt,
        user_requirements="希望重点突出老师的敬业精神"
    )

    # 处理请求
    response = rag_system.process_request(request)

    # 输出结果
    logger.info(f"题目: {prompt.title}")
    logger.info(f"置信度分数: {response.confidence_score:.2f}")

    logger.info("=== 主题分析 ===")
    logger.info(response.guidance.theme_analysis)

    logger.info("=== 结构建议 ===")
    for i, suggestion in enumerate(response.guidance.structure_suggestion, 1):
        logger.info(f"{i}. {suggestion}")

    logger.info("=== 写作技巧 ===")
    for tip in response.guidance.writing_tips:
        logger.info(f"• {tip}")

    logger.info("=== 要点提示 ===")
    for point in response.guidance.key_points:
        logger.info(f"• {point}")

    logger.info(f"=== 检索信息 ===")
    logger.info(f"相关素材数量: {response.retrieval_info.get('materials_count', 0)}")
    logger.info(f"相关范文数量: {response.retrieval_info.get('essays_count', 0)}")


def demo_argumentative_essay():
    """演示议论文指导生成"""
    from src.core.models import RAGRequest

    # 创建 RAG 系统
    rag_system = RAGSystem()
    rag_system.initialize()

    # 构建作文题目
    prompt = EssayPrompt(
        title="论坚持的重要性",
        description="写一篇议论文，论证坚持在成功中的重要作用",
        essay_type=EssayType.ARGUMENTATIVE,
        difficulty_level=DifficultyLevel.HIGH,
        keywords=["坚持", "成功", "重要性"],
        requirements=[
            "论点明确",
            "论据充分",
            "论证有力",
            "逻辑清晰"
        ],
        word_count=800
    )

    # 构建请求
    request = RAGRequest(
        prompt=prompt,
        user_requirements="希望能举一些具体的名人事例"
    )

    # 处理请求
    response = rag_system.process_request(request)

    # 输出结果
    logger.info(f"题目: {prompt.title}")
    logger.info(f"置信度分数: {response.confidence_score:.2f}")

    logger.info("=== 主题分析 ===")
    logger.info(response.guidance.theme_analysis)

    logger.info("=== 结构建议 ===")
    for i, suggestion in enumerate(response.guidance.structure_suggestion, 1):
        logger.info(f"{i}. {suggestion}")

    logger.info("=== 写作技巧 ===")
    for tip in response.guidance.writing_tips:
        logger.info(f"• {tip}")


def demo_search_functionality():
    """演示搜索功能"""
    # 创建 RAG 系统
    rag_system = RAGSystem()
    rag_system.initialize()

    # 搜索素材
    logger.info("=== 搜索写作素材 ===")
    materials = rag_system.search_materials("坚持", top_k=3)
    for i, material in enumerate(materials, 1):
        logger.info(f"{i}. 【{material.category}】{material.title}")
        logger.info(f"   内容: {material.content[:100]}...")

    # 搜索范文
    logger.info("\n=== 搜索范文 ===")
    essays = rag_system.search_essays("老师", top_k=2)
    for i, essay in enumerate(essays, 1):
        logger.info(f"{i}. 【{essay.essay_type.value}】{essay.title}")
        logger.info(f"   内容: {essay.content[:100]}...")


def interactive_demo():
    """交互式演示"""
    logger.info("=== 交互式演示模式 ===")

    # 创建 RAG 系统
    rag_system = RAGSystem()
    if not rag_system.initialize():
        logger.error("RAG 系统初始化失败")
        return

    while True:
        print("\n" + "="*50)
        print("作文教学 RAG 系统")
        print("="*50)
        print("1. 生成写作指导")
        print("2. 搜索写作素材")
        print("3. 搜索范文")
        print("4. 添加素材")
        print("5. 添加范文")
        print("6. 查看系统状态")
        print("0. 退出")

        choice = input("\n请选择功能 (0-6): ").strip()

        if choice == "0":
            print("感谢使用！")
            break
        elif choice == "1":
            interactive_generate_guidance(rag_system)
        elif choice == "2":
            interactive_search_materials(rag_system)
        elif choice == "3":
            interactive_search_essays(rag_system)
        elif choice == "4":
            interactive_add_material(rag_system)
        elif choice == "5":
            interactive_add_essay(rag_system)
        elif choice == "6":
            interactive_show_status(rag_system)
        else:
            print("无效选择，请重新输入")


def interactive_generate_guidance(rag_system):
    """交互式生成指导"""
    from src.core.models import RAGRequest

    print("\n--- 生成写作指导 ---")

    title = input("请输入作文题目: ").strip()
    if not title:
        print("题目不能为空")
        return

    description = input("请输入题目描述 (可选): ").strip()

    print("作文类型:")
    print("1. 记叙文 (narrative)")
    print("2. 议论文 (argumentative)")
    print("3. 说明文 (descriptive)")
    essay_type_choice = input("请选择作文类型 (1-3): ").strip()

    essay_type_map = {
        "1": "narrative",
        "2": "argumentative",
        "3": "descriptive"
    }
    essay_type = essay_type_map.get(essay_type_choice, "narrative")

    print("难度等级:")
    print("1. 小学 (elementary)")
    print("2. 初中 (middle)")
    print("3. 高中 (high)")
    level_choice = input("请选择难度等级 (1-3): ").strip()

    level_map = {
        "1": "elementary",
        "2": "middle",
        "3": "high"
    }
    difficulty_level = level_map.get(level_choice, "middle")

    # 构建题目
    prompt = EssayPrompt(
        title=title,
        description=description,
        essay_type=EssayType(essay_type),
        difficulty_level=DifficultyLevel(difficulty_level)
    )

    request = RAGRequest(prompt=prompt)

    print("\n正在生成写作指导...")
    response = rag_system.process_request(request)

    print(f"\n=== 写作指导：{title} ===")
    print(f"置信度分数: {response.confidence_score:.2f}")

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


def interactive_search_materials(rag_system):
    """交互式搜索素材"""
    print("\n--- 搜索写作素材 ---")

    query = input("请输入搜索关键词: ").strip()
    if not query:
        print("搜索关键词不能为空")
        return

    materials = rag_system.search_materials(query, top_k=5)

    if not materials:
        print("未找到相关素材")
        return

    print(f"\n找到 {len(materials)} 个相关素材:")
    for i, material in enumerate(materials, 1):
        print(f"\n{i}. 【{material.category}】{material.title}")
        print(f"   {material.content[:200]}...")


def interactive_search_essays(rag_system):
    """交互式搜索范文"""
    print("\n--- 搜索范文 ---")

    query = input("请输入搜索关键词: ").strip()
    if not query:
        print("搜索关键词不能为空")
        return

    essays = rag_system.search_essays(query, top_k=3)

    if not essays:
        print("未找到相关范文")
        return

    print(f"\n找到 {len(essays)} 篇相关范文:")
    for i, essay in enumerate(essays, 1):
        print(f"\n{i}. 【{essay.essay_type.value}】{essay.title}")
        if essay.highlights:
            print(f"   亮点: {', '.join(essay.highlights)}")
        print(f"   {essay.content[:200]}...")


def interactive_add_material(rag_system):
    """交互式添加素材"""
    print("\n--- 添加写作素材 ---")

    title = input("请输入素材标题: ").strip()
    if not title:
        print("标题不能为空")
        return

    content = input("请输入素材内容: ").strip()
    if not content:
        print("内容不能为空")
        return

    category = input("请输入素材分类 (默认: 用户添加): ").strip()
    if not category:
        category = "用户添加"

    success = rag_system.add_material(title, content, category)

    if success:
        print(f"成功添加素材: {title}")
    else:
        print("添加素材失败")


def interactive_add_essay(rag_system):
    """交互式添加范文"""
    print("\n--- 添加范文 ---")

    title = input("请输入范文标题: ").strip()
    if not title:
        print("标题不能为空")
        return

    content = input("请输入范文内容: ").strip()
    if not content:
        print("内容不能为空")
        return

    print("作文类型:")
    print("1. 记叙文 (narrative)")
    print("2. 议论文 (argumentative)")
    print("3. 说明文 (descriptive)")
    choice = input("请选择作文类型 (1-3): ").strip()

    type_map = {
        "1": "narrative",
        "2": "argumentative",
        "3": "descriptive"
    }
    essay_type = type_map.get(choice, "narrative")

    success = rag_system.add_essay(title, content, essay_type)

    if success:
        print(f"成功添加范文: {title}")
    else:
        print("添加范文失败")


def interactive_show_status(rag_system):
    """显示系统状态"""
    print("\n--- 系统状态 ---")

    status = rag_system.get_system_status()

    print(f"系统已初始化: {status.get('initialized', False)}")

    kb_info = status.get('knowledge_base', {})
    print(f"素材数量: {kb_info.get('materials_count', 0)}")
    print(f"范文数量: {kb_info.get('essays_count', 0)}")

    vector_info = status.get('vector_store', {})
    print(f"向量数据库类型: {vector_info.get('type', 'Unknown')}")
    print(f"向量数据库文档数: {vector_info.get('document_count', 0)}")

    generator_info = status.get('generator', {})
    print(f"生成器可用: {generator_info.get('available', False)}")
    print(f"生成器模型: {generator_info.get('model', 'Unknown')}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="作文教学 RAG 系统")
    parser.add_argument("--mode", choices=["demo", "interactive"], default="demo",
                       help="运行模式: demo(演示) 或 interactive(交互)")

    args = parser.parse_args()

    if args.mode == "demo":
        main()
    elif args.mode == "interactive":
        interactive_demo()
