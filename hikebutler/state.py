"""
LangGraph State 定义

使用 TypedDict 定义状态结构，包含用户画像和中间结果。
"""

from typing import TypedDict, List, Dict, Any, Optional
from langgraph.graph.message import add_messages


class HikeButlerState(TypedDict):
    """
    HikeButler Agent 的状态定义。

    Attributes:
        messages: 消息列表，用于与 LLM 交互
        user_profile: 用户画像（JSON 格式）
        user_id: 用户 ID
        intermediate_results: 中间结果字典
        current_task: 当前任务类型（preparation 或 review）
        input_data: 用户输入数据
        output_data: 最终输出数据
    """

    messages: List[Any]
    user_profile: Optional[Dict[str, Any]]
    user_id: Optional[str]
    intermediate_results: Dict[str, Any]
    current_task: Optional[str]  # "preparation" 或 "review"
    input_data: Optional[Dict[str, Any]]
    output_data: Optional[Dict[str, Any]]

