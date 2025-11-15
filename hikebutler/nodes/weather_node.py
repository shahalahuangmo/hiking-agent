"""
天气查询节点

通过 MCP 工具调用 Windy API 获取天气预报。
"""

from typing import Dict, Any
from hikebutler.state import HikeButlerState


def weather_node(state: HikeButlerState) -> HikeButlerState:
    """
    天气查询节点。

    根据用户输入的徒步地点和时间，调用 MCP 工具获取天气预报。

    Args:
        state: 当前状态

    Returns:
        更新后的状态
    """
    # TODO: 实现天气查询逻辑
    # 1. 从 state 中提取地点和时间信息
    # 2. 调用 MCP 工具 mcp_windy_fetch
    # 3. 解析天气数据
    # 4. 更新 state.intermediate_results

    state["intermediate_results"]["weather"] = {
        "status": "pending",
        "message": "天气查询功能待实现",
    }

    return state

