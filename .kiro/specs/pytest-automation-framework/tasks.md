# 实施计划：pytest 自动化测试框架

## 概述

基于设计文档的分层架构，按照 核心层 → 引擎层 → 测试用例层 → 插件层 → CI 集成 的顺序逐步实现。每个阶段完成后通过检查点验证，确保增量交付的正确性。

## 任务

- [x] 1. 搭建框架目录结构与基础配置
  - [x] 1.1 创建测试框架目录结构和 `__init__.py` 文件
    - 创建 `tests/` 下的所有子目录：`config/`、`fixtures/`、`utils/`、`pages/`、`testcases/api/`、`testcases/ui/`、`testcases/performance/`、`testcases/security/`、`testdata/`、`reports/`
    - 在每个 Python 包目录下创建 `__init__.py`
    - 在 `reports/` 下创建 `.gitkeep`
    - _需求: 1.1_

  - [x] 1.2 创建 `tests/pytest.ini` 配置文件
    - 配置 markers：api、ui、perf、security
    - 配置 addopts、testpaths
    - _需求: 1.2, 5.5, 6.5, 7.2_

  - [x] 1.3 更新 `requirements.txt`，添加测试依赖
    - 添加 pytest>=7.0、hypothesis>=6.0、pytest-html、allure-pytest、requests、playwright、PyYAML、locust
    - _需求: 1.2_

- [x] 2. 实现核心层组件
  - [x] 2.1 实现 `tests/utils/config_manager.py` 配置管理器
    - 实现 ConfigManager 类：`__init__`、`get`（支持点号嵌套 key）、`get_base_url`、`resolve_env`
    - 支持从 `--env` 命令行参数或 `TEST_ENV` 环境变量解析环境名
    - 环境名无效时回退到 dev 并记录 WARNING
    - 配置文件不存在时抛出 FileNotFoundError
    - _需求: 1.3, 1.4_

  - [x] 2.2 创建环境配置文件
    - 创建 `tests/config/config.yaml`（默认配置）
    - 创建 `tests/config/dev.yaml`（开发环境，base_url: http://localhost:5000）
    - 创建 `tests/config/staging.yaml` 和 `tests/config/prod.yaml`
    - _需求: 1.3_

  - [ ]* 2.3 编写 ConfigManager 属性测试
    - **Property 1: 配置加载与环境解析的正确性**
    - 使用 Hypothesis 生成随机环境名和嵌套字典配置数据，验证写入后加载的值与原始值一致
    - **验证需求: 1.3, 1.4**

  - [x] 2.4 实现 `tests/utils/data_driver.py` 数据驱动模块
    - 实现 DataDriver 类：`load_yaml`、`load_json`、`load_csv`、`load`（根据扩展名自动选择）
    - 不支持的格式抛出 ValueError
    - _需求: 2.7_

  - [ ]* 2.5 编写 DataDriver 属性测试
    - **Property 5: 数据驱动加载的往返一致性**
    - 使用 Hypothesis 生成随机字典列表，写入 YAML/JSON 后通过 DataDriver 加载，验证数据等价
    - **验证需求: 2.7**

  - [x] 2.6 实现 `tests/utils/logger.py` 日志模块
    - 实现 `setup_logger` 函数，支持控制台和文件双输出
    - 日志格式：`[时间戳] [级别] [名称] 消息`
    - 支持按日期分类日志文件
    - _需求: 4.4, 4.5_

  - [ ]* 2.7 编写 Logger 属性测试
    - **Property 6: 日志格式与错误堆栈的完整性**
    - 使用 Hypothesis 生成随机日志消息和级别，验证输出包含时间戳、级别和消息；对异常对象验证包含堆栈信息
    - **验证需求: 4.4, 4.5**

- [x] 3. 检查点 - 核心层验证
  - 确保所有测试通过，如有问题请向用户确认。

- [x] 4. 实现引擎层 - API 测试引擎
  - [x] 4.1 实现 `tests/utils/api_client.py` HTTP 客户端
    - 实现 ApiClient 类：`__init__`、`request`、`get`、`post`、`put`、`delete`、`set_token`、`get_last_response`
    - 自动拼接 base_url，记录请求/响应日志
    - 支持 Authorization header 管理
    - _需求: 2.1, 2.2_

  - [ ]* 4.2 编写 ApiClient 属性测试
    - **Property 2: HTTP 客户端方法路由与请求头正确性**
    - 使用 Hypothesis 从 [GET,POST,PUT,DELETE] 随机选择方法，生成随机 token，验证请求方法和 Authorization header 正确
    - **验证需求: 2.1, 2.2**

  - [x] 4.3 实现 `tests/utils/assertions.py` 响应断言工具
    - 实现 ResponseAssertions 类：`status_code`、`json_field`（支持点号路径）、`json_has_field`、`response_time_less_than`
    - 支持链式调用
    - 断言失败时附带期望值与实际值对比信息
    - _需求: 2.3_

  - [ ]* 4.4 编写 ResponseAssertions 属性测试
    - **Property 3: 响应断言工具的正确性**
    - 使用 Hypothesis 生成随机状态码（100-599）和随机 JSON 字典，验证匹配断言通过、不匹配断言抛出 AssertionError
    - **验证需求: 2.3**

  - [ ]* 4.5 编写 ApiClient 日志完整性属性测试
    - **Property 4: API 失败请求的日志完整性**
    - 使用 Hypothesis 生成随机 URL 路径、方法和错误状态码，验证日志包含完整请求 URL、方法、状态码和响应体
    - **验证需求: 2.6**

