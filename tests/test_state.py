"""
State 测试
"""

from hikebutler.state import HikeButlerState


def test_state_structure():
    """测试 State 结构。"""
    state: HikeButlerState = {
        "messages": [],
        "user_profile": None,
        "user_id": "test_user",
        "intermediate_results": {},
        "current_task": "preparation",
        "input_data": {"location": "北京香山"},
        "output_data": None,
    }

    assert state["user_id"] == "test_user"
    assert state["current_task"] == "preparation"
    assert state["input_data"]["location"] == "北京香山"

