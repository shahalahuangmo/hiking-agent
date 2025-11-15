"""
Embedding 工厂类

通过抽象层实现 Embedding 模型切换，支持 Qwen、DeepSeek、OpenAI 等。
"""

from typing import Any, Dict
from langchain.embeddings.base import Embeddings
from langchain_openai import OpenAIEmbeddings
from hikebutler.config.loader import load_model_config
import logging

logger = logging.getLogger(__name__)


class EmbeddingFactory:
    """Embedding 工厂类，负责创建和管理 Embedding 实例。"""

    _instance: "EmbeddingFactory" = None
    _embedding: Embeddings = None
    _config: Dict[str, Any] = None

    def __new__(cls):
        """单例模式。"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """初始化工厂。"""
        if self._config is None:
            self._config = load_model_config()
            self._embedding = self._create_embedding()

    def _create_embedding(self) -> Embeddings:
        """
        根据配置创建 Embedding 实例。

        Returns:
            Embedding 实例

        Raises:
            ValueError: 不支持的模型提供商
        """
        embedding_config = self._config.get("embedding", {})
        provider = embedding_config.get("provider", "qwen")
        model_name = embedding_config.get("model_name", "text-embedding-v2")
        api_key = embedding_config.get("api_key")
        dimension = embedding_config.get("dimension", 1024)

        if not api_key:
            raise ValueError(f"未配置 {provider} Embedding API Key")

        # 根据提供商创建不同的 Embedding 实例
        if provider == "openai":
            return OpenAIEmbeddings(
                model=model_name,
                openai_api_key=api_key,
            )
        elif provider == "qwen":
            # TODO: 实现 Qwen Embedding 封装
            logger.warning("Qwen Embedding 封装待实现，当前使用 OpenAI 接口")
            return OpenAIEmbeddings(
                model="text-embedding-ada-002",  # 临时使用
                openai_api_key=api_key,
            )
        elif provider == "deepseek":
            # TODO: 实现 DeepSeek Embedding 封装
            logger.warning("DeepSeek Embedding 封装待实现，当前使用 OpenAI 接口")
            return OpenAIEmbeddings(
                model="text-embedding-ada-002",  # 临时使用
                openai_api_key=api_key,
            )
        else:
            raise ValueError(f"不支持的 Embedding 提供商: {provider}")

    def get_embedding(self) -> Embeddings:
        """
        获取 Embedding 实例。

        Returns:
            Embedding 实例
        """
        return self._embedding

    def reload(self):
        """重新加载配置并创建新的 Embedding 实例。"""
        self._config = load_model_config()
        self._embedding = self._create_embedding()
        logger.info("Embedding 配置已重新加载")


def get_embedding() -> Embeddings:
    """
    获取 Embedding 实例的便捷函数。

    Returns:
        Embedding 实例
    """
    factory = EmbeddingFactory()
    return factory.get_embedding()

