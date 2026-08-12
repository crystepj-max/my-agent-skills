#!/usr/bin/env python3
"""Add a '仓库链接 / 来源' column to skill-desc-translation.md, preserving the
Chinese descriptions exactly. Source is looked up from a classified mapping."""
import re, shutil, os

SRC_MD = "/Users/chris/WorkBuddy/2026-08-01-16-08-33/skill-desc-translation.md"
BAK = SRC_MD + ".bak"
shutil.copy(SRC_MD, BAK)

MATT = "https://github.com/mattpocock/skills"
BAOYU = "https://github.com/JimLiu/baoyu-skills"
BERK = "https://github.com/xbtlin/ai-berkshire"
BUNDLE = "WorkBuddy 内置/应用市场（见 install_all_skills.sh 原样打包）"

mattpocock = {"ask-matt","code-review","codebase-design","diagnosing-bugs","domain-modeling",
    "grill-me","grilling","handoff","implement","improve-codebase-architecture","prototype",
    "resolving-merge-conflicts","teach","to-spec","to-tickets","triage","tdd","wayfinder",
    "writing-great-skills","grill-with-docs","research","setup-matt-pocock-skills"}
baoyu = {"baoyu-comic","baoyu-image-gen","baoyu-infographic","baoyu-slide-deck"}
berkshire = {"bottleneck-hunter","deep-company-series","dyp-ask","earnings-review","earnings-team",
    "financial-data","income-investment","industry-funnel","industry-research","investment-checklist",
    "investment-memo-craft","investment-research","investment-team","management-deep-dive",
    "portfolio-review","private-company-research","quality-screen","thesis-drift","thesis-tracker",
    "wechat-article","news-pulse"}
explicit = {
    "agnes-ai-generation-skill": "https://github.com/Yacey/agnes-ai-generation-skill",
    "beautiful-html-templates": "https://github.com/zarazhangrui/beautiful-html-templates",
    "frontend-slides": "https://github.com/zarazhangrui/frontend-slides",
    "guizang-ppt-skill": "https://github.com/op7418/guizang-ppt-skill",
    "humanize-ppt": "https://github.com/LearnPrompt/humanize-ppt",
    "llm-wiki": "https://github.com/nashsu/llm_wiki_skill",
    "remotion-video-toolkit": "https://github.com/shreefentsar/remotion-video-toolkit",
    "ppt-master": "https://github.com/hugohe3/ppt-master",
}
# 5 heavy skills: large local binary assets -> install via repo, not bundled
HEAVY = {"beautiful-html-templates","guizang-ppt-skill","humanize-ppt","ppt-master","baoyu-slide-deck"}
builtin = {"edit-article","find-skills","frontend-design","git-guardrails-claude-code","hatch-pet",
    "migrate-to-shoehorn","neat-freak","obsidian-vault","remotion-best-practices",
    "remotion-video-production","scaffold-exercises","setup-pre-commit","skill-creator",
    "storage-analyzer","video-production"}

def source_for(name):
    if name in explicit:
        return explicit[name]
    elif name in mattpocock:
        return MATT
    elif name in baoyu:
        return BAOYU
    elif name in berkshire:
        return BERK
    else:
        return BUNDLE

def fmt(url):
    # render as markdown link if it's a URL, else keep text
    if url.startswith("http"):
        m = re.match(r"https?://(github\.com/[^/]+/[^/]+)", url)
        label = m.group(1) if m else url
        return f"[{label}]({url})"
    return url

row_re = re.compile(r'^\|\s*(\d+)\s*\|\s*`([^`]+)`\s*\|\s*(.+?)\s*\|\s*$')
out = []
added = 0
with open(SRC_MD) as f:
    for line in f:
        line = line.rstrip("\n")
        m = row_re.match(line)
        if m:
            num, name, desc = m.group(1), m.group(2), m.group(3)
            src = fmt(source_for(name))
            if name in HEAVY:
                src = src + "（体积大，建议用仓库链接安装，未打包进脚本）"
            out.append(f"| {num} | `{name}` | {desc} | {src} |")
            added += 1
        else:
            out.append(line)

# fix header row + separator to have 4 columns
out = [l.replace("| # | Skill 名称 | 中文描述 |", "| # | Skill 名称 | 中文描述 | 仓库链接 / 来源 |")
         .replace("|---|---|---|", "|---|---|---|---|") for l in out]

with open(SRC_MD, "w") as f:
    f.write("\n".join(out) + "\n")

print(f"rows updated: {added}")
print("mapping coverage check:")
allnames = mattpocock | baoyu | berkshire | set(explicit) | builtin
print("  mattpocock:", len(mattpocock), "baoyu:", len(baoyu), "berkshire:", len(berkshire),
      "explicit:", len(explicit), "builtin:", len(builtin), "total:", len(allnames))
