"""
LangGraph 工作流定义

定义准备阶段和复盘阶段的工作流。
"""

from typing import Literal
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langsmith import traceable

from hikebutler.state import HikeButlerState
from hikebutler.nodes import (
    route_node,
    weather_node,
    gear_node,
    photo_plan_node,
    fusion_node,
    post_gen_node,
    xhs_node,
)
from hikebutler.tools.mcp_tools import mcp_windy_fetch, mcp_xhs_post
import logging

logger = logging.getLogger(__name__)


@traceable(name="hikebutler_workflow")
def create_preparation_workflow() -> StateGraph:
    """
    创建徒步准备阶段的工作流。

    Returns:
        LangGraph StateGraph 实例
    """
    # 定义工具列表
    tools = [mcp_windy_fetch]

    # 创建工具节点
    tool_node = ToolNode(tools)

    # 创建工作流图
    workflow = StateGraph(HikeButlerState)

    # 添加节点
    workflow.add_node("route", route_node)
    workflow.add_node("weather", weather_node)
    workflow.add_node("gear", gear_node)
    workflow.add_node("photo_plan", photo_plan_node)
    workflow.add_node("fusion", fusion_node)
    workflow.add_node("tools", tool_node)

    # 设置入口点
    workflow.set_entry_point("route")

    # 添加边
    workflow.add_edge("route", "weather")
    workflow.add_edge("weather", "gear")
    workflow.add_edge("gear", "photo_plan")
    workflow.add_edge("photo_plan", "fusion")
    workflow.add_edge("fusion", END)

    # 条件边（如果需要）
    # workflow.add_conditional_edges(
    #     "tools",
    #     should_continue,
    #     {
    #         "continue": "fusion",
    #         "end": END,
    #     },
    # )

    return workflow.compile()


@traceable(name="hikebutler_review_workflow")
def create_review_workflow() -> StateGraph:
    """
    创建徒步复盘阶段的工作流。

    Returns:
        LangGraph StateGraph 实例
    """
    # 定义工具列表
    tools = [mcp_xhs_post]

    # 创建工具节点
    tool_node = ToolNode(tools)

    # 创建工作流图
    workflow = StateGraph(HikeButlerState)

    # 添加节点
    workflow.add_node("post_gen", post_gen_node)
    workflow.add_node("xhs", xhs_node)
    workflow.add_node("tools", tool_node)

    # 设置入口点
    workflow.set_entry_point("post_gen")

    # 添加边
    workflow.add_edge("post_gen", "xhs")
    workflow.add_edge("xhs", END)

    return workflow.compile()


def should_continue(state: HikeButlerState) -> Literal["continue", "end"]:
    """
    判断是否继续执行工作流。

    Args:
        state: 当前状态

    Returns:
        "continue" 或 "end"
    """
    # TODO: 实现条件判断逻辑
    return "end"

