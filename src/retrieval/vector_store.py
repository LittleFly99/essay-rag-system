"""
向量数据库管理
使用 ChromaDB 作为向量数据库
"""
import os
from typing import List, Dict, Any, Optional, Tuple
from loguru import logger

from ..core.models import DocumentChunk
from .embedding import EmbeddingModel

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    logger.warning("chromadb 未安装，将使用内存向量存储")


class VectorStore:
    """向量数据库类"""

    def __init__(self, db_path: str = "./data/vectordb"):
        self.db_path = db_path
        self.embedding_model = EmbeddingModel()
        self.client = None
        self.collection = None
        self._documents = []  # 内存存储后备方案
        self._embeddings = []  # 内存存储嵌入向量
        self._metadata = []   # 内存存储元数据
        self._initialize_db()

    def _initialize_db(self):
        """初始化数据库"""
        try:
            if CHROMADB_AVAILABLE:
                os.makedirs(self.db_path, exist_ok=True)
                self.client = chromadb.PersistentClient(path=self.db_path)
                self.collection = self.client.get_or_create_collection(
                    name="essay_knowledge",
                    metadata={"description": "作文知识库"}
                )
                logger.info(f"ChromaDB 初始化成功: {self.db_path}")
            else:
                logger.info("使用内存向量存储")
        except Exception as e:
            logger.error(f"向量数据库初始化失败: {e}")
            logger.info("将使用内存向量存储")

    def add_documents(self, chunks: List[DocumentChunk]) -> bool:
        """添加文档块到向量数据库"""
        try:
            if not chunks:
                return True

            # 提取文本内容
            texts = [chunk.content for chunk in chunks]

            # 生成嵌入向量
            embeddings = self.embedding_model.encode(texts)

            if CHROMADB_AVAILABLE and self.collection is not None:
                # 使用 ChromaDB
                ids = [chunk.id or f"doc_{i}" for i, chunk in enumerate(chunks)]
                metadatas = [chunk.metadata for chunk in chunks]
                documents = texts

                self.collection.add(
                    embeddings=embeddings,
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
                logger.info(f"成功添加 {len(chunks)} 个文档块到 ChromaDB")
            else:
                # 使用内存存储
                for i, chunk in enumerate(chunks):
                    self._documents.append(chunk.content)
                    self._embeddings.append(embeddings[i])
                    self._metadata.append(chunk.metadata)
                logger.info(f"成功添加 {len(chunks)} 个文档块到内存存储")

            return True
        except Exception as e:
            logger.error(f"添加文档失败: {e}")
            return False

    def search(self, query: str, top_k: int = 5, filter_dict: Optional[Dict[str, Any]] = None) -> List[Tuple[DocumentChunk, float]]:
        """搜索相关文档"""
        try:
            if CHROMADB_AVAILABLE and self.collection is not None:
                return self._search_chromadb(query, top_k, filter_dict)
            else:
                return self._search_memory(query, top_k, filter_dict)
        except Exception as e:
            logger.error(f"向量搜索失败: {e}")
            return []

    def _search_chromadb(self, query: str, top_k: int, filter_dict: Optional[Dict[str, Any]]) -> List[Tuple[DocumentChunk, float]]:
        """使用 ChromaDB 搜索"""
        try:
            # 生成查询向量
            query_embedding = self.embedding_model.encode_single(query)

            # 执行搜索
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where=filter_dict
            )

            # 处理结果
            search_results = []
            if results['documents'] and results['documents'][0]:
                for i, (doc, metadata, distance) in enumerate(zip(
                    results['documents'][0],
                    results['metadatas'][0],
                    results['distances'][0]
                )):
                    chunk = DocumentChunk(
                        id=results['ids'][0][i],
                        content=doc,
                        metadata=metadata,
                        source=metadata.get('source', 'unknown'),
                        chunk_index=metadata.get('chunk_index', 0)
                    )
                    # ChromaDB 返回的是距离，需要转换为相似度
                    similarity = 1.0 / (1.0 + distance)
                    search_results.append((chunk, similarity))

            return search_results
        except Exception as e:
            logger.error(f"ChromaDB 搜索失败: {e}")
            return []

    def _search_memory(self, query: str, top_k: int, filter_dict: Optional[Dict[str, Any]]) -> List[Tuple[DocumentChunk, float]]:
        """使用内存存储搜索"""
        try:
            if not self._documents:
                return []

            # 生成查询向量
            query_embedding = self.embedding_model.encode_single(query)

            # 计算相似度
            similarities = []
            for i, embedding in enumerate(self._embeddings):
                similarity = self.embedding_model.similarity(query_embedding, embedding)

                # 应用过滤器
                if filter_dict:
                    metadata = self._metadata[i]
                    match = all(
                        metadata.get(key) == value
                        for key, value in filter_dict.items()
                    )
                    if not match:
                        continue

                similarities.append((i, similarity))

            # 排序并取 top_k
            similarities.sort(key=lambda x: x[1], reverse=True)
            top_results = similarities[:top_k]

            # 构建结果
            search_results = []
            for idx, similarity in top_results:
                chunk = DocumentChunk(
                    id=f"mem_doc_{idx}",
                    content=self._documents[idx],
                    metadata=self._metadata[idx],
                    source=self._metadata[idx].get('source', 'memory'),
                    chunk_index=idx
                )
                search_results.append((chunk, similarity))

            return search_results
        except Exception as e:
            logger.error(f"内存搜索失败: {e}")
            return []

    def delete_documents(self, ids: List[str]) -> bool:
        """删除文档"""
        try:
            if CHROMADB_AVAILABLE and self.collection is not None:
                self.collection.delete(ids=ids)
                logger.info(f"从 ChromaDB 删除 {len(ids)} 个文档")
            else:
                # 内存存储的删除逻辑比较复杂，这里简化处理
                logger.info(f"内存存储暂不支持按ID删除")
            return True
        except Exception as e:
            logger.error(f"删除文档失败: {e}")
            return False

    def get_collection_info(self) -> Dict[str, Any]:
        """获取集合信息"""
        try:
            if CHROMADB_AVAILABLE and self.collection is not None:
                count = self.collection.count()
                return {
                    "type": "ChromaDB",
                    "document_count": count,
                    "collection_name": self.collection.name
                }
            else:
                return {
                    "type": "Memory",
                    "document_count": len(self._documents),
                    "collection_name": "memory_store"
                }
        except Exception as e:
            logger.error(f"获取集合信息失败: {e}")
            return {"type": "Unknown", "document_count": 0}
