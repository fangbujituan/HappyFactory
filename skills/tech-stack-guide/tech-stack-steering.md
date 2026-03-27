---
inclusion: auto
---

# 技术选型约束规则

在进行代码生成、项目脚手架搭建、依赖推荐时，必须遵循以下规则：

## 选型数据源

参考 #[[file:skills/tech-stack-guide/frameworks.yaml]] 中定义的框架清单。

## 核心规则

1. 只推荐 `status: preferred` 或 `status: accepted` 的框架，绝不推荐 `status: excluded` 的框架
2. 优先推荐 `status: preferred` 的框架，仅在 preferred 不适用时才推荐 accepted
3. 如果用户未指定具体框架，默认使用 preferred 级别的框架
4. 推荐框架时简要说明选择理由和适用场景
5. 如果用户明确要求使用清单外的框架，提醒该框架不在团队选型范围内，但尊重用户最终决定

## 版本约束

- 使用 frameworks.yaml 中标注的版本范围
- 不推荐已 EOL 或即将 EOL 的版本

## 场景匹配

根据项目类型自动匹配合适的技术栈分类：
- Web 前端项目 → 查看 `web_frontend` + `css_ui` + `build_tools`
- Web 后端项目 → 查看 `web_backend` + `database`
- 桌面应用 → 查看 `desktop`
- 移动应用 → 查看 `mobile`
- 全栈项目 → 综合查看前后端 + 数据库 + 部署工具
