#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nexus Skill 关键词预检 Hook
UserPromptSubmit 触发：在模型处理前检测用户输入，
命中两性关系关键词则注入 additionalContext 以激活 /nexus skill。
"""

import json
import sys

# ============================================================
# 关键词表 — 按信号强度分组
# ============================================================

# 强信号：几乎一定是两性关系问题
STRONG_KEYWORDS = [
    # 关系状态断裂
    "分手", "被分手", "分开了",
    "复合", "和好",
    "挽回", "追回来",
    "失恋",
    "离婚", "想离婚", "离不离婚",
    "分居",
    "前任", "前男友", "前女友", "前夫", "前妻",
    "男朋友", "女朋友", "男友", "女友", "老公", "老婆",
    # 忠诚/背叛
    "出轨", "劈腿", "第三者", "小三", "暧昧对象",
    "背叛了我", "被他骗了", "被她骗了",
    # 婚姻
    "婚姻", "夫妻", "结婚",
    # 关系描述
    "感情破裂", "关系破裂",
    "两性关系", "伴侣关系",
    "修复关系",
    "退婚",
]

# 中信号：在多数语境下指向两性关系问题
MEDIUM_KEYWORDS = [
    # 情绪/痛苦
    "走不出来", "放不下", "忘不掉", "忘不了",
    "情绪崩溃", "很难受", "好难过",
    # 冲突
    "冷战", "冷暴力", "不联系",
    "吵架", "争吵", "争执",
    "总是吵架", "天天吵架", "频繁吵架",
    "吵得很凶", "争执不休",
    "四个月没说话",
    # 信任
    "没有安全感", "疑神疑鬼",
    "信任破裂", "不信任",
    # 关系问题
    "恋爱", "谈恋爱", "对象",
    "感情问题", "情感问题",
    "感情淡了", "没感觉了", "像室友",
    "没激情", "感情变淡",
    # 被抛弃/失去
    "被抛弃", "不辞而别", "突然冷淡",
    "有了新欢", "有新欢",
    "异地恋",
]

# 弱信号：需要复合判断（仅在与其他信号共现时才触发）
WEAK_KEYWORDS = [
    "他不理我", "她不理我",
    "他不回我", "她不回我",
    "想他", "想她",
    "忘了他", "忘了她",
    "回到过去",
]

# 排除关键词：包含这些词时不触发（非两性关系场景）
EXCLUSION_KEYWORDS = [
    "亲子", "孩子", "宝宝", "小孩",
    "职场", "同事", "老板", "工作",
    "朋友", "闺蜜", "兄弟",
    "父母", "爸爸", "妈妈", "父亲", "母亲",
    "代码", "编程", "bug", "程序",
    "股票", "基金", "交易",
]

# ============================================================
# 检测逻辑
# ============================================================


def detect_keywords(prompt: str) -> list[str]:
    """返回命中的关键词列表，未命中返回空列表。"""
    matched = []

    # 强信号：命中任一即触发
    for kw in STRONG_KEYWORDS:
        if kw in prompt:
            matched.append(kw)

    # 中信号：命中任一即触发
    for kw in MEDIUM_KEYWORDS:
        if kw in prompt:
            matched.append(kw)

    # 弱信号：仅在已有强/中信号命中时追加（不独立触发）
    if matched:
        for kw in WEAK_KEYWORDS:
            if kw in prompt and kw not in matched:
                matched.append(kw)

    # 排除检查：如果命中了排除关键词，且没有强信号，则不触发
    if not any(kw in STRONG_KEYWORDS for kw in matched):
        for ex in EXCLUSION_KEYWORDS:
            if ex in prompt:
                return []

    return matched


def main():
    try:
        raw = sys.stdin.read()
    except (OSError, EOFError):
        sys.exit(0)

    if not raw or not raw.strip():
        sys.exit(0)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        sys.exit(0)

    prompt = data.get("prompt", "")
    if not prompt:
        sys.exit(0)

    matched = detect_keywords(prompt)

    if not matched:
        sys.exit(0)

    # 命中 → 注入 additionalContext
    matched_str = "、".join(matched[:8])  # 最多显示 8 个
    output = {
        "additionalContext": (
            f"【自动激活 /nexus】用户在消息中提到了两性关系/情感关键词：{matched_str}。"
            "如果 nexus skill 尚未激活，请立即执行 Skill tool 加载 nexus"
            "（skill 名: nexus，位于用户级 skill 目录）。"
            "nexus 是一个两性情感修复 AI 理疗师 skill，"
            "融合 Imago、EFT、Gottman、IBCT 四大伴侣疗法，"
            "覆盖分手/复合/挽回/修复/沟通冲突/信任破裂/失恋/感情变淡/出轨/冷战等场景。"
            "激活后请以理疗师 Siqi 的身份进行回复，"
            "先做情绪承接（镜像+验证+安全容器），再做评估和干预。"
        ),
    }

    sys.stdout.write(json.dumps(output, ensure_ascii=False))
    sys.exit(0)


if __name__ == "__main__":
    main()
