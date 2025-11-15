"""
LLM 工厂类

通过抽象层实现模型切换，支持 DeepSeek、Qwen、OpenAI 等。
"""

from typing import Any, Dict
from langchain.llms.base import BaseLLM
from langchain_openai import ChatOpenAI
from hikebutler.config.loader import load_model_config
import logging

logger = logging.getLogger(__name__)


class LLMFactory:
    """LLM 工厂类，负责创建和管理 LLM 实例。"""

    _instance: "LLMFactory" = None
    _llm: BaseLLM = None
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
            self._llm = self._create_llm()

    def _create_llm(self) -> BaseLLM:
        """
        根据配置创建 LLM 实例。

        Returns:
            LLM 实例

        Raises:
            ValueError: 不支持的模型提供商
        """
        llm_config = self._config.get("llm", {})
        provider = llm_config.get("provider", "deepseek")
        model_name = llm_config.get("model_name", "deepseek-chat")
        api_key = llm_config.get("api_key")
        temperature = llm_config.get("temperature", 0.7)
        max_tokens = llm_config.get("max_tokens", 2000)

        if not api_key:
            raise ValueError(f"未配置 {provider} API Key")

        # 根据提供商创建不同的 LLM 实例
        if provider == "openai":
            return ChatOpenAI(
                model=model_name,
                api_key=api_key,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        elif provider == "deepseek":
            # TODO: 实现 DeepSeek LLM 封装
            # 可以使用 langchain_community 或自定义封装
            logger.warning("DeepSeek LLM 封装待实现，当前使用 OpenAI 接口")
            return ChatOpenAI(
                model="gpt-3.5-turbo",  # 临时使用
                api_key=api_key,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        elif provider == "qwen":
            # TODO: 实现 Qwen LLM 封装
            logger.warning("Qwen LLM 封装待实现，当前使用 OpenAI 接口")
            return ChatOpenAI(
                model="gpt-3.5-turbo",  # 临时使用
                api_key=api_key,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        else:
            raise ValueError(f"不支持的 LLM 提供商: {provider}")

    def get_llm(self) -> BaseLLM:
        """
        获取 LLM 实例。

        Returns:
            LLM 实例
        """
        return self._llm

    def reload(self):
        """重新加载配置并创建新的 LLM 实例。"""
        self._config = load_model_config()
        self._llm = self._create_llm()
        logger.info("LLM 配置已重新加载")


def get_llm() -> BaseLLM:
    """
    获取 LLM 实例的便捷函数。

    Returns:
        LLM 实例
    """
    factory = LLMFactory()
    return factory.get_llm()

