---
inclusion: auto
---

# 架构规范约束规则

在进行代码生成、项目脚手架搭建、模块设计时，必须遵循以下架构规则：

## 规则数据源

参考 #[[file:skills/architecture-guide/patterns.yaml]] 中定义的架构规范。

## 核心规则（不可违反）

1. 后端项目必须采用三层架构：Controller → Service → Repository
2. Controller 层只负责接收请求、参数校验、调用 Service、返回响应，禁止编写任何业务逻辑
3. 所有业务逻辑必须在 Service 层实现
4. 所有数据库操作必须通过 Repository 层，禁止在 Controller 或 Service 中直接写 SQL 或 ORM 查询
5. 配置与代码必须分离，禁止在代码中硬编码配置值（数据库地址、端口、密钥等）
6. 敏感信息（密码、密钥、Token）必须通过环境变量注入，不得出现在配置文件或代码中
7. 使用全局异常处理器统一处理错误响应，不在每个 Controller 方法中单独 try-catch
8. Service 层抛出业务异常，不处理 HTTP 相关逻辑（如状态码、响应格式）

## 推荐规则

1. 优先使用依赖注入管理组件依赖，便于测试和替换
2. 通用横切逻辑（认证、日志、限流）放在中间件中，不散落在各 Controller
3. 工具函数必须是无状态的纯函数，不依赖业务层组件
4. 使用自定义异常类表达业务错误（如 UserNotFoundException）
5. API 设计遵循 RESTful 风格，URL 使用名词复数，HTTP 方法表达操作语义
6. 统一 API 响应格式：`{"code": 200, "message": "success", "data": {}}`
7. 项目目录按功能域组织（controllers/、services/、repositories/），而非按技术类型

## 设计模式

- 推荐使用：依赖注入、工厂模式、策略模式、装饰器模式、Repository 模式
- 避免使用：God Object（上帝类）、Service Locator、硬编码单例

## 场景匹配

- 新建后端项目 → 按 patterns.yaml 中 backend_template 生成目录结构
- 新建前端项目 → 按 patterns.yaml 中 frontend_template 生成目录结构
- 新增 API 接口 → 必须同时创建 Controller、Service、Repository 三层文件
- 重构代码 → 检查是否违反分层约束，将错位的逻辑迁移到正确的层
