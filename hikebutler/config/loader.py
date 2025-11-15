"""
配置加载器

负责加载和管理项目配置，支持环境变量替换。
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv


def load_config(config_path: str = "config/config.yaml") -> Dict[str, Any]:
    """
    加载配置文件，支持环境变量替换。

    Args:
        config_path: 配置文件路径

    Returns:
        配置字典
    """
    # 加载环境变量
    load_dotenv()

    config_file = Path(config_path)
    if not config_file.exists():
        raise FileNotFoundError(f"配置文件不存在: {config_path}")

    with open(config_file, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # 递归替换环境变量
    config = _replace_env_vars(config)

    return config


def load_model_config(config_path: str = "config/models.yaml") -> Dict[str, Any]:
    """
    加载模型配置文件。

    Args:
        config_path: 模型配置文件路径

    Returns:
        模型配置字典
    """
    load_dotenv()

    config_file = Path(config_path)
    if not config_file.exists():
        raise FileNotFoundError(f"模型配置文件不存在: {config_path}")

    with open(config_file, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # 替换环境变量
    config = _replace_env_vars(config)

    return config


def _replace_env_vars(obj: Any) -> Any:
    """
    递归替换配置中的环境变量。

    Args:
        obj: 配置对象

    Returns:
        替换后的配置对象
    """
    if isinstance(obj, dict):
        return {k: _replace_env_vars(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_replace_env_vars(item) for item in obj]
    elif isinstance(obj, str) and obj.startswith("${") and obj.endswith("}"):
        # 提取环境变量名
        env_var = obj[2:-1]
        return os.getenv(env_var, obj)
    else:
        return obj

