"""
节点测试
"""

import pytest
from hikebutler.state import HikeButlerState
from hikebutler.nodes.route_node import route_node
from hikebutler.nodes.weather_node import weather_node


def test_route_node():
    """测试路线规划节点。"""
    state: HikeButlerState = {
        "messages": [],
        "user_profile": None,
        "user_id": "test_user",
        "intermediate_results": {},
        "current_task": "preparation",
        "input_data": {"location": "北京香山"},
        "output_data": None,
    }

    result = route_node(state)
    assert "route" in result["intermediate_results"]


def test_weather_node():
    """测试天气查询节点。"""
    state: HikeButlerState = {
        "messages": [],
        "user_profile": None,
        "user_id": "test_user",
        "intermediate_results": {},
        "current_task": "preparation",
        "input_data": {"location": "北京香山"},
        "output_data": None,
    }

    result = weather_node(state)
    assert "weather" in result["intermediate_results"]

