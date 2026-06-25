# Changelog

本文件记录 Nexus 的所有重要变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)，
本项目遵循[语义化版本](https://semver.org/spec/v2.0.0.html)。

---

## [1.0.0] — 2026-06-25

### Added

- **SKILL.md** — 核心 Skill 文件：角色定义（理疗师 Siqi）、六层 26 项能力金字塔、四种疗法智能匹配速查表、6 步工作流、伦理红线、输出规范、References/Examples 完整索引、工具说明
- **prompts/core/workflow.md** — 6 步完整工作流（情绪承接→评估→匹配→干预→交付→收束），每步含决策树与分支
- **prompts/core/guardrails.md** — 三条绝对伦理红线（自伤转介/隐私底线/能力边界）+ 六类语言禁忌 + 安全容器维持规则
- **prompts/core/output-spec.md** — 对话语气规范 + 脱敏处理规则 + 四种交付物格式模板 + 18 场景速查表
- **references/ 深度知识库（10 个文件）**：
  - 5 个疗法知识文件：总览对比 + Imago / EFT / Gottman / IBCT 核心理论与技术手册
  - 5 个场景融合文件：修复期沟通 / 冲突降级 / 信任重建 / 镜像信写作 / 自我重建
- **examples/ 18 个场景示例**：
  - 恋爱 10 个（分手复合、情绪崩溃、频繁吵架、断联、异地信任、发现出轨、辨识咨询、不被看见、前任新欢、安全感缺失）
  - 婚姻 8 个（冷战、产后恶化、婆媳/岳婿冲突、经济分歧、出轨重建、无性婚姻、离婚辨识、室友婚姻）
  - 5 个高频场景含完整 AI 模拟对话 + 可交付输出
  - 13 个场景含框架骨架，渐进补充
- **scripts/desensitize.py** — 零外部依赖脱敏工具：自动识别手机号/身份证号/日期/金额/QQ号/微信号/邮箱/车牌号 + 中文姓名/地名/机构名 + 交互式确认模式
- **README.md** — GitHub 着陆页：功能列表 + ASCII 架构图 + 四平台安装 + 快速使用 + 设计原则 + 已知限制
- **CONTRIBUTING.md** — 贡献指南：环境搭建 + 贡献类型 + 示例规范 + PR 流程
- **LICENSE** — MIT，署名 Siqi Liu
- **.gitignore** — Python/OS/IDE/临时文件排除
- **.github/CODEOWNERS** — 代码所有者配置

### Design Decisions

- **融合命名 Nexus**（拉丁语"联结"）：四疗法在关系断裂处的重连。简短好记，跨语言无歧义
- **理疗师命名 Siqi**：用户钦定——四份溯源报告的作者为它们代言
- **渐进式披露**：Level 1 (name+desc) → Level 2 (SKILL.md) → Level 2.5 (prompts/core/) → Level 3 (references/ + examples/)
- **疗法 + 场景混合 references 切分**：5 疗法文件提供知识纵深，5 场景文件提供融合操作指南
- **v1.0 示例渐进发布**：5 高频场景（分手复合/情绪崩溃/频繁吵架/发现出轨/婚姻冷战）含完整对话 + 交付物，其余骨架待补
- **零依赖脱敏工具**：纯标准库正则引擎，遵守"无必要不引入依赖"原则
- **先接住人再分析问题**：所有工作流 Step 1 为情绪承接，以 Imago 镜像开场

---

[1.0.0]: https://github.com/Aether-liusiqi/nexus/releases/tag/v1.0.0
