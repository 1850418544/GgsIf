# API 接口自动化测试框架

基于 Python + pytest 构建的接口自动化测试框架，支持多环境配置、多种报告生成和多渠道通知。

---

## ✨ 功能特性

- 🧪 **接口测试**：基于 pytest 的自动化测试框架
- 📊 **多格式报告**：Excel、TXT、Allure 三种报告格式
- 💬 **多渠道通知**：企业微信机器人、邮件通知
- 🔧 **灵活配置**：支持环境变量和 .env 文件配置
- 📁 **清晰结构**：模块化设计，易于扩展和维护

---

## 📋 环境要求

- Python >= 3.8
- 依赖包见 `requirements.txt`

---

## 🛠️ 安装步骤

```bash
# 1. 克隆项目（或直接下载）
git clone <repository-url>
cd GgsIf

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，配置邮箱、企业微信等参数
```

---

## 🚀 使用方法

### 快速运行

```bash
# 方式1：通过 main.py 运行（推荐）
python main.py

# 方式2：直接运行 pytest
pytest testcases/ -v

# 方式3：运行指定测试文件
pytest testcases/test_auth_login.py -v

# 方式4：生成 Allure 报告
pytest testcases/ --alluredir=reports/allure-results
```

### 命令行参数

```bash
# 运行所有测试
python main.py

# 运行指定测试（-k 参数过滤）
python main.py -k "login"

# 详细输出
python main.py -v

# 生成 Allure 报告（已在 pytest.ini 中配置）
python main.py
```

---

## 📁 项目结构

```
GgsIf/
├── config/              # 配置模块
│   ├── __init__.py
│   └── config.py        # 全局配置类
├── testcases/           # 测试用例
│   ├── __init__.py
│   ├── test_auth_login.py    # 登录模块测试
│   └── test_home_page.py     # 首页模块测试
├── utils/               # 工具模块
│   ├── __init__.py
│   ├── http_client.py       # HTTP 请求封装
│   ├── logger.py            # 日志管理
│   ├── excel_reporter.py    # Excel 报告生成
│   ├── txt_reporter.py      # TXT 报告生成
│   ├── wechat_notifier.py   # 企业微信通知
│   └── email_notifier.py    # 邮件通知
├── .env                  # 环境变量配置（需创建）
├── .env.example          # 环境变量模板
├── .gitignore            # Git 忽略配置
├── conftest.py           # pytest 钩子函数
├── main.py               # 项目入口
├── pytest.ini            # pytest 配置
├── requirements.txt      # 依赖清单
└── README.md             # 项目说明
```

---

## ⚙️ 配置说明

### 环境变量配置（.env 文件）

```ini
# API配置
API_BASE_URL=https://pehss.sfrtlce.cn/service-boss
API_TIMEOUT=30

# 测试账号
TEST_USERNAME=fan
TEST_PASSWORD=fan123

# 企业微信通知（可选）
SEND_WECHAT_NOTIFICATION=true
WECHAT_WEBHOOK_URL=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx

# 邮件通知（可选）
SEND_EMAIL_NOTIFICATION=true
SMTP_HOST=smtp.163.com
SMTP_PORT=465
SMTP_USER=your_email@163.com
SMTP_PASS=your_auth_code
EMAIL_TO=recipient@example.com

# 其他配置
GENERATE_ALLURE_REPORT=true
```

### 配置项说明

| 配置项 | 说明 | 默认值 |
|---|---|---|
| `API_BASE_URL` | API 基础地址 | - |
| `API_TIMEOUT` | 请求超时时间（秒） | 30 |
| `TEST_USERNAME` | 测试账号用户名 | fan |
| `TEST_PASSWORD` | 测试账号密码 | fan123 |
| `SEND_WECHAT_NOTIFICATION` | 是否启用企业微信通知 | false |
| `WECHAT_WEBHOOK_URL` | 企业微信机器人 Webhook | - |
| `SEND_EMAIL_NOTIFICATION` | 是否启用邮件通知 | false |
| `SMTP_HOST` | SMTP 服务器地址 | smtp.qq.com |
| `SMTP_PORT` | SMTP 端口 | 465 |
| `SMTP_USER` | 发件人邮箱 | - |
| `SMTP_PASS` | 邮箱授权码 | - |
| `EMAIL_TO` | 收件人邮箱（支持多个，逗号分隔） | - |

---

## 📧 通知配置

### 企业微信通知

1. 在企业微信群中添加「群机器人」
2. 获取 Webhook 地址
3. 在 `.env` 中配置：
   ```ini
   SEND_WECHAT_NOTIFICATION=true
   WECHAT_WEBHOOK_URL=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx
   ```

### 邮件通知

支持以下邮箱服务商：

| 邮箱 | SMTP 服务器 | 端口 |
|---|---|---|
| QQ 邮箱 | smtp.qq.com | 465 |
| 163 邮箱 | smtp.163.com | 465 |
| Gmail | smtp.gmail.com | 465 |

**配置示例（163 邮箱）**：
```ini
SEND_EMAIL_NOTIFICATION=true
SMTP_HOST=smtp.163.com
SMTP_PORT=465
SMTP_USER=your_email@163.com
SMTP_PASS=your_auth_code  # 授权码，非登录密码
EMAIL_TO=user1@qq.com,user2@example.com
```

---

## 📊 报告生成

### 报告类型

| 报告类型 | 路径 | 说明 |
|---|---|---|
| Excel 报告 | `reports/test_report_YYYYMMDD_HHMMSS.xlsx` | 详细测试结果表格 |
| TXT 报告 | `reports/test_summary.txt` | 简洁的测试摘要 |
| Allure 报告 | `reports/allure-results/` | 交互式 HTML 报告 |

### 查看 Allure 报告

```bash
# 生成 HTML 报告
allure generate reports/allure-results -o reports/allure-report --clean

# 启动预览服务
allure serve reports/allure-results
```

---

## 🐳 部署到服务器

### 方式一：手动部署

```bash
# 1. 上传代码到服务器
scp -r . user@server:/path/to/project

# 2. 安装依赖
cd /path/to/project
pip install -r requirements.txt

# 3. 配置环境变量
cp .env.example .env
# 编辑 .env 文件

# 4. 运行测试
python main.py
```

### 方式二：定时任务

```bash
# 编辑 crontab
crontab -e

# 添加定时任务（每天早上 8 点运行）
0 8 * * * cd /path/to/project && python main.py >> logs/cron.log 2>&1
```

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT License

---

## 📞 联系方式

如有问题，请联系项目维护者。
