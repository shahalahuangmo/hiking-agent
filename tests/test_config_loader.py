"""
配置加载器测试
"""

import pytest
from pathlib import Path
from hikebutler.config.loader import load_config, load_model_config


def test_load_config():
    """测试配置加载。"""
    config = load_config()
    assert config is not None
    assert "app" in config
    assert "langgraph" in config


def test_load_model_config():
    """测试模型配置加载。"""
    model_config = load_model_config()
    assert model_config is not None
    assert "llm" in model_config
    assert "embedding" in model_config

