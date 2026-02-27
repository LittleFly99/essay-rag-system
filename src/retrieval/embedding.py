"""
嵌入模型管理
处理文本向量化
"""
from typing import List, Optional
import numpy as np
from loguru import logger


# 是一个来自 sentence-transformers 库的 Python 类，专门用于将句子或文本转换为向量（embedding）。这些向量可以用于文本相似度计算、聚类、检索等自然语言处理任务。SentenceTransformer 封装了预训练的 Transformer 模型（如 BERT、RoBERTa 等），让你可以方便地将一段文本编码为固定长度的高维向量。
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    logger.warning("sentence-transformers 未安装，将使用简单的向量化方法")


class EmbeddingModel:
    """嵌入模型类"""

    def __init__(self, model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
        self.model_name = model_name
        self.model = None
        self._initialize_model()

    def _initialize_model(self):
        """初始化模型"""
        try:
            if SENTENCE_TRANSFORMERS_AVAILABLE:
                self.model = SentenceTransformer(self.model_name)
                logger.info(f"成功加载嵌入模型: {self.model_name}")
            else:
                logger.warning("使用简单向量化方法")
        except Exception as e:
            logger.error(f"加载嵌入模型失败: {e}")
            self.model = None

    def encode(self, texts: List[str]) -> List[List[float]]:
        """编码文本为向量"""
        try:
            if self.model is not None and SENTENCE_TRANSFORMERS_AVAILABLE:
                # 使用 sentence-transformers
                embeddings = self.model.encode(texts)
                return embeddings.tolist()
            else:
                # 使用简单的向量化方法
                return self._simple_encode(texts)
        except Exception as e:
            logger.error(f"文本编码失败: {e}")
            return self._simple_encode(texts)

    def _simple_encode(self, texts: List[str]) -> List[List[float]]:
        """简单的文本向量化方法（基于字符统计）"""
        try:
            import jieba
            from collections import Counter
            import math

            # 分词并统计词频
            all_words = set()
            text_words = []

            for text in texts:
                words = list(jieba.cut(text))
                text_words.append(words)
                all_words.update(words)

            all_words = list(all_words)
            vocab_size = len(all_words)

            if vocab_size == 0:
                return [[0.0] * 100 for _ in texts]

            # 创建词汇到索引的映射
            word_to_idx = {word: idx for idx, word in enumerate(all_words)}

            # 计算 TF-IDF 向量
            embeddings = []
            for words in text_words:
                word_count = Counter(words)
                tf_idf_vector = [0.0] * min(vocab_size, 100)  # 限制向量维度

                for word, count in word_count.items():
                    if word in word_to_idx:
                        idx = word_to_idx[word]
                        if idx < 100:  # 只取前100维
                            # 简单的 TF-IDF 计算
                            tf = count / len(words) if words else 0
                            # 简化的 IDF 计算
                            idf = math.log(len(texts) + 1)
                            tf_idf_vector[idx] = tf * idf

                # 归一化
                norm = sum(x*x for x in tf_idf_vector) ** 0.5
                if norm > 0:
                    tf_idf_vector = [x/norm for x in tf_idf_vector]

                embeddings.append(tf_idf_vector)

            return embeddings
        except Exception as e:
            logger.error(f"简单编码失败: {e}")
            # 返回随机向量作为后备
            return [[0.1] * 100 for _ in texts]

    def encode_single(self, text: str) -> List[float]:
        """编码单个文本"""
        embeddings = self.encode([text])
        return embeddings[0] if embeddings else [0.0] * 100

    def similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """计算两个向量的余弦相似度"""
        try:
            # 转换为 numpy 数组
            v1 = np.array(vec1)
            v2 = np.array(vec2)

            # 计算余弦相似度
            dot_product = np.dot(v1, v2)
            norm_v1 = np.linalg.norm(v1)
            norm_v2 = np.linalg.norm(v2)

            if norm_v1 == 0 or norm_v2 == 0:
                return 0.0

            similarity = dot_product / (norm_v1 * norm_v2)
            return float(similarity)
        except Exception as e:
            logger.error(f"计算相似度失败: {e}")
            return 0.0
