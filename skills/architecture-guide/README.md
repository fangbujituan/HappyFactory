# 架构指南 Skill

## 目的

在自动编码过程中，确保 AI 生成的代码遵循团队的架构规范和设计原则。避免产出违反分层约束、配置硬编码、职责混乱的代码。

## 使用方式

本 skill 作为 steering 规则自动生效，当 Kiro 在以下场景中工作时会参考此架构指南：

- 新建项目脚手架
- 设计模块架构（spec 的 design 阶段）
- 生成代码（spec 的 task 执行阶段）
- 代码重构建议

## 核心约束

1. 后端项目必须采用三层架构：Controller → Service → Repository
2. Controller 层禁止编写业务逻辑
3. 配置与代码必须分离，敏感信息通过环境变量注入
4. 所有数据库操作必须通过 Repository 层

## 维护

编辑 `patterns.yaml` 来调整架构规则。修改 `level` 字段控制规则的强制程度：
- `required`：必须遵循
- `preferred`：推荐遵循
- `optional`：可选
