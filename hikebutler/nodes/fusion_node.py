"""
信息融合节点

将所有中间结果融合，生成最终的徒步计划。
"""

from typing import Dict, Any
from hikebutler.state import HikeButlerState


def fusion_node(state: HikeButlerState) -> HikeButlerState:
    """
    信息融合节点。

    将路线、天气、装备、拍摄计划等信息融合，生成完整的徒步计划。

    Args:
        state: 当前状态

    Returns:
        更新后的状态
    """
    # TODO: 实现信息融合逻辑
    # 1. 收集所有中间结果
    # 2. 调用 LLM 进行信息融合
    # 3. 生成 Markdown 格式的徒步计划
    # 4. 更新 state.output_data

    state["output_data"] = {
        "plan": "徒步计划融合功能待实现",
        "format": "markdown",
    }

    return state

