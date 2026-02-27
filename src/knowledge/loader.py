"""
知识库数据加载器
用于加载和初始化知识库数据
"""
import os
from typing import List, Dict, Any
from loguru import logger

from .local_kb import LocalKnowledgeBase
from ..core.models import WritingMaterial, SampleEssay, EssayType, DifficultyLevel
from ..core.utils import read_text_file, generate_id


class KnowledgeLoader:
    """知识库数据加载器"""

    def __init__(self, kb: LocalKnowledgeBase):
        self.kb = kb

    def load_sample_data(self) -> bool:
        """加载示例数据"""
        try:
            # 加载示例素材
            self._load_sample_materials()

            # 加载示例范文
            self._load_sample_essays()

            logger.info("示例数据加载完成")
            return True
        except Exception as e:
            logger.error(f"加载示例数据失败: {e}")
            return False

    def _load_sample_materials(self):
        """加载示例写作素材"""
        sample_materials = [
            {
                "title": "坚持不懈的力量",
                "content": "古人云：'绳锯木断，水滴石穿。'这句话告诉我们，持续不断的努力具有巨大的力量。无论是学习还是工作，只要我们坚持不懈，终将收获成功。就像著名科学家爱迪生发明电灯泡，经历了上千次失败，但他从未放弃，最终照亮了整个世界。",
                "category": "名言警句",
                "keywords": ["坚持", "毅力", "成功", "努力"],
                "source": "古代名言",
                "difficulty_level": "middle"
            },
            {
                "title": "友谊的珍贵",
                "content": "真正的友谊如同珍珠一样珍贵。朋友在我们快乐时与我们分享喜悦，在我们困难时给予帮助和支持。马克思和恩格斯的友谊就是最好的例子，他们在学术上相互切磋，在生活中相互扶持，这种友谊超越了时间和空间的限制。",
                "category": "情感表达",
                "keywords": ["友谊", "朋友", "支持", "分享"],
                "source": "现代素材",
                "difficulty_level": "middle"
            },
            {
                "title": "环保的重要性",
                "content": "地球是我们共同的家园，保护环境是每个人的责任。随着工业的发展，环境污染日益严重，我们必须采取行动。从小事做起，比如垃圾分类、节约用水、减少使用塑料袋等，每个人的小小努力汇聚起来就能产生巨大的力量。",
                "category": "社会话题",
                "keywords": ["环保", "责任", "行动", "家园"],
                "source": "时事素材",
                "difficulty_level": "high"
            },
            {
                "title": "读书的意义",
                "content": "书籍是人类进步的阶梯。通过读书，我们可以获得知识，开阔视野，提升思维能力。读书不仅能让我们了解世界，更能让我们了解自己。正如莎士比亚所说：'书籍是全世界的营养品。'让我们在书的海洋中尽情遨游吧。",
                "category": "学习成长",
                "keywords": ["读书", "知识", "成长", "智慧"],
                "source": "教育名言",
                "difficulty_level": "middle"
            }
        ]

        for material_data in sample_materials:
            material = WritingMaterial(
                title=material_data["title"],
                content=material_data["content"],
                category=material_data["category"],
                keywords=material_data["keywords"],
                source=material_data.get("source"),
                difficulty_level=DifficultyLevel(material_data["difficulty_level"])
            )
            self.kb.add_material(material)

    def _load_sample_essays(self):
        """加载示例范文"""
        sample_essays = [
            {
                "title": "我的老师",
                "content": """我的语文老师是一位和蔼可亲的女老师。她有着一头乌黑的长发，总是梳理得整整齐齐。她的眼睛很大，总是闪烁着智慧的光芒。

每当上语文课的时候，老师总是用生动的语言为我们讲解课文。她的声音很好听，就像泉水一样清脆。当我们遇到不懂的问题时，她总是耐心地为我们解答，从不觉得麻烦。

有一次，我因为生病落下了几天的功课。老师发现后，主动为我补课。她放弃了自己的休息时间，认真地为我讲解每一个知识点。看着老师疲惫的神情，我的心中充满了感动。

老师不仅在学习上关心我们，在生活上也像妈妈一样照顾我们。记得有一次下雨，我忘记带雨伞，老师主动把自己的雨伞借给了我。

我爱我的老师，她是我人生路上的引路人。我要好好学习，用优异的成绩来报答她的恩情。""",
                "essay_type": "narrative",
                "difficulty_level": "elementary",
                "score": 85,
                "highlights": ["描写生动", "情感真挚", "结构清晰"],
                "structure_analysis": "开头介绍老师外貌，中间通过具体事例展现老师的品质，结尾抒发感情"
            },
            {
                "title": "论勤奋",
                "content": """勤奋是成功的基石。古往今来，凡是在事业上取得成就的人，都离不开勤奋这一品质。

首先，勤奋能够弥补天赋的不足。天才固然重要，但更重要的是后天的努力。爱迪生曾说："天才是百分之一的灵感加上百分之九十九的汗水。"这句话深刻地说明了勤奋的重要性。即使天赋平平，只要勤奋努力，也能取得不凡的成就。

其次，勤奋能够积累知识和经验。知识需要通过不断的学习和实践来获得，经验需要通过反复的尝试和总结来积累。只有勤奋的人，才能在知识的海洋中不断探索，在实践的道路上不断前进。

再次，勤奋能够培养坚强的意志。在勤奋的过程中，我们会遇到各种困难和挫折。正是这些困难锻炼了我们的意志，让我们变得更加坚强和成熟。

总之，勤奋是通向成功的必由之路。让我们都做一个勤奋的人，用汗水浇灌成功的花朵。""",
                "essay_type": "argumentative",
                "difficulty_level": "high",
                "score": 90,
                "highlights": ["论点明确", "论证充分", "逻辑清晰"],
                "structure_analysis": "总-分-总结构，开头提出论点，中间分层论证，结尾总结升华"
            }
        ]

        for essay_data in sample_essays:
            essay = SampleEssay(
                title=essay_data["title"],
                content=essay_data["content"],
                essay_type=EssayType(essay_data["essay_type"]),
                difficulty_level=DifficultyLevel(essay_data["difficulty_level"]),
                score=essay_data.get("score"),
                highlights=essay_data.get("highlights", []),
                structure_analysis=essay_data.get("structure_analysis")
            )
            self.kb.add_essay(essay)

    def load_from_directory(self, directory_path: str) -> bool:
        """从目录加载数据"""
        try:
            if not os.path.exists(directory_path):
                logger.warning(f"目录不存在: {directory_path}")
                return False

            # 加载素材文件
            materials_dir = os.path.join(directory_path, "materials")
            if os.path.exists(materials_dir):
                self._load_materials_from_dir(materials_dir)

            # 加载范文文件
            essays_dir = os.path.join(directory_path, "essays")
            if os.path.exists(essays_dir):
                self._load_essays_from_dir(essays_dir)

            logger.info(f"从目录加载数据完成: {directory_path}")
            return True
        except Exception as e:
            logger.error(f"从目录加载数据失败: {e}")
            return False

    def _load_materials_from_dir(self, materials_dir: str):
        """从目录加载素材"""
        for filename in os.listdir(materials_dir):
            if filename.endswith('.txt'):
                filepath = os.path.join(materials_dir, filename)
                content = read_text_file(filepath)
                if content:
                    # 简单的素材创建逻辑，实际可以更复杂
                    material = WritingMaterial(
                        title=filename.replace('.txt', ''),
                        content=content,
                        category="导入素材",
                        difficulty_level=DifficultyLevel.MIDDLE
                    )
                    self.kb.add_material(material)

    def _load_essays_from_dir(self, essays_dir: str):
        """从目录加载范文"""
        for filename in os.listdir(essays_dir):
            if filename.endswith('.txt'):
                filepath = os.path.join(essays_dir, filename)
                content = read_text_file(filepath)
                if content:
                    # 简单的范文创建逻辑，实际可以更复杂
                    essay = SampleEssay(
                        title=filename.replace('.txt', ''),
                        content=content,
                        essay_type=EssayType.NARRATIVE,
                        difficulty_level=DifficultyLevel.MIDDLE
                    )
                    self.kb.add_essay(essay)
