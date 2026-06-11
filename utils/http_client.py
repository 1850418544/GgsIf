"""
HTTP客户端模块
封装requests库，提供统一的HTTP请求接口
支持GET、POST、PUT、DELETE、PATCH等请求方法
自动处理超时和异常情况
"""
import requests
import time
from config.config import Config
from utils.logger import logger

class HttpClient:
    """HTTP客户端类，封装常用的HTTP请求方法"""
    
    def __init__(self, base_url=None):
        """初始化HTTP客户端
        
        参数：
            base_url (str, 可选): API基础地址，默认为Config.BASE_URL
        
        使用示例：
            # 使用默认配置
            client = HttpClient()
            
            # 使用自定义地址
            client = HttpClient(base_url="https://api.example.com")
        """
        # 设置基础URL
        self.base_url = base_url or Config.BASE_URL
        
        # 创建会话对象，可保持连接复用
        # 创建一个requests会话对象，用于保持连接复用
        # 会话对象可以：1. 复用TCP连接(提升性能) 2. 保持cookies 3. 共享请求头配置
        # 用法：self.session.get() / self.session.post() 等方式发送请求
        self.session = requests.Session()
        # 设置默认请求头
        self.session.headers.update(Config.HEADERS)
        # 禁用SSL证书验证(测试环境使用，生产环境建议启用)
        self.session.verify = False
        
        # 存储token
        self.token = None
    
    def set_token(self, token):
        """设置认证token
        
        参数：
            token (str): JWT token字符串
        
        使用示例：
            client.set_token("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
        """
        self.token = token
        self.session.headers.update({"Authorization": f"Bearer {token}"})
    
    def clear_token(self):
        """清除token，恢复匿名访问状态"""
        self.token = None
        if "Authorization" in self.session.headers:
            del self.session.headers["Authorization"]
    
    def request(self, method, endpoint, params=None, json=None, headers=None, timeout=None):
        """发送HTTP请求(通用方法)
        
        参数：
            method (str): HTTP方法，如GET、POST、PUT、DELETE
            endpoint (str): API端点路径，如"/api/user/login"
            params (dict, 可选): URL查询参数
            json (dict, 可选): 请求体JSON数据
            headers (dict, 可选): 自定义请求头
            timeout (int, 可选): 超时时间，默认使用Config.TIMEOUT
        
        返回：
            dict: 包含以下键的字典
                - status_code: HTTP状态码
                - response: 响应JSON数据(如果响应是JSON)
                - response_text: 响应文本
                - elapsed_time: 响应时间(毫秒)
                - headers: 响应头
                - error: 错误信息(如果有)
        
        使用示例：
            response = client.request("POST", "/api/login", json={"username": "test"})
            if response["status_code"] == 200:
                print(response["response"])
        """
        # 拼接完整URL
        url = f"{self.base_url}{endpoint}"
        # 设置超时时间
        timeout = timeout or Config.TIMEOUT
        
        # 记录开始时间
        start_time = time.time()
        
        try:
            # 记录请求日志
            logger.info(f"发送请求: {method} {url}")
            logger.debug(f"请求参数: {json or params}")
            
            # 更新请求头(如果有自定义头)
            if headers:
                self.session.headers.update(headers)
            
            # 发送请求
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=json,
                timeout=timeout,
                verify=False  # 禁用SSL验证
            )
            
            # 计算响应时间(毫秒)
            elapsed_time = (time.time() - start_time) * 1000
            
            # 记录响应日志
            logger.info(f"请求完成: {response.status_code} - {elapsed_time:.2f}ms")
            logger.debug(f"响应内容: {response.text[:500]}")  # 最多显示500字符
            
            # 返回响应结果
            return {
                "status_code": response.status_code,
                "response": response.json() if response.content else {},
                "response_text": response.text,
                "elapsed_time": elapsed_time,
                "headers": dict(response.headers)
            }
            
        except requests.exceptions.Timeout:
            # 处理超时异常
            elapsed_time = (time.time() - start_time) * 1000
            logger.error(f"请求超时: {url}")
            return {
                "status_code": None,
                "response": {},
                "response_text": "Request Timeout",
                "elapsed_time": elapsed_time,
                "error": "Request Timeout"
            }
        except requests.exceptions.RequestException as e:
            # 处理其他请求异常
            elapsed_time = (time.time() - start_time) * 1000
            logger.error(f"请求失败: {e}")
            return {
                "status_code": None,
                "response": {},
                "response_text": str(e),
                "elapsed_time": elapsed_time,
                "error": str(e)
            }
    
    def get(self, endpoint, params=None, **kwargs):
        """发送GET请求
        
        参数：
            endpoint (str): API端点路径
            params (dict, 可选): URL查询参数
            **kwargs: 其他可选参数(headers, timeout等)
        
        使用示例：
            response = client.get("/api/users", params={"page": 1, "size": 10})
        """
        return self.request("GET", endpoint, params=params, **kwargs)
    
    def post(self, endpoint, json=None, **kwargs):
        """发送POST请求
        
        参数：
            endpoint (str): API端点路径
            json (dict, 可选): 请求体JSON数据
            **kwargs: 其他可选参数(headers, timeout等)
        
        使用示例：
            response = client.post("/api/login", json={"username": "fan", "password": "fan123"})
        """
        return self.request("POST", endpoint, json=json, **kwargs)
    
    def put(self, endpoint, json=None, **kwargs):
        """发送PUT请求
        
        参数：
            endpoint (str): API端点路径
            json (dict, 可选): 请求体JSON数据
            **kwargs: 其他可选参数(headers, timeout等)
        
        使用示例：
            response = client.put("/api/users/1", json={"name": "newname"})
        """
        return self.request("PUT", endpoint, json=json, **kwargs)
    
    def delete(self, endpoint, **kwargs):
        """发送DELETE请求
        
        参数：
            endpoint (str): API端点路径
            **kwargs: 其他可选参数(headers, timeout等)
        
        使用示例：
            response = client.delete("/api/users/1")
        """
        return self.request("DELETE", endpoint, **kwargs)
    
    def patch(self, endpoint, json=None, **kwargs):
        """发送PATCH请求
        
        参数：
            endpoint (str): API端点路径
            json (dict, 可选): 请求体JSON数据
            **kwargs: 其他可选参数(headers, timeout等)
        
        使用示例：
            response = client.patch("/api/users/1", json={"name": "updated"})
        """
        return self.request("PATCH", endpoint, json=json, **kwargs)