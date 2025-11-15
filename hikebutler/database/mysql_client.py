"""
MySQL 数据库客户端

负责用户画像和历史徒步数据的存储和查询。
"""

from typing import Dict, Any, Optional, List
import pymysql
from pymysql.connections import Connection
from pymysql.cursors import DictCursor
from hikebutler.config.loader import load_config
import logging

logger = logging.getLogger(__name__)


class MySQLClient:
    """MySQL 数据库客户端。"""

    def __init__(self):
        """初始化数据库连接配置。"""
        config = load_config()
        db_config = config.get("database", {}).get("mysql", {})
        self.host = db_config.get("host", "localhost")
        self.port = db_config.get("port", 3306)
        self.user = db_config.get("user", "root")
        self.password = db_config.get("password", "")
        self.database = db_config.get("database", "hikebutler")
        self.pool_size = db_config.get("pool_size", 5)
        self._connection: Optional[Connection] = None

    def connect(self):
        """建立数据库连接。"""
        try:
            self._connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                charset="utf8mb4",
                cursorclass=DictCursor,
            )
            logger.info("MySQL 连接成功")
        except Exception as e:
            logger.error(f"MySQL 连接失败: {e}")
            raise

    def close(self):
        """关闭数据库连接。"""
        if self._connection:
            self._connection.close()
            self._connection = None
            logger.info("MySQL 连接已关闭")

    def execute_query(self, sql: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """
        执行查询语句。

        Args:
            sql: SQL 查询语句
            params: 查询参数

        Returns:
            查询结果列表
        """
        if not self._connection:
            self.connect()

        try:
            with self._connection.cursor() as cursor:
                cursor.execute(sql, params)
                return cursor.fetchall()
        except Exception as e:
            logger.error(f"查询执行失败: {e}")
            raise

    def execute_update(self, sql: str, params: Optional[tuple] = None) -> int:
        """
        执行更新语句。

        Args:
            sql: SQL 更新语句
            params: 更新参数

        Returns:
            受影响的行数
        """
        if not self._connection:
            self.connect()

        try:
            with self._connection.cursor() as cursor:
                affected_rows = cursor.execute(sql, params)
                self._connection.commit()
                return affected_rows
        except Exception as e:
            self._connection.rollback()
            logger.error(f"更新执行失败: {e}")
            raise

    def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        获取用户画像。

        Args:
            user_id: 用户 ID

        Returns:
            用户画像字典，如果不存在则返回 None
        """
        sql = "SELECT profile_json FROM users WHERE id = %s"
        results = self.execute_query(sql, (user_id,))
        if results:
            return results[0].get("profile_json")
        return None

    def save_user_profile(self, user_id: str, profile: Dict[str, Any]):
        """
        保存用户画像。

        Args:
            user_id: 用户 ID
            profile: 用户画像字典
        """
        import json

        sql = """
            INSERT INTO users (id, profile_json)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE profile_json = %s
        """
        profile_json = json.dumps(profile, ensure_ascii=False)
        self.execute_update(sql, (user_id, profile_json, profile_json))

    def init_tables(self):
        """初始化数据库表结构。"""
        # 创建 users 表
        users_sql = """
            CREATE TABLE IF NOT EXISTS users (
                id VARCHAR(255) PRIMARY KEY,
                profile_json JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """

        # 创建 trips 表
        trips_sql = """
            CREATE TABLE IF NOT EXISTS trips (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(255),
                gpx TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """

        try:
            self.execute_update(users_sql)
            self.execute_update(trips_sql)
            logger.info("数据库表初始化成功")
        except Exception as e:
            logger.error(f"数据库表初始化失败: {e}")
            raise

