"""
简化测试版本
只使用基本的内置库来演示RAG系统功能
"""
import os
import sys
import json
import hashlib
from typing import List, Dict, Any
from datetime import datetime

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 简化的数据模型
class EssayPrompt:
    def __init__(self, title: str, description: str = "", essay_type: str = "narrative",
                 difficulty_level: str = "middle", keywords: List[str] = None,
                 requirements: List[str] = None, word_count: int = None):
        self.title = title
        self.description = description
        self.essay_type = essay_type
        self.difficulty_level = difficulty_level
        self.keywords = keywords or []
        self.requirements = requirements or []
        self.word_count = word_count
        self.created_at = datetime.now()

class WritingMaterial:
    def __init__(self, title: str, content: str, category: str,
                 difficulty_level: str = "middle", keywords: List[str] = None):
        self.id = hashlib.md5((title + content).encode()).hexdigest()[:12]
        self.title = title
        self.content = content
        self.category = category
        self.difficulty_level = difficulty_level
        self.keywords = keywords or []

class SampleEssay:
    def __init__(self, title: str, content: str, essay_type: str = "narrative",
                 difficulty_level: str = "middle", score: int = None,
                 highlights: List[str] = None):
        self.id = hashlib.md5((title + content).encode()).hexdigest()[:12]
        self.title = title
        self.content = content
        self.essay_type = essay_type
        self.difficulty_level = difficulty_level
        self.score = score
        self.highlights = highlights or []

class WritingGuidance:
    def __init__(self, theme_analysis: str, structure_suggestion: List[str],
                 writing_tips: List[str], key_points: List[str],
                 reference_materials: List[WritingMaterial] = None,
                 sample_essays: List[SampleEssay] = None):
        self.theme_analysis = theme_analysis
        self.structure_suggestion = structure_suggestion
        self.writing_tips = writing_tips
        self.key_points = key_points
        self.reference_materials = reference_materials or []
        self.sample_essays = sample_essays or []

