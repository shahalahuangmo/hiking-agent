"""
ChromaDB 连接诊断脚本
用于诊断 httpx 与 ChromaDB 服务器的兼容性问题
"""

import sys
import logging
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def test_with_requests():
    """使用 requests 库测试连接"""
    try:
        import requests
        logger.info("=" * 60)
        logger.info("测试 1: 使用 requests 库")
        logger.info("=" * 60)
        
        url = "http://localhost:8000/api/v2/auth/identity"
        response = requests.get(url, timeout=5)
        logger.info(f"✓ 状态码: {response.status_code}")
        logger.info(f"✓ 响应: {response.json()}")
        return True
    except Exception as e:
        logger.error(f"✗ 失败: {e}")
        return False


def test_with_httpx():
    """使用 httpx 库测试连接"""
    try:
        import httpx
        logger.info("=" * 60)
        logger.info("测试 2: 使用 httpx 库（默认配置）")
        logger.info("=" * 60)
        
        url = "http://localhost:8000/api/v2/auth/identity"
        response = httpx.get(url, timeout=5.0)
        logger.info(f"✓ 状态码: {response.status_code}")
        logger.info(f"✓ 响应: {response.json()}")
        return True
    except Exception as e:
        logger.error(f"✗ 失败: {e}")
        return False


def test_with_httpx_http11():
    """使用 httpx 强制 HTTP/1.1"""
    try:
        import httpx
        logger.info("=" * 60)
        logger.info("测试 3: 使用 httpx（强制 HTTP/1.1）")
        logger.info("=" * 60)
        
        url = "http://localhost:8000/api/v2/auth/identity"
        # 强制使用 HTTP/1.1
        client = httpx.Client(http2=False)
        response = client.get(url, timeout=5.0)
        logger.info(f"✓ 状态码: {response.status_code}")
        logger.info(f"✓ 响应: {response.json()}")
        client.close()
        return True
    except Exception as e:
        logger.error(f"✗ 失败: {e}")
        return False


def test_chromadb_client():
    """测试 ChromaDB 客户端"""
    try:
        import chromadb
        from chromadb.config import Settings
        
        logger.info("=" * 60)
        logger.info("测试 4: ChromaDB HttpClient")
        logger.info("=" * 60)
        
        # 方法 1: 默认设置
        try:
            logger.info("尝试: 默认设置")
            client = chromadb.HttpClient(
                host="localhost",
                port=8000,
                settings=Settings(anonymized_telemetry=False),
            )
            version = client.get_version()
            logger.info(f"✓ 成功！版本: {version}")
            return True
        except Exception as e1:
            logger.warning(f"默认设置失败: {e1}")
            
            # 方法 2: 无 settings
            try:
                logger.info("尝试: 无 settings 参数")
                client = chromadb.HttpClient(host="localhost", port=8000)
                version = client.get_version()
                logger.info(f"✓ 成功！版本: {version}")
                return True
            except Exception as e2:
                logger.error(f"✗ 也失败了: {e2}")
                return False
    except Exception as e:
        logger.error(f"✗ ChromaDB 客户端创建失败: {e}")
        return False


def test_with_custom_httpx_client():
    """使用自定义 httpx 客户端测试 ChromaDB"""
    try:
        import chromadb
        from chromadb.config import Settings
        import httpx
        
        logger.info("=" * 60)
        logger.info("测试 5: ChromaDB + 自定义 httpx 客户端")
        logger.info("=" * 60)
        
        # 创建自定义 httpx 客户端
        http_client = httpx.Client(
            http2=False,  # 禁用 HTTP/2
            timeout=10.0,
            follow_redirects=True,
        )
        
        # 注意：ChromaDB 的 HttpClient 不直接支持传入自定义 httpx 客户端
        # 这里只是演示概念
        logger.info("⚠️  ChromaDB HttpClient 不支持传入自定义 httpx 客户端")
        logger.info("   这可能是问题的根源")
        
        http_client.close()
        return False
    except Exception as e:
        logger.error(f"✗ 失败: {e}")
        return False


def main():
    """运行所有诊断测试"""
    logger.info("\n" + "=" * 60)
    logger.info("ChromaDB 连接诊断")
    logger.info("=" * 60 + "\n")
    
    results = {}
    
    # 测试 1: requests
    results["requests"] = test_with_requests()
    print()
    
    # 测试 2: httpx 默认
    results["httpx_default"] = test_with_httpx()
    print()
    
    # 测试 3: httpx HTTP/1.1
    results["httpx_http11"] = test_with_httpx_http11()
    print()
    
    # 测试 4: ChromaDB 客户端
    results["chromadb_client"] = test_chromadb_client()
    print()
    
    # 测试 5: 自定义 httpx
    results["custom_httpx"] = test_with_custom_httpx_client()
    print()
    
    # 总结
    logger.info("=" * 60)
    logger.info("诊断结果总结")
    logger.info("=" * 60)
    for test_name, success in results.items():
        status = "✓ 成功" if success else "✗ 失败"
        logger.info(f"{test_name}: {status}")
    
    logger.info("\n" + "=" * 60)
    if results.get("requests") and not results.get("httpx_default"):
        logger.warning("发现问题：requests 成功，但 httpx 失败")
        logger.warning("这可能是 httpx 与 ChromaDB 服务器的兼容性问题")
        logger.warning("\n可能的解决方案：")
        logger.warning("1. 降级 httpx 版本: pip install 'httpx<0.24.0'")
        logger.warning("2. 升级 chromadb: pip install --upgrade chromadb")
        logger.warning("3. 检查是否有代理设置干扰")
    elif not results.get("requests"):
        logger.error("基础连接失败，请检查 ChromaDB 服务是否正常运行")
    elif results.get("chromadb_client"):
        logger.info("✓ ChromaDB 客户端连接正常！")
    else:
        logger.warning("ChromaDB 客户端连接失败，但基础连接正常")
        logger.warning("建议检查 chromadb 库的版本兼容性")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()

