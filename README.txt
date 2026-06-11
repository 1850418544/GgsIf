=======================================================
         API 接口自动化测试框架
=======================================================

项目简介
--------
基于 Python + pytest 构建的接口自动化测试框架，支持多环境配置、
多种报告生成和多渠道通知。

主要特性
--------
- 接口测试：基于 pytest 的自动化测试框架
- 多格式报告：Excel、TXT、Allure 三种报告格式
- 多渠道通知：企业微信机器人、邮件通知
- 灵活配置：支持环境变量和 .env 文件配置
- 清晰结构：模块化设计，易于扩展和维护

环境要求
--------
- Python >= 3.8
- 依赖包见 requirements.txt

安装步骤
--------
1. 克隆项目（或直接下载）
   git clone <repository-url>
   cd GgsIf

2. 安装依赖
   pip install -r requirements.txt

3. 配置环境变量
   cp .env.example .env
   编辑 .env 文件，配置邮箱、企业微信等参数

使用方法
--------
快速运行：
  python main.py

其他方式：
  pytest testcases/ -v                  # 直接运行 pytest
  pytest testcases/test_auth_login.py   # 运行指定测试文件
  python main.py -k "login"             # 运行包含 login 的测试

项目结构
--------
GgsIf/
├── config/              # 配置模块
│   └── config.py        # 全局配置类
├── testcases/           # 测试用例
│   ├── test_auth_login.py    # 登录模块测试
│   └── test_home_page.py     # 首页模块测试
├── utils/               # 工具模块
│   ├── http_client.py       # HTTP 请求封装
│   ├── logger.py            # 日志管理
│   ├── excel_reporter.py    # Excel 报告生成
│   ├── txt_reporter.py      # TXT 报告生成
│   ├── wechat_notifier.py   # 企业微信通知
│   └── email_notifier.py    # 邮件通知
├── .env                  # 环境变量配置
├── .env.example          # 环境变量模板
├── conftest.py           # pytest 钩子函数
├── main.py               # 项目入口
├── pytest.ini            # pytest 配置
└── requirements.txt      # 依赖清单

配置说明
--------
环境变量配置（.env 文件）：
  API_BASE_URL=https://pehss.sfrtlce.cn/service-boss
  API_TIMEOUT=30
  TEST_USERNAME=fan
  TEST_PASSWORD=fan123
  
  # 企业微信通知
  SEND_WECHAT_NOTIFICATION=true
  WECHAT_WEBHOOK_URL=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx
  
  # 邮件通知
  SEND_EMAIL_NOTIFICATION=true
  SMTP_HOST=smtp.163.com
  SMTP_PORT=465
  SMTP_USER=your_email@163.com
  SMTP_PASS=your_auth_code
  EMAIL_TO=recipient@example.com

通知配置
--------
企业微信通知：
  1. 在企业微信群中添加「群机器人」
  2. 获取 Webhook 地址
  3. 在 .env 中配置相关参数

邮件通知：
  支持 QQ 邮箱、163 邮箱、Gmail 等
  需要配置 SMTP 服务器和授权码

报告生成
--------
报告类型：
  - Excel 报告：reports/test_report_YYYYMMDD_HHMMSS.xlsx
  - TXT 报告：reports/test_summary.txt
  - Allure 报告：reports/allure-results/

查看 Allure 报告：
  allure generate reports/allure-results -o reports/allure-report --clean
  allure serve reports/allure-results

部署到服务器
------------
1. 上传代码到服务器
   scp -r . user@server:/path/to/project

2. 安装依赖
   cd /path/to/project
   pip install -r requirements.txt

3. 配置环境变量并运行
   python main.py

定时任务示例：
  crontab -e
  0 8 * * * cd /path/to/project && python main.py >> logs/cron.log 2>&1

=======================================================
