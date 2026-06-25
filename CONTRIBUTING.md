# 贡献指南

感谢你对 Nexus 的兴趣！Nexus 是一个开放的两性情感修复 AI Skill，融合了 Imago、EFT、Gottman 和 IBCT 四种伴侣疗法。

## 环境搭建

Nexus 是一个纯 Markdown + Python 项目，不需要复杂的开发环境。

```bash
git clone git@github.com:Aether-liusiqi/nexus.git
cd nexus
# Python 3.6+ 即可运行脱敏工具，无额外依赖
python scripts/desensitize.py --help
```

## 可贡献的类型

| 类型 | 说明 | 难度 |
|------|------|------|
| **场景示例完善** | 将 13 个骨架示例补充为完整的模拟对话 + 交付物 | 中等 |
| **新增场景** | 提供新的两性关系问题场景 | 中等 |
| **疗法知识更新** | 基于新研究/新文献更新 references/ 中的疗法知识 | 较高 |
| **工具改进** | 改进 desensitize.py 的识别准确率或增加新功能 | 较高 |
| **文档完善** | 修正错别字、改进表达、补充说明 | 入门 |
| **四平台兼容性测试** | 在不同平台上测试 Skill 加载和触发 | 入门 |

## 示例贡献规范

### 场景示例格式

每个示例文件（`examples/XX-name.md`）包含两部分：

1. **A 部分：模拟对话** — AI 理疗师 Siqi 从情绪承接→评估→疗法匹配→干预→交付的完整会话流
2. **B 部分：可交付输出** — 该场景下具体的产物（信函/协议/路线图/计划/报告等）

### 模拟对话的写作标准

- 对话自然，不是脚本式问答
- Siqi 的语气：温暖但不煽情、专业但不冷漠、直接但不强硬
- 始终以"情绪承接"开场——不做建议前先做镜像
- 用户方真实——不说"好的我懂了谢谢"——有迟疑、有反问、有情绪
- 交付物是对话的自然产物，不是突然出现的

### 知识库贡献规范

- 每个文件聚焦一个主题
- 篇幅控制在 1000-2500 字
- 可独立阅读，不依赖其他 references 文件
- 如有引用，注明来源

## PR 流程

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feat/your-feature`
3. 提交更改：`git commit -m "feat: 描述你的更改"`
4. 推送到你的 Fork：`git push origin feat/your-feature`
5. 创建 Pull Request

PR 标题遵循 [Conventional Commits](https://www.conventionalcommits.org/)：
- `feat:` 新场景/新功能
- `fix:` 错误修复
- `docs:` 文档更改
- `refactor:` 代码重构

---

> **提示**：如果你是第一次贡献开源项目——从"文档完善"或"示例补充"开始是最容易的入口。我们欢迎任何水平的贡献。
