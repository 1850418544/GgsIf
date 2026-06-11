"""
企业微信通知模块
支持发送文本消息和文件消息到企业微信机器人
"""
import requests
import json
from utils.logger import logger

class WeChatWorkNotifier:
    """企业微信通知类"""
    
    def __init__(self, webhook_url):
        """初始化企业微信通知器
        参数：
            webhook_url (str): 企业微信机器人的Webhook地址
        使用示例：
            notifier = WeChatWorkNotifier("https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx")
        """
        self.webhook_url = webhook_url
    
    def send_text(self, content):
        """发送文本消息
        参数：
            content (str): 消息内容
        返回：
            dict: 接口响应数据
        使用示例：
            notifier.send_text("测试完成! 通过5个接口,失败0个")
        """
        data = {
            "msgtype": "text",
            "text": {
                "content": content
            }
        }
        
        try:
            response = requests.post(
                self.webhook_url,
                headers={"Content-Type": "application/json"},
                data=json.dumps(data),
                verify=False  # 跳过SSL证书验证(解决企业微信证书问题)
            )
            response.raise_for_status()  # 检查HTTP状态码是否为2xx
            result = response.json()
            
            if result.get("errcode") == 0:
                logger.info("企业微信文本消息发送成功")
            else:
                logger.error(f"企业微信文本消息发送失败: {result.get('errmsg')}")
            
            return result
        except Exception as e:
            logger.error(f"发送企业微信消息失败: {e}")
            return {"errcode": -1, "errmsg": str(e)}
    
    def send_markdown(self, content):
        """发送Markdown消息
        参数：
            content (str): Markdown格式的消息内容
        返回：
            dict: 接口响应
        使用示例：
            notifier.send_markdown("## 测试报告\n\n- 通过: 5\n- 失败: 0")
        """
        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": content
            }
        }
        
        try:
            response = requests.post(
                self.webhook_url,
                headers={"Content-Type": "application/json"},
                data=json.dumps(data),
                verify=False  # 跳过SSL证书验证(解决企业微信证书问题)
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get("errcode") == 0:
                logger.info("企业微信Markdown消息发送成功")
            else:
                logger.error(f"企业微信Markdown消息发送失败: {result.get('errmsg')}")
            
            return result
        except Exception as e:
            logger.error(f"发送企业微信Markdown消息失败: {e}")
            return {"errcode": -1, "errmsg": str(e)}
    
    def send_file(self, file_path):
        """发送文件消息
        
        参数：
            file_path (str): 文件路径
        
        返回：
            dict: 接口响应
        
        使用示例：
            notifier.send_file("reports/test_summary.txt")
        """
        try:
            import os
            
            # 检查文件是否存在且大小不超过20MB(企业微信限制)
            if not os.path.exists(file_path):
                logger.error(f"文件不存在: {file_path}")
                return {"errcode": -1, "errmsg": "文件不存在"}
            
            file_size = os.path.getsize(file_path)
            if file_size > 20 * 1024 * 1024:
                logger.error(f"文件大小超过20MB限制: {file_size} bytes")
                return {"errcode": -1, "errmsg": "文件大小超过20MB限制"}
            
            # 1. 先上传文件获取media_id(需要添加type参数)
            upload_url = self.webhook_url.replace("/send?", "/upload_media?type=file")
            
            with open(file_path, "rb") as f:
                files = {"file": f}
                upload_response = requests.post(upload_url, files=files, verify=False)
                upload_response.raise_for_status()
                upload_result = upload_response.json()
            
            if upload_result.get("errcode") != 0:
                logger.error(f"上传文件失败: {upload_result.get('errmsg')}")
                return upload_result
            
            media_id = upload_result.get("media_id")
            
            # 2. 发送文件消息
            data = {
                "msgtype": "file",
                "file": {
                    "media_id": media_id
                }
            }
            
            response = requests.post(
                self.webhook_url,
                headers={"Content-Type": "application/json"},
                data=json.dumps(data),
                verify=False  # 跳过SSL证书验证(解决企业微信证书问题)
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get("errcode") == 0:
                logger.info("企业微信文件消息发送成功")
            else:
                logger.error(f"企业微信文件消息发送失败: {result.get('errmsg')}")
            
            return result
        except Exception as e:
            logger.error(f"发送企业微信文件失败: {e}")
            return {"errcode": -1, "errmsg": str(e)}
    
    def send_test_report(self, test_results, txt_report_path):
        """发送测试报告摘要到企业微信
        
        参数：
            test_results (list): 测试结果列表
            txt_report_path (str): TXT报告文件路径
        
        使用示例：
            notifier.send_test_report(test_results, "reports/test_summary.txt")
        """
        # 计算统计数据
        total = len(test_results)
        passed = sum(1 for r in test_results if r.get("result") == "PASS")
        failed = total - passed
        
        # 筛选报错的接口(状态码为500或其他错误状态码)
        error_interfaces = [r for r in test_results if r.get("actual_status") in [500, 502, 503, 404, 403, 401]]
        
        # 构建简洁的Markdown报告
        markdown_content = f"""## 🧪 接口自动化测试报告

**测试时间**: {test_results[0].get('test_time', '未知') if test_results else '未知'}

### 📊 测试统计
- 总接口数: {total}
- 成功接口: {passed}
- 失败接口: {failed}
"""
        
        # 如果有报错接口,列出详情
        if error_interfaces:
            markdown_content += "\n### ❌ 报错接口详情\n"
            for idx, result in enumerate(error_interfaces, 1):
                markdown_content += f"""{idx}. **{result.get('case_name', '未知')}**
> - URL: {result.get('url', '')}
> - 状态码: {result.get('actual_status', '')}
> - 响应: {result.get('actual_response', '')[:50]}
"""
        
        markdown_content += "\n*报告由自动化测试框架自动发送*"
        
        # 发送Markdown消息(始终发送)
        self.send_markdown(markdown_content)
        
        # 发送TXT文件(可选,失败不影响主流程)
        if txt_report_path:
            file_result = self.send_file(txt_report_path)
            if file_result.get("errcode") != 0:
                logger.warning(f"TXT文件发送失败,已跳过")
