"""
ChromaDB 向量数据库客户端

用于 RAG 知识库，存储小红书动态、用户历史经验等。
"""

from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
from langchain.embeddings.base import Embeddings
from hikebutler.config.loader import load_config
from hikebutler.models.embedding_factory import get_embedding
import logging

logger = logging.getLogger(__name__)


class ChromaDBClient:
    """ChromaDB 向量数据库客户端。"""

    def __init__(self):
        """初始化 ChromaDB 客户端。"""
        config = load_config()
        chroma_config = config.get("database", {}).get("chromadb", {})
        self.path = chroma_config.get("path", "./chroma_db")
        self.collection_name = chroma_config.get("collection_name", "hiking_knowledge")

        # 初始化 ChromaDB 客户端
        self.client = chromadb.PersistentClient(
            path=self.path,
            settings=Settings(anonymized_telemetry=False),
        )

        # 获取或创建集合
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"},
        )

        # 获取 Embedding 模型
        self.embedding_model = get_embedding()

        logger.info(f"ChromaDB 客户端初始化成功: {self.path}")

    def add_documents(
        self,
        documents: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None,
    ):
        """
        添加文档到向量库。

        Args:
            documents: 文档列表
            metadatas: 元数据列表
            ids: 文档 ID 列表
        """
        # 生成 embeddings
        embeddings = self.embedding_model.embed_documents(documents)

        # 如果没有提供 IDs，自动生成
        if ids is None:
            ids = [f"doc_{i}" for i in range(len(documents))]

        # 如果没有提供元数据，使用空字典
        if metadatas is None:
            metadatas = [{}] * len(documents)

        # 添加到集合
        self.collection.add(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
            ids=ids,
        )

        logger.info(f"已添加 {len(documents)} 个文档到向量库")

    def search(
        self,
        query: str,
        top_k: int = 5,
        similarity_threshold: float = 0.7,
    ) -> List[Dict[str, Any]]:
        """
        搜索相似文档。

        Args:
            query: 查询文本
            top_k: 返回前 k 个结果
            similarity_threshold: 相似度阈值

        Returns:
            搜索结果列表，每个结果包含 document、metadata、distance
        """
        # 生成查询 embedding
        query_embedding = self.embedding_model.embed_query(query)

        # 搜索
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

        # 格式化结果
        formatted_results = []
        if results["documents"] and len(results["documents"][0]) > 0:
            for i, doc in enumerate(results["documents"][0]):
                distance = results["distances"][0][i] if results["distances"] else 1.0
                # ChromaDB 使用余弦距离，转换为相似度
                similarity = 1 - distance

                if similarity >= similarity_threshold:
                    formatted_results.append(
                        {
                            "document": doc,
                            "metadata": results["metadatas"][0][i]
                            if results["metadatas"]
                            else {},
                            "similarity": similarity,
                            "distance": distance,
                        }
                    )

        return formatted_results

    def delete_collection(self):
        """删除集合（谨慎使用）。"""
        self.client.delete_collection(name=self.collection_name)
        logger.warning(f"已删除集合: {self.collection_name}")

