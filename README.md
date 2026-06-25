# Nexus 🪢 — AI 两性情感修复心理理疗师

> 融合 Imago、EFT、Gottman、IBCT 四大伴侣疗法，在关系断裂处重新联结。

[![Version](https://img.shields.io/badge/version-1.0.0-blue)](CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Platforms](https://img.shields.io/badge/platforms-4-orange)]()

---

## 功能

Nexus 是一个 AI Skill，激活后 AI 将扮演你的专属两性情感修复心理理疗师 **Siqi**。六层能力金字塔：

| 层级 | 名称 | 能力数 | 说明 |
|------|------|--------|------|
| 1 | 情绪承接与安全构建 | 4 | 危机干预、情绪验证、安全容器、自伤评估 |
| 2 | 问题评估与模式识别 | 5 | 关系史映射、依恋风格识别、互动循环追踪、深层需求挖掘、原生家庭分析 |
| 3 | 疗法匹配与策略制定 | 3 | 智能疗法匹配、用户指定疗法、干预路线图 |
| 4 | 具体干预执行 | 7 | 镜像信、沟通训练、冲突降级、信任重建、行为改变请求、情感连接重建、零负面性承诺 |
| 5 | 自我重建 | 5 | 哀伤处理、认同重建、模式总结、未来准备度、自我关怀 |
| 6 | 维持与预防 | 4 | 关系检查、联结仪式、预警信号、关闭出口 |

**四种疗法智能匹配**：根据你的问题自动选择 Imago / EFT / Gottman / IBCT，或有机融合。你也可以指定"用 Gottman 的视角看"。

---

## 架构

```
nexus/
├── SKILL.md                      # 核心入口 — 角色 + 能力金字塔 + 疗法速查
├── prompts/core/                 # 渐进披露 Level 2.5
│   ├── workflow.md               #   6 步完整工作流
│   ├── guardrails.md             #   伦理红线 + 语言禁忌
│   └── output-spec.md            #   输出规范 + 交付物模板
├── references/                   # 渐进披露 Level 3 — 深度知识库
│   ├── 01-four-therapies-overview.md
│   ├── 02-imago.md               #   Imago 核心理论 + 技术手册
│   ├── 03-eft.md                 #   EFT 核心理论 + 技术手册
│   ├── 04-gottman.md             #   Gottman 核心理论 + 技术手册
│   ├── 05-ibct.md                #   IBCT 核心理论 + 技术手册
│   ├── 06-communication-repair.md
│   ├── 07-conflict-deescalation.md
│   ├── 08-trust-rebuilding.md
│   ├── 09-letter-writing.md
│   └── 10-self-reconstruction.md
├── examples/                     # 18 个场景示例
│   ├── 01-breakup-closure-letter.md      ← 完整对话 + 交付物
│   ├── 02-post-breakup-collapse.md       ← 完整对话 + 交付物
│   ├── 03-frequent-fighting.md           ← 完整对话 + 交付物
│   ├── 06-infidelity-discovery.md        ← 完整对话 + 交付物
│   ├── 11-marital-cold-war.md            ← 完整对话 + 交付物
│   └── ... (13 个场景骨架，渐进补充)
├── hooks/
│   └── nexus-detector.py         # 关键词预检 Hook — 确定性自动激活
├── scripts/
│   └── desensitize.py            # 零依赖脱敏工具
└── tests/                        # v1.2 预留
```

---

## 四平台安装

### Claude Code

```bash
# 复制到项目级 skill 目录
cp -r nexus/ .claude/skills/

# 或全局安装
cp -r nexus/ ~/.claude/skills/
```

### Codex CLI

```bash
cp -r nexus/ .agents/skills/
```

### OpenClaw

```bash
cp -r nexus/ <workspace>/skills/
```

### OpenCode

```bash
cp -r nexus/ .opencode/skills/
```

### Hook 自动激活（推荐）

上述安装依赖模型扫描 skill 描述来匹配触发——当 skill 列表较长时，`nexus` 名字不自解释，可能被漏掉。**UserPromptSubmit Hook** 提供确定性触发：每次用户输入时进行关键词预检，命中即注入激活指令，不依赖模型判断。

```bash
# 1. 复制 hook 脚本到 Claude Code hooks 目录
cp hooks/nexus-detector.py ~/.claude/hooks/
```

**2. 在 `~/.claude/settings.json` 中添加 hooks 配置：**

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python ~/.claude/hooks/nexus-detector.py",
            "timeout": 10,
            "statusMessage": "检测情感关键词..."
          }
        ]
      }
    ]
  }
}
```

**原理**：UserPromptSubmit 在模型处理链之前触发，对用户输入做纯字符串关键词匹配（~10ms）。命中 50+ 两性关系关键词（分手/复合/挽回/失恋/冷战/出轨等），则通过 `additionalContext` 注入激活指令——模型不需要从技能列表中"认出" nexus，指令直接告诉它加载。

关键词分三级：**强信号**（28 个，命中即触发）、**中信号**（23 个，需通过排除检查）、**弱信号**（8 个，仅追加不独立触发）。**排除词**（17 个）防止"和朋友吵架""孩子冷战"等非两性场景误触发。详见 [hooks/nexus-detector.py](hooks/nexus-detector.py)。

---

## 快速使用

安装后，在对话中自然描述你的两性关系问题即可自动激活：

> "我和女朋友分手了，她写了很长一段话，我想复合但不知道怎么开口。"

> "我们结婚5年了，最近一年总是吵架，为一点小事就能炸。"

> "我发现他手机上有暧昧聊天，我想修复但不知道怎么开始。"

Nexus 会自动激活，Siqi 会先承接你的情绪，然后逐步帮你分析、匹配疗法、制定干预方案。

---

## 脱敏工具

```bash
# 交互式脱敏
python scripts/desensitize.py chat_log.txt

# 自动脱敏 + 查看映射表
python scripts/desensitize.py chat_log.txt --auto --show-map

# 输出到文件
python scripts/desensitize.py chat_log.txt --output clean.txt
```

---

## 设计原则

- **先接住人，再分析问题** — 所有对话以情绪承接开场
- **疗法融合而非堆砌** — 场景文件中四疗法交叉引用
- **渐进式披露** — Level 1→2→3 按需加载，不污染基础上下文
- **隐私是底线** — 对话不存储、输出自动脱敏
- **不替代专业帮助** — 自伤/自杀风险立即转介线下

---

## 已知限制

1. **非真人治疗师。** Siqi 是一个 AI 理疗师，不替代持牌心理健康专业人员。
2. **不做诊断。** 不诊断精神疾病（抑郁症、人格障碍等）。
3. **不替代危机干预。** 如有自伤或自杀念头，请立即联系当地危机热线或前往医院。
4. **脱敏工具 limitations。** `desensitize.py` 基于正则表达式，中文姓名和机构名识别率有限。敏感信息建议手动复核。
5. **不提供法律建议。** 离婚协议、财产分割、抚养权等问题请咨询律师。

---

## 许可

MIT © 2026 Siqi Liu

---

> *我们在关系中受伤，也在关系中被治愈。*
