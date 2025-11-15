"""
Gradio UI 应用

提供"徒步准备"和"徒步复盘"两个页面的交互界面。
"""

import gradio as gr
from typing import Dict, Any, Tuple, List
from hikebutler.graph.workflow import (
    create_preparation_workflow,
    create_review_workflow,
)
from hikebutler.state import HikeButlerState
import logging

try:
    import pandas as pd
except ImportError:
    # 如果没有 pandas，使用列表作为替代
    pd = None

logger = logging.getLogger(__name__)

# 初始化工作流
preparation_workflow = create_preparation_workflow()
review_workflow = create_review_workflow()


def prepare_hiking(
    location: str,
    duration: str,
    difficulty: str,
    user_id: str = "default_user",
) -> Tuple[Any, str]:
    """
    处理徒步准备请求。

    Args:
        location: 徒步地点
        duration: 期望时长
        difficulty: 难度偏好
        user_id: 用户 ID

    Returns:
        (装备清单 DataFrame, 徒步计划)
    """
    try:
        # 构建初始状态
        initial_state: HikeButlerState = {
            "messages": [],
            "user_profile": None,
            "user_id": user_id,
            "intermediate_results": {},
            "current_task": "preparation",
            "input_data": {
                "location": location,
                "duration": duration,
                "difficulty": difficulty,
            },
            "output_data": None,
        }

        # 执行工作流
        result = preparation_workflow.invoke(initial_state)

        # 提取结果
        output_data = result.get("output_data", {})
        gear_list_data = output_data.get("gear_list", [])
        plan = output_data.get("plan", "徒步计划生成中...")

        # 将装备清单转换为 DataFrame 或列表格式
        if pd is not None:
            if isinstance(gear_list_data, list):
                if len(gear_list_data) > 0 and isinstance(gear_list_data[0], dict):
                    # 如果是字典列表，转换为 DataFrame
                    gear_df = pd.DataFrame(gear_list_data)
                elif len(gear_list_data) > 0 and isinstance(gear_list_data[0], list):
                    # 如果是列表的列表，转换为 DataFrame
                    gear_df = pd.DataFrame(gear_list_data, columns=["装备名称", "数量", "备注"])
                else:
                    # 默认空 DataFrame
                    gear_df = pd.DataFrame(columns=["装备名称", "数量", "备注"])
            else:
                # 默认空 DataFrame
                gear_df = pd.DataFrame(columns=["装备名称", "数量", "备注"])
            gear_result = gear_df
        else:
            # 如果没有 pandas，返回列表格式
            if isinstance(gear_list_data, list):
                gear_result = gear_list_data
            else:
                gear_result = [["装备清单生成中...", "", ""]]

        return gear_result, plan

    except Exception as e:
        logger.error(f"徒步准备处理失败: {e}")
        if pd is not None:
            error_df = pd.DataFrame(columns=["装备名称", "数量", "备注"])
            return error_df, f"错误: {str(e)}"
        else:
            return [["错误", str(e), ""]], f"错误: {str(e)}"


def review_hiking(
    gpx_file: Any,
    photos: Any,
    thoughts: str,
    user_id: str = "default_user",
) -> Tuple[str, str]:
    """
    处理徒步复盘请求。

    Args:
        gpx_file: GPX 轨迹文件
        photos: 照片文件列表
        thoughts: 个人感想
        user_id: 用户 ID

    Returns:
        (帖子预览, 发布状态)
    """
    try:
        # 读取 GPX 文件
        gpx_content = None
        if gpx_file:
            with open(gpx_file.name, "r", encoding="utf-8") as f:
                gpx_content = f.read()

        # 构建初始状态
        initial_state: HikeButlerState = {
            "messages": [],
            "user_profile": None,
            "user_id": user_id,
            "intermediate_results": {},
            "current_task": "review",
            "input_data": {
                "gpx": gpx_content,
                "photos": photos,
                "thoughts": thoughts,
            },
            "output_data": None,
        }

        # 执行工作流
        result = review_workflow.invoke(initial_state)

        # 提取结果
        output_data = result.get("output_data", {})
        post = output_data.get("post", "帖子生成中...")
        xhs_status = output_data.get("xhs_status", {}).get("message", "待发布")

        return post, xhs_status

    except Exception as e:
        logger.error(f"徒步复盘处理失败: {e}")
        return f"错误: {str(e)}", ""


def create_ui():
    """
    创建 Gradio UI 界面。

    Returns:
        Gradio Interface 实例
    """
    # 创建 Tab 布局
    with gr.Blocks(title="HikeButler - 徒步私人管家") as app:
        gr.Markdown("# 🏔️ HikeButler - 徒步私人管家 AI Agent")

        with gr.Tabs():
            # 徒步准备页面
            with gr.Tab("徒步准备"):
                gr.Markdown("### 输入您的徒步偏好，AI 将为您生成个性化计划")
                with gr.Row():
                    with gr.Column():
                        location_input = gr.Textbox(
                            label="徒步地点",
                            placeholder="例如：北京香山",
                        )
                        duration_input = gr.Dropdown(
                            label="期望时长",
                            choices=["半天", "一天", "两天", "三天以上"],
                            value="一天",
                        )
                        difficulty_input = gr.Dropdown(
                            label="难度偏好",
                            choices=["简单", "中等", "困难", "极限"],
                            value="中等",
                        )
                        user_id_input = gr.Textbox(
                            label="用户 ID（可选）",
                            value="default_user",
                        )
                        prepare_btn = gr.Button("生成徒步计划", variant="primary")

                    with gr.Column():
                        gear_output = gr.Dataframe(
                            label="装备清单",
                            headers=["装备名称", "数量", "备注"],
                        )
                        plan_output = gr.Markdown(label="徒步计划")

                prepare_btn.click(
                    fn=prepare_hiking,
                    inputs=[location_input, duration_input, difficulty_input, user_id_input],
                    outputs=[gear_output, plan_output],
                )

            # 徒步复盘页面
            with gr.Tab("徒步复盘"):
                gr.Markdown("### 上传您的徒步轨迹和照片，AI 将为您生成复盘帖子")
                with gr.Row():
                    with gr.Column():
                        gpx_input = gr.File(
                            label="GPX 轨迹文件",
                            file_types=[".gpx"],
                        )
                        photos_input = gr.File(
                            label="照片（可多选）",
                            file_count="multiple",
                            file_types=["image"],
                        )
                        thoughts_input = gr.Textbox(
                            label="个人感想",
                            placeholder="分享您的徒步感受...",
                            lines=5,
                        )
                        review_user_id_input = gr.Textbox(
                            label="用户 ID（可选）",
                            value="default_user",
                        )
                        review_btn = gr.Button("生成复盘帖子", variant="primary")

                    with gr.Column():
                        post_output = gr.Markdown(label="生成的帖子")
                        xhs_status_output = gr.Textbox(label="发布状态")
                        publish_btn = gr.Button("发布到小红书", variant="secondary")

                review_btn.click(
                    fn=review_hiking,
                    inputs=[
                        gpx_input,
                        photos_input,
                        thoughts_input,
                        review_user_id_input,
                    ],
                    outputs=[post_output, xhs_status_output],
                )

    return app


def launch_ui(share: bool = False, server_name: str = "127.0.0.1", server_port: int = 7860):
    """
    启动 Gradio UI。

    Args:
        share: 是否创建公共链接
        server_name: 服务器地址
        server_port: 服务器端口
    """
    app = create_ui()
    app.launch(share=share, server_name=server_name, server_port=server_port)