# 简化的知识库
class SimpleKnowledgeBase:
    def __init__(self, knowledge_path: str):
        self.knowledge_path = knowledge_path
        self.materials_file = os.path.join(knowledge_path, "materials.json")
        self.essays_file = os.path.join(knowledge_path, "essays.json")

        os.makedirs(knowledge_path, exist_ok=True)
        self._init_data_files()

    def _init_data_files(self):
        if not os.path.exists(self.materials_file):
            with open(self.materials_file, 'w', encoding='utf-8') as f:
                json.dump({"materials": []}, f, ensure_ascii=False, indent=2)

        if not os.path.exists(self.essays_file):
            with open(self.essays_file, 'w', encoding='utf-8') as f:
                json.dump({"essays": []}, f, ensure_ascii=False, indent=2)

    def add_material(self, material: WritingMaterial) -> bool:
        try:
            with open(self.materials_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            material_dict = {
                "id": material.id,
                "title": material.title,
                "content": material.content,
                "category": material.category,
                "difficulty_level": material.difficulty_level,
                "keywords": material.keywords
            }

            data["materials"].append(material_dict)

            with open(self.materials_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            return True
        except Exception as e:
            print(f"添加素材失败: {e}")
            return False

    def search_materials(self, query: str, top_k: int = 5) -> List[WritingMaterial]:
        try:
            with open(self.materials_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            materials = []
            for material_dict in data["materials"]:
                # 简单的文本匹配
                if (query in material_dict["title"] or
                    query in material_dict["content"] or
                    any(query in keyword for keyword in material_dict["keywords"])):

                    material = WritingMaterial(
                        title=material_dict["title"],
                        content=material_dict["content"],
                        category=material_dict["category"],
                        difficulty_level=material_dict["difficulty_level"],
                        keywords=material_dict["keywords"]
                    )
                    materials.append(material)

            return materials[:top_k]
        except Exception as e:
            print(f"搜索素材失败: {e}")
            return []

    def list_materials(self) -> List[WritingMaterial]:
        try:
            with open(self.materials_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            materials = []
            for material_dict in data["materials"]:
                material = WritingMaterial(
                    title=material_dict["title"],
                    content=material_dict["content"],
                    category=material_dict["category"],
                    difficulty_level=material_dict["difficulty_level"],
                    keywords=material_dict["keywords"]
                )
                materials.append(material)

            return materials
        except Exception as e:
            print(f"列出素材失败: {e}")
            return []

# 简化的RAG系统
class SimpleRAGSystem:
    def __init__(self):
        self.knowledge_base = SimpleKnowledgeBase("./data/knowledge")
        self.is_initialized = False

    def initialize(self, load_sample_data: bool = True) -> bool:
        try:
            if load_sample_data:
                self._load_sample_data()
            self.is_initialized = True
            print("RAG 系统初始化完成")
            return True
        except Exception as e:
            print(f"RAG 系统初始化失败: {e}")
            return False

    def _load_sample_data(self):
        # 添加示例素材
        sample_materials = [
            WritingMaterial(
                title="坚持不懈的力量",
                content="古人云：'绳锯木断，水滴石穿。'这句话告诉我们，持续不断的努力具有巨大的力量。无论是学习还是工作，只要我们坚持不懈，终将收获成功。就像著名科学家爱迪生发明电灯泡，经历了上千次失败，但他从未放弃，最终照亮了整个世界。",
                category="名言警句",
                keywords=["坚持", "毅力", "成功", "努力"]
            ),
            WritingMaterial(
                title="友谊的珍贵",
                content="真正的友谊如同珍珠一样珍贵。朋友在我们快乐时与我们分享喜悦，在我们困难时给予帮助和支持。马克思和恩格斯的友谊就是最好的例子，他们在学术上相互切磋，在生活中相互扶持，这种友谊超越了时间和空间的限制。",
                category="情感表达",
                keywords=["友谊", "朋友", "支持", "分享"]
            ),
            WritingMaterial(
                title="读书的意义",
                content="书籍是人类进步的阶梯。通过读书，我们可以获得知识，开阔视野，提升思维能力。读书不仅能让我们了解世界，更能让我们了解自己。正如莎士比亚所说：'书籍是全世界的营养品。'让我们在书的海洋中尽情遨游吧。",
                category="学习成长",
                keywords=["读书", "知识", "成长", "智慧"]
            )
        ]

        for material in sample_materials:
            self.knowledge_base.add_material(material)

    def process_request(self, prompt: EssayPrompt) -> Dict[str, Any]:
        try:
            # 检索相关素材
            query = f"{prompt.title} {prompt.description} {' '.join(prompt.keywords)}"
            materials = self.knowledge_base.search_materials(query, top_k=3)

            # 生成写作指导
            guidance = self._generate_guidance(prompt, materials)

            return {
                "guidance": guidance,
                "materials_found": len(materials),
                "confidence_score": 0.8 if materials else 0.5
            }
        except Exception as e:
            print(f"处理请求失败: {e}")
            return {
                "guidance": self._get_fallback_guidance(),
                "materials_found": 0,
                "confidence_score": 0.3
            }

    def _generate_guidance(self, prompt: EssayPrompt, materials: List[WritingMaterial]) -> WritingGuidance:
        # 根据作文类型生成指导
        if prompt.essay_type == "narrative":
            theme_analysis = f"这是一篇记叙文题目：'{prompt.title}'。记叙文要求通过具体的事例来表达主题思想，注重情节的完整性和人物的生动性。"
            structure_suggestion = [
                "开头：简要交代时间、地点、人物、事件",
                "发展：详细叙述事件的经过，突出重点",
                "高潮：事件的关键转折点",
                "结尾：总结事件意义，点明主题"
            ]
            writing_tips = [
                "运用生动的描写手法，让读者有身临其境的感觉",
                "合理安排叙述顺序，可采用倒叙、插叙等手法",
                "注意详略得当，重点部分要详写",
                "融入真情实感，使文章感人"
            ]
            key_points = [
                "确保事件的真实性和完整性",
                "人物形象要鲜明立体",
                "语言要生动形象，富有表现力",
                "主题要明确，通过事件自然体现"
            ]
        else:  # argumentative
            theme_analysis = f"这是一篇议论文题目：'{prompt.title}'。议论文要求明确提出观点，并运用事实和道理进行论证，逻辑性要强。"
            structure_suggestion = [
                "引论：提出问题，明确论点",
                "本论：分层论证，举例说明",
                "结论：总结论证，强调观点"
            ]
            writing_tips = [
                "论点要明确、正确、深刻",
                "论据要典型、充分、有说服力",
                "论证要严密、合理、有逻辑",
                "语言要准确、鲜明、生动"
            ]
            key_points = [
                "开门见山，直接提出论点",
                "选择有代表性的事例和名言",
                "注意正反对比论证",
                "结尾要有力，升华主题"
            ]

        return WritingGuidance(
            theme_analysis=theme_analysis,
            structure_suggestion=structure_suggestion,
            writing_tips=writing_tips,
            key_points=key_points,
            reference_materials=materials
        )

    def _get_fallback_guidance(self) -> WritingGuidance:
        return WritingGuidance(
            theme_analysis="系统暂时无法分析题目，请稍后重试。",
            structure_suggestion=["请根据题目要求规划文章结构"],
            writing_tips=["注意语言表达的准确性"],
            key_points=["紧扣题目要求"]
        )

    def get_system_status(self) -> Dict[str, Any]:
        materials = self.knowledge_base.list_materials()
        return {
            "initialized": self.is_initialized,
            "materials_count": len(materials),
            "system_type": "Simplified RAG System"
        }

def quick_demo():
    """快速演示"""
    print("=== RAG 作文教学系统 - 简化演示 ===\n")

    # 1. 创建和初始化系统
    print("1. 创建 RAG 系统...")
    rag_system = SimpleRAGSystem()

    print("2. 初始化系统（加载示例数据）...")
    if rag_system.initialize():
        print("   ✓ 系统初始化成功！")
    else:
        print("   ✗ 系统初始化失败")
        return

    # 2. 查看系统状态
    print("\n3. 检查系统状态...")
    status = rag_system.get_system_status()
    print(f"   - 素材数量: {status['materials_count']}")
    print(f"   - 系统类型: {status['system_type']}")

    # 3. 创建作文题目
    print("\n4. 创建作文题目...")
    prompt = EssayPrompt(
        title="我最敬佩的人",
        description="写一篇记叙文，通过具体事例表现你最敬佩的人的品质",
        essay_type="narrative",
        difficulty_level="middle",
        keywords=["敬佩", "品质", "事例"],
        requirements=[
            "选择一个你最敬佩的人",
            "通过具体事例来表现人物品质",
            "语言要生动形象，情感要真挚"
        ],
        word_count=600
    )
    print(f"   题目: {prompt.title}")
    print(f"   类型: {prompt.essay_type}")
    print(f"   难度: {prompt.difficulty_level}")

    # 4. 生成写作指导
    print("\n5. 生成写作指导...")
    response = rag_system.process_request(prompt)

    guidance = response["guidance"]
    print(f"   置信度分数: {response['confidence_score']:.2f}")
    print(f"   找到相关素材: {response['materials_found']} 个")

    # 5. 显示指导内容
    print("\n=== 生成的写作指导 ===")

    print("\n【主题分析】")
    print(guidance.theme_analysis)

    print("\n【结构建议】")
    for i, suggestion in enumerate(guidance.structure_suggestion, 1):
        print(f"{i}. {suggestion}")

    print("\n【写作技巧】")
    for tip in guidance.writing_tips:
        print(f"• {tip}")

    print("\n【要点提示】")
    for point in guidance.key_points:
        print(f"• {point}")

    if guidance.reference_materials:
        print("\n【参考素材】")
        for material in guidance.reference_materials[:2]:
            print(f"• 【{material.category}】{material.title}")
            print(f"  {material.content[:100]}...")

    print("\n=== 演示完成 ===")

if __name__ == "__main__":
    quick_demo()
