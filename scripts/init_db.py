"""
数据库初始化脚本

用于初始化 MySQL 数据库表结构。
"""

import sys
import logging
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from hikebutler.database.mysql_client import MySQLClient

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def main():
    """初始化数据库。"""
    try:
        logger.info("开始初始化数据库...")
        client = MySQLClient()
        client.connect()
        client.init_tables()
        client.close()
        logger.info("数据库初始化完成！")
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

