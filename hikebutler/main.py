"""
HikeButler 主程序入口

启动 Gradio UI 和初始化服务。
"""

import logging
import sys
from hikebutler.ui.gradio_app import launch_ui
from hikebutler.config.loader import load_config

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger(__name__)


def main():
    """主函数。"""
    try:
        # 加载配置
        config = load_config()
        app_config = config.get("app", {})
        app_name = app_config.get("name", "HikeButler")
        app_version = app_config.get("version", "0.1.0")

        logger.info(f"启动 {app_name} v{app_version}")

        # 启动 UI
        launch_ui(share=False, server_name="127.0.0.1", server_port=7860)

    except KeyboardInterrupt:
        logger.info("程序被用户中断")
    except Exception as e:
        logger.error(f"程序运行出错: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

