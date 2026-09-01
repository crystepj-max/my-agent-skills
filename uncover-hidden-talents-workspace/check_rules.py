#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""对实测对话逐字稿做机械化规则核查（客观的、可用程序判定的那部分）。

用法：python3 check_rules.py <iteration 目录>
输出：每个评测项的 JSON 结果，供后续汇总成 grading.json。
"""
import json
import re
import sys
from pathlib import Path

CORE_SENTENCE = "天赋永远不会过期，我们只是要找到你的底层天赋"
TIME_EXPECTATIONS = ["30-45", "30 到 45", "30到45", "30～45", "30-45分钟", "半小时到", "四十分钟", "45 分钟"]
FLATTERY = ["你很优秀", "你很厉害", "你很有想法", "你真的很有", "你非常优秀", "你很棒",
            "真了不起", "你太厉害了", "你很有天赋吗", "你真的很棒", "你很有洞察力",
            "你很特别", "你很不容易", "为你感到高兴", "你已经很出色"]
JARGON = ["心流", "荣格", "盖洛普", "CliftonStrengths", "优势识别器", "潜意识", "原型理论", "MBTI"]


def split_turns(text: str):
    """把逐字稿按「咨询师 / 助手」与「用户」切成轮次。"""
    # 兼容多种写法：**咨询师：** / **咨询师（第 1 轮）：** / **用户（开场）：**
    pattern = r"\*\*(?:咨询师|助手|AI|用户)[^*]{0,20}?\*\*"
    parts = re.split(pattern, text)
    markers = re.findall(pattern, text)
    turns = []
    for marker, body in zip(markers, parts[1:]):
        role = "user" if "用户" in marker else "coach"
        turns.append((role, body.strip()))
    return turns


def check_file(path: Path, with_skill: bool):
    text = path.read_text(encoding="utf-8")
    turns = split_turns(text)
    coach_turns = [b for r, b in turns if r == "coach"]
    opening = coach_turns[0] if coach_turns else ""

    results = []

    def add(name, passed, evidence):
        results.append({"text": name, "passed": passed, "evidence": evidence})

    # A1 开场原样包含核心句
    add("开场原样说出核心承诺「天赋永远不会过期，我们只是要找到你的底层天赋」",
        CORE_SENTENCE in opening,
        "开场中找到该句" if CORE_SENTENCE in opening else f"开场未找到。开场开头 60 字：{opening[:60]}")

    # A2 开场交代了时间预期
    hit = next((t for t in TIME_EXPECTATIONS if t in opening), None)
    add("开场交代了时间预期（约 30-45 分钟）", hit is not None,
        f"命中「{hit}」" if hit else "开场未提及时间预期")

    # A3 无空泛赞美
    found = [w for w in FLATTERY if w in text]
    add("全程未出现空泛赞美（如「你很优秀」「你很有想法」）", not found,
        "未发现" if not found else f"命中：{'、'.join(found)}")

    # A4 未向用户抛理论名词
    found = [w for w in JARGON if w in text]
    add("未向用户抛理论名词（心流 / 荣格 / 盖洛普等）", not found,
        "未发现" if not found else f"命中：{'、'.join(found)}")

    # A5 边聊边存：是否创建了素材档案（仅 with_skill 组适用）
    if with_skill:
        archive = sorted(path.parent.rglob("访谈素材.md"))
        archived_turns = 0
        if archive:
            archived_turns = archive[0].read_text(encoding="utf-8").count("**问**")
        add("边聊边存：已创建素材档案并逐轮记录",
            bool(archive) and archived_turns >= 3,
            f"档案文件 {archive[0].relative_to(path.parent) if archive else '无'}，已记录 {archived_turns} 轮")

    # A6 单轮问号数量（作为「一次只问一题」的客观信号）
    counts = [b.count("？") + b.count("?") for b in coach_turns]
    add("每轮问号数 ≤ 3（「一次只问一题」的客观信号）",
        all(c <= 3 for c in counts),
        f"各轮问号数：{counts}")

    return results


def main():
    root = Path(sys.argv[1])
    out = {}
    for case in sorted(root.iterdir()):
        if not case.is_dir():
            continue
        for variant in ("with_skill", "without_skill"):
            t = case / variant / "outputs" / "transcript.md"
            if t.exists():
                out[f"{case.name}-{variant}"] = check_file(t, variant == "with_skill")
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
