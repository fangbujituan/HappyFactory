# Flask API 自动化测试项目

基于 Flask 的 REST API 项目，集成了以 pytest 为核心的自动化测试框架，支持 API 测试、UI 测试、性能测试和安全测试。

## 项目结构

```
├── app/                          # Flask 应用
│   ├── __init__.py               # App 工厂函数
│   └── routes/
│       └── auth.py               # 认证路由 (POST /api/login)
├── tests/                        # 测试框架
│   ├── conftest.py               # 全局 fixture
│   ├── pytest.ini                # pytest 配置
│   ├── config/                   # 多环境配置 (dev/staging/prod)
│   ├── fixtures/                 # 测试 fixture
│   ├── pages/                    # Page Object Model 页面对象
│   ├── utils/                    # 工具模块
│   │   ├── api_client.py         # HTTP 客户端封装
│   │   ├── assertions.py         # 响应断言工具
│   │   ├── config_manager.py     # 配置管理器
│   │   ├── data_driver.py        # 数据驱动加载器
│   │   └── logger.py             # 日志工具
│   ├── testcases/                # 测试用例
│   │   ├── api/                  # API 接口测试
│   │   ├── ui/                   # UI 自动化测试
│   │   ├── performance/          # 性能测试 (Locust)
│   │   └── security/             # 安全测试
│   └── testdata/                 # 测试数据 (YAML/CSV)
├── .github/workflows/test.yml    # GitHub Actions CI
├── requirements.txt
└── run.py                        # 应用入口
```

## 快速开始

### 安装依赖

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 启动应用

```bash
python run.py
```

应用运行在 http://localhost:5000

### 运行测试

```bash
# 全量测试
pytest -c tests/pytest.ini

# 按类型运行
pytest -m api -c tests/pytest.ini        # API 测试
pytest -m security -c tests/pytest.ini   # 安全测试
pytest -m ui -c tests/pytest.ini         # UI 测试
pytest -m perf -c tests/pytest.ini       # 性能测试
```

### 指定环境

```bash
pytest -c tests/pytest.ini --env staging
# 或
TEST_ENV=staging pytest -c tests/pytest.ini
```

## 测试报告

运行测试后自动生成：
- HTML 报告：`tests/reports/report.html`
- JUnit XML：`tests/reports/junit.xml`
- Allure（可选）：`pytest --alluredir=tests/reports/allure-results -c tests/pytest.ini`

## 数据驱动

测试数据存放在 `tests/testdata/`，支持 YAML、JSON、CSV 格式：

```python
from tests.utils.data_driver import DataDriver

@pytest.mark.parametrize("data", DataDriver.load("tests/testdata/login_data.yaml"))
def test_login(flask_client, data):
    resp = flask_client.post("/api/login", json=data["input"])
    assert resp.status_code == data["expected"]["status_code"]
```

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/login | 用户登录，返回 token |

## 技术栈

- Flask 3.0+ — Web 框架
- pytest — 测试框架
- Playwright — UI 自动化
- Locust — 性能测试
- Hypothesis — 属性测试
- Allure / pytest-html — 测试报告
