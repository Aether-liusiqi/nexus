#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nexus 脱敏处理工具 — 零外部依赖，纯标准库。

自动识别聊天记录/文本中的敏感信息，交互式确认后替换。
支持：中文姓名、地名、单位/学校名、精确日期、金额、手机号、身份证号。

用法:
    python desensitize.py input.txt                    # 交互模式
    python desensitize.py input.txt --output clean.txt # 输出到文件
    python desensitize.py input.txt --auto             # 自动替换（跳过确认）
    python desensitize.py input.txt --show-map         # 显示替换映射表
    echo "文本" | python desensitize.py                # 从 stdin 读取
"""

import re
import sys
import argparse
import json
from collections import OrderedDict


# ---- 检测规则 ----

RULES = {
    "手机号": {
        "pattern": re.compile(r'1[3-9]\d[-\s]?\d{4}[-\s]?\d{4}'),
        "replace": "[手机号]",
    },
    "身份证号": {
        "pattern": re.compile(r'[1-9]\d{5}(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx]'),
        "replace": "[身份证号]",
    },
    "精确日期": {
        "pattern": re.compile(
            r'(?:19|20)\d{2}[年/\-.](?:1[0-2]|0?[1-9])[月/\-.](?:[12]\d|3[01]|0?[1-9])[日号]?'
        ),
        "replace": lambda m: "XXXX年XX月XX日",
    },
    "金额_元": {
        "pattern": re.compile(r'(\d{2,}(?:\.\d{1,2})?)\s*元'),
        "replace": lambda m: f"约{_round_amount(m.group(1))}元",
    },
    "金额_万": {
        "pattern": re.compile(r'(\d+(?:\.\d+)?)\s*万'),
        "replace": lambda m: f"约{_round_amount(m.group(1))}万元",
    },
    "QQ号": {
        "pattern": re.compile(r'QQ[号:：]?\s*\d{5,12}'),
        "replace": "[QQ号]",
    },
    "微信号": {
        "pattern": re.compile(r'(?:微信|wx|WX|wechat)[号:：]?\s*[a-zA-Z][a-zA-Z0-9_\-]{5,19}'),
        "replace": "[微信号]",
    },
    "邮箱": {
        "pattern": re.compile(r'\b[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}\b'),
        "replace": "[邮箱]",
    },
    "车牌号": {
        "pattern": re.compile(r'[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤川青藏琼宁][A-Z][A-HJ-NP-Z0-9]{4,5}[A-HJ-NP-Z0-9挂学警港澳]'),
        "replace": "[车牌号]",
    },
}

# 地名后缀：省/市/区/县/镇/街道/村/路/街/巷等
PLACE_SUFFIXES = r'(?:省|市|区|县|镇|乡|街道|村|路|街|巷|弄|道|里|胡同|新区|开发区|工业园|高新区)'

# 单位后缀
ORG_SUFFIXES = r'(?:局|公司|医院|大学|学院|中学|小学|研究所|中心|银行|证券|保险|基金|集团|厂|院|站|所|队|处|科|室|委员会|办公室|总队|支队|大队|分局|支行|分行|总行|居委会|村委会|物业)'

# 中文姓名模式（两字或三字，不含复姓处理）
CHINESE_NAME_PATTERN = re.compile(
    r'(?<![a-zA-Z0-9一-鿿])'
    r'[一-鿿]{2,3}'
    r'(?=\s*(?:女士|先生|同志|老师|医生|教授|经理|局长|主任|市长|书记|总的|同学|师傅|阿姨|叔叔|伯伯|婶婶|舅舅|舅妈|姑姑|姑妈|姨|姨妈|哥哥|姐姐|弟弟|妹妹|爸爸|妈妈|爷爷|奶奶|外公|外婆|老公|老婆|男朋友|女朋友|前任|现任|闺蜜|兄弟)'
    r'|[：:，,。.！!？?\s]'
    r')'
)


def _round_amount(num_str: str) -> str:
    """将金额数字取整显示，同时保留量级感"""
    try:
        num = float(num_str.replace(',', ''))
    except ValueError:
        return num_str
    if num >= 10000:
        return f"{num/10000:.1f}万"
    elif num >= 1000:
        return f"{num/1000:.1f}千"
    elif num >= 100:
        return f"{int(num // 100) * 100}余"
    else:
        return str(int(num))


def find_pattern_matches(text: str) -> list[dict]:
    """查找所有可被 RULES 匹配的敏感项"""
    matches = []
    for rule_name, rule in RULES.items():
        for m in rule["pattern"].finditer(text):
            start, end = m.start(), m.end()
            original = m.group()
            if isinstance(rule["replace"], str):
                replacement = rule["replace"]
            else:
                replacement = rule["replace"](m)
            matches.append({
                "rule": rule_name,
                "start": start,
                "end": end,
                "original": original.strip(),
                "replacement": replacement,
            })
    matches.sort(key=lambda x: x["start"])
    return matches


def find_chinese_names(text: str) -> list[dict]:
    """查找可能的中文姓名"""
    matches = []
    for m in CHINESE_NAME_PATTERN.finditer(text):
        name = m.group().strip()
        # 过滤常见非姓名后缀词
        if name in SKIP_NAMES:
            continue
        start, end = m.start(), m.end()
        matches.append({
            "rule": "中文姓名",
            "start": start,
            "end": end,
            "original": name,
            "replacement": _name_replacement(name),
        })
    return matches


SKIP_NAMES = {
    "是的", "好的", "可以", "不过", "所以", "因为", "但是", "而且", "然后", "如果",
    "已经", "没有", "这个", "那个", "什么", "怎么", "为什么", "怎么样",
    "我觉得", "你知道", "就是说", "所以说", "其实", "真的", "可能", "应该",
    "谢谢", "对不起", "没关系", "不客气", "请问", "你好",
    "今天", "明天", "昨天", "现在", "以前", "以后",
    "一个", "两个", "三个", "一些", "一点",
    "不能", "不会", "不想", "不要", "不是",
    "有人", "有时候", "有时候", "怎么办", "是不是",
}


def _name_replacement(name: str) -> str:
    """根据姓名字数生成替换"""
    if len(name) == 2:
        return f"小{name[1]}" if name[1] not in SKIP_NAMES else "某人"
    elif len(name) == 3:
        return f"{name[0]}某"
    return "某人"


def find_place_names(text: str) -> list[dict]:
    """查找可能的地名"""
    pattern = re.compile(
        r'(?:[一-鿿]{2,6})' + PLACE_SUFFIXES
    )
    matches = []
    for m in pattern.finditer(text):
        original = m.group()
        # 过滤过短或明显不是地名的
        if len(original) < 4:
            continue
        # 提取地名核心部分用于替换
        prefix = original[:-len(re.search(PLACE_SUFFIXES, original).group())]
        if len(prefix) >= 2:
            replacement = f"{prefix[0]}某{original[-2:]}"
        else:
            replacement = f"某地{original[-2:]}"
        matches.append({
            "rule": "地名",
            "start": m.start(),
            "end": m.end(),
            "original": original,
            "replacement": replacement,
        })
    return matches


def find_org_names(text: str) -> list[dict]:
    """查找可能的单位/学校名"""
    pattern = re.compile(
        r'(?:[一-鿿]{2,12})' + ORG_SUFFIXES
    )
    matches = []
    seen = set()
    for m in pattern.finditer(text):
        original = m.group()
        if original in seen:
            continue
        seen.add(original)
        if len(original) < 5:
            continue
        replacement = f"某{original[-2:]}"
        matches.append({
            "rule": "单位/学校",
            "start": m.start(),
            "end": m.end(),
            "original": original,
            "replacement": replacement,
        })
    return matches


# ---- 核心逻辑 ----

def collect_all_matches(text: str) -> list[dict]:
    """收集所有类型的敏感信息匹配"""
    matches = []
    matches.extend(find_pattern_matches(text))
    matches.extend(find_chinese_names(text))
    matches.extend(find_place_names(text))
    matches.extend(find_org_names(text))

    # 按位置排序，移除重叠项（保留更长的匹配）
    matches.sort(key=lambda x: (x["start"], -(x["end"] - x["start"])))
    filtered = []
    last_end = 0
    for m in matches:
        if m["start"] >= last_end:
            filtered.append(m)
            last_end = m["end"]
    return sorted(filtered, key=lambda x: x["start"])


def interactive_confirm(matches: list[dict]) -> list[dict]:
    """交互式确认每项替换"""
    if not matches:
        print("未检测到敏感信息。")
        return []

    print(f"\n检测到 {len(matches)} 项可能的敏感信息：\n")
    for i, m in enumerate(matches, 1):
        print(f"  [{i}] {m['rule']}: \"{m['original']}\" -> \"{m['replacement']}\"")

    print("\n选项：")
    print("  y   — 全部替换（推荐）")
    print("  n   — 全部跳过")
    print("  s   — 逐项确认")
    print("  q   — 退出")

    choice = input("\n请选择 [y/n/s/q]: ").strip().lower()

    if choice == 'q':
        print("已取消。")
        sys.exit(0)
    elif choice == 'y':
        return matches
    elif choice == 'n':
        return []
    elif choice == 's':
        confirmed = []
        for i, m in enumerate(matches, 1):
            resp = input(f"  [{i}/{len(matches)}] {m['rule']}: \"{m['original']}\" -> \"{m['replacement']}\" [y/n/q]: ").strip().lower()
            if resp == 'q':
                print("已取消剩余项。")
                break
            elif resp == 'y' or resp == '':
                confirmed.append(m)
            else:
                print(f"    已跳过。")
        return confirmed
    else:
        print("无效输入，默认全部替换。")
        return matches


def apply_matches(text: str, matches: list[dict]) -> tuple[str, dict[str, str]]:
    """执行替换，返回脱敏后文本和映射表"""
    mapping = OrderedDict()
    result_chars = list(text)
    # 从后往前替换，避免索引偏移
    for m in reversed(matches):
        start, end = m["start"], m["end"]
        original = m["original"]
        replacement = m["replacement"]
        result_chars[start:end] = replacement
        mapping[original] = replacement
    return ''.join(result_chars), dict(mapping)


def main():
    parser = argparse.ArgumentParser(
        description="Nexus 脱敏处理工具 — 自动识别并替换聊天记录中的敏感信息",
    )
    parser.add_argument("input", nargs="?", default=None,
                        help="输入文件路径（不指定则从 stdin 读取）")
    parser.add_argument("--output", "-o", default=None,
                        help="输出文件路径（不指定则输出到 stdout）")
    parser.add_argument("--auto", "-a", action="store_true",
                        help="自动替换所有检测到的敏感项，跳过确认")
    parser.add_argument("--show-map", "-s", action="store_true",
                        help="在输出末尾显示替换映射表")
    args = parser.parse_args()

    # 读取输入
    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        if sys.stdin.isatty():
            print("请输入要脱敏的文本（输入完成后按 Ctrl+Z 然后回车 结束）：", file=sys.stderr)
        text = sys.stdin.read()

    if not text.strip():
        print("错误：输入为空。", file=sys.stderr)
        sys.exit(1)

    # 收集匹配
    matches = collect_all_matches(text)

    # 确认或自动
    if args.auto:
        confirmed = matches
    else:
        confirmed = interactive_confirm(matches)

    # 应用替换
    result, mapping = apply_matches(text, confirmed)

    # 输出
    output_lines = [result]
    if args.show_map and mapping:
        output_lines.append("\n--- 替换映射表 ---")
        for orig, repl in mapping.items():
            output_lines.append(f"  {orig} -> {repl}")

    output_text = '\n'.join(output_lines)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_text)
        print(f"\n脱敏完成。已写入 {args.output}（共 {len(confirmed)} 项替换）")
    else:
        # 确保 Windows 下 UTF-8 输出
        if sys.platform == "win32":
            sys.stdout.reconfigure(encoding='utf-8')
        print(output_text)


if __name__ == "__main__":
    main()