- [x] 5. 实现 Fixture 层与测试数据
  - [x] 5.1 实现 `tests/conftest.py` 全局 fixture
    - 实现 config fixture（session 级别）
    - 实现 flask_app fixture（session 级别，TESTING=True）
    - 实现 flask_client fixture（函数级别）
    - 实现 api_client fixture（session 级别）
    - _需求: 1.5, 2.4_

  - [x] 5.2 实现 `tests/fixtures/api_fixtures.py` API 测试 fixture
    - 提供已认证的 api_client fixture（自动登录获取 token）
    - _需求: 1.5, 2.2_

  - [x] 5.3 创建测试数据文件
    - 创建 `tests/testdata/login_data.yaml`：包含正常登录、错误密码、缺少字段等测试场景
    - 创建 `tests/testdata/login_data.csv`：CSV 格式的登录测试数据
    - _需求: 2.7_

- [x] 6. 检查点 - 引擎层与 Fixture 验证
  - 确保所有测试通过，如有问题请向用户确认。

- [x] 7. 实现 API 测试用例
  - [x] 7.1 实现 `tests/testcases/api/test_login.py` 登录接口测试
    - 使用 Flask test_client 测试 POST /api/login
    - 测试正确凭据登录：验证 code=200 且包含 token 字段
    - 测试错误密码：验证 code=401
    - 测试缺少参数：验证 code=400
    - 使用 @pytest.mark.api 标记
    - _需求: 2.4, 2.5_

  - [x] 7.2 实现数据驱动登录测试
    - 使用 `pytest.mark.parametrize` + `DataDriver.load` 从 YAML 文件加载测试数据
    - 验证数据驱动注入机制正常工作
    - _需求: 2.7, 2.8_

  - [ ]* 7.3 编写 API 测试用例的单元测试
    - 测试边界情况：空请求体、无效 JSON、超长字段
    - _需求: 2.5, 2.6_

- [x] 8. 实现 UI 测试引擎与用例
  - [x] 8.1 实现 `tests/pages/base_page.py` 页面基类
    - 实现 BasePage 类：`navigate`、`click`、`fill`、`get_text`、`wait_for`、`screenshot`
    - 基于 Playwright 封装
    - _需求: 3.2, 3.3_

  - [x] 8.2 实现 `tests/fixtures/ui_fixtures.py` UI 测试 fixture
    - 实现 browser_page fixture，支持 headless 模式配置
    - 测试结束后自动关闭浏览器
    - 测试失败时自动截图
    - _需求: 3.1, 3.4, 3.5, 3.6_

  - [x] 8.3 实现 `tests/testcases/ui/test_login_page.py` UI 测试用例模板
    - 提供登录页面 UI 测试的基本结构和示例
    - 使用 @pytest.mark.ui 标记
    - _需求: 3.2_

- [x] 9. 检查点 - 测试用例层验证
  - 确保所有测试通过，如有问题请向用户确认。

- [x] 10. 实现插件层
  - [x] 10.1 实现 `tests/testcases/performance/locustfile.py` 性能测试脚本
    - 编写 Locust 性能测试脚本模板，针对 POST /api/login 接口
    - 支持通过配置文件定义并发用户数和持续时间
    - 使用 @pytest.mark.perf 标记（pytest 入口）
    - _需求: 5.1, 5.2, 5.3, 5.4_

  - [x] 10.2 实现 `tests/testcases/security/test_security.py` 安全测试用例
    - 实现 SQL 注入检测测试模板
    - 实现 XSS 检测测试模板
    - 实现认证与授权测试模板
    - 使用 @pytest.mark.security 标记
    - _需求: 6.1, 6.2, 6.3, 6.4_

- [x] 11. 实现报告与 CI 集成
  - [x] 11.1 配置测试报告生成
    - 在 pytest.ini 中配置 Allure 和 HTML 报告输出路径
    - 配置 JUnit XML 输出
    - _需求: 4.1, 4.2, 4.3, 7.3_

  - [x] 11.2 创建 `.github/workflows/test.yml` CI 配置文件
    - 配置 GitHub Actions workflow：安装依赖、执行 API 测试、生成报告
    - 支持按 marker 分类执行测试
    - _需求: 7.1, 7.4_

- [x] 12. 最终检查点 - 全量验证
  - 确保所有测试通过，如有问题请向用户确认。

## 备注

- 标记 `*` 的任务为可选任务，可跳过以加速 MVP 交付
- 每个任务引用了具体的需求编号，确保需求可追溯
- 检查点任务用于阶段性验证，确保增量交付的正确性
- 属性测试验证设计文档中的 6 个正确性属性，使用 Hypothesis 库实现
- 单元测试验证具体示例和边界情况
