#!/usr/bin/env python3
"""
agent-skill-bridge: 把公共池 ~/.agents/skills/ 桥接进各 agent 默认 skill 目录（软链接），
并对每个 agent 做「同名 skill 去重」，确保每个 agent 对同一 skill 只保留 1 份（指向公共池的真源）。

扩展能力：
  - 中文化（--mode cn）：把自有 skill 的英文 / 空 description 译为中文，提升 "/" 命令可读性。

规则（用户确认版）：
  1) 插件型 skill 不碰     2) agent 默认路径/独有 skill 不碰
  3) 公共池靠软链桥接       4) 同名冲突 -> 删 agent 副本、改用公共池（先备份）

默认范围：claude / codex / workbuddy（可通过 --agents 覆盖）。

模式：
  --mode dry      # 只读规划桥接，不改动任何东西
  --mode apply    # 执行桥接（冲突副本先备份到 BACKUP_ROOT）
  --mode verify    # 校验各 agent 是否已覆盖公共池、无断链
  --mode dedup     # 校验/修复同名 skill 去重（默认只读；加 --fix 才实际删除重复项）
  --mode cn        # 中文化：检测自有 skill 的英文/空 description，自动归一化中英夹杂项，
                   #          报告仍需 LLM 翻译的纯英文项（默认只读；加 --fix 才写入归一化结果）
  --mode sync      # 同步回 GitHub：复制自有 skill(agent-skill-bridge)进仓库 + 刷新清单最新更新列
                   #          + 运行 sync.sh 提交推送 main。也可由 apply / cn --fix / dedup --fix 自动触发
  --no-sync        # 上述写操作后不自动推送 GitHub（默认自动同步）
用法：
  python3 bridge.py --mode dry
  python3 bridge.py --mode apply
  python3 bridge.py --mode verify
  python3 bridge.py --mode dedup            # 仅报告每个 agent 的重复 skill
  python3 bridge.py --mode dedup --fix      # 实际移除可安全删除的重复项（命令 .md / 非池软链），插件内重复仅报告
  python3 bridge.py --mode cn               # 仅报告英文/空 description（不改文件）
  python3 bridge.py --mode cn --fix         # 自动归一化中英夹杂项并写入；列出仍需 LLM 翻译的纯英文项
  python3 bridge.py --mode apply --agents claude,codex,workbuddy
"""
import os, shutil, argparse, re, json, time, sys, subprocess

HOME = os.path.expanduser("~")
USER_SRC = os.path.join(HOME, ".agents", "skills")
BACKUP_ROOT = os.path.join(HOME, ".agents", "skill-bridge-backups")
DATE_STR = time.strftime("%Y-%m-%d")

# 默认 agent -> 默认 skill 目录。新增 agent 在此加一行即可。
DEFAULT_AGENTS = {
    "claude":    os.path.join(HOME, ".claude", "skills"),
    "codex":     os.path.join(HOME, ".codex", "skills"),
    "workbuddy": os.path.join(HOME, ".workbuddy", "skills"),
}
# 可选（当前无可用可执行文件/暂未启用，需要时取消注释）：
# "kimicode": os.path.join(HOME, ".kimi-code", "skills"),

# 自有 skill 集中管理仓库（用于同步回 GitHub）
MY_REPO = os.path.join(HOME, "my-agent-skills")
OWN_BRIDGE = "agent-skill-bridge"


# ---------------------------------------------------------------------------
# 通用工具
# ---------------------------------------------------------------------------
def realpath(p):
    return os.path.realpath(p)


def list_skills(root):
    """返回 root 下带 SKILL.md 的目录名 -> realpath 映射。"""
    if not os.path.isdir(root):
        return {}
    out = {}
    for n in os.listdir(root):
        p = os.path.join(root, n)
        if os.path.isdir(p) and os.path.isfile(os.path.join(p, "SKILL.md")):
            out[n] = realpath(p)
    return out


def backup_and_remove(agent, name, path, sub="bridge"):
    """先备份（软链保留指向，实体目录 copytree），再删除原路径。返回是否执行了删除。"""
    dest = os.path.join(BACKUP_ROOT, sub, agent, name)
    if not os.path.exists(dest):
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        if os.path.islink(path):
            link = os.readlink(path)
            os.symlink(link, dest)
            with open(dest + ".linktarget.txt", "w") as f:
                f.write(link)
        else:
            shutil.copytree(path, dest)
        print(f"    [备份] {path} -> {dest}")
    else:
        print(f"    [备份已存在,跳过] {dest}")
    if os.path.islink(path):
        os.remove(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)
    else:
        os.remove(path)
    return True


# ---------------------------------------------------------------------------
# 桥接（dry / apply / verify）
# ---------------------------------------------------------------------------
def plan(user_skills, agents):
    print("公共用户池:", USER_SRC, "存在" if os.path.isdir(USER_SRC) else "【不存在】")
    print("=" * 72)
    for ag, tgt in agents.items():
        existing = list_skills(tgt)
        print(f"\n### {ag}  ->  {tgt}")
        if not os.path.isdir(tgt):
            print("    [需先] mkdir -p 目标目录 (当前不存在)")
            continue
        adds, replaces, keep = [], [], []
        for name, src_real in user_skills.items():
            tpath = os.path.join(tgt, name)
            if name not in existing:
                adds.append(name)
            elif existing[name] == src_real:
                keep.append(name)            # 已是公共池软链，跳过
            else:
                replaces.append((name, existing[name], src_real))  # 规则4
        print(f"    [ADD 软链]   {len(adds)}: {', '.join(sorted(adds)) if adds else '(无)'}")
        print(f"    [REPLACE 删副本] {len(replaces)}:")
        for n, ex, sr in sorted(replaces):
            print(f"        {n}: 删除 {ex} -> 链接 {sr}")
        if keep:
            print(f"    [已正确,跳过] {len(keep)}: {', '.join(sorted(keep))}")
    print("\n" + "=" * 72)
    print("规则2 校验 - 各 agent 独有(公共池无同名)的 skill 将保持不动:")
    for ag, tgt in agents.items():
        existing = list_skills(tgt)
        only = [n for n in existing if n not in user_skills]
        if only:
            print(f"  {ag}: {', '.join(sorted(only))}")
    print("\n(以上为只读规划。apply 模式将先备份冲突副本到", BACKUP_ROOT, "再替换)")


def apply(user_skills, agents):
    if not os.path.isdir(USER_SRC):
        print("公共池不存在:", USER_SRC)
        return
    print("备份根目录:", BACKUP_ROOT)
    print("=" * 72)
    for ag, tgt in agents.items():
        if not os.path.isdir(tgt):
            print(f"### {ag}: 目标不存在,跳过 ({tgt})")
            continue
        os.makedirs(tgt, exist_ok=True)
        existing = list_skills(tgt)
        added = repl = kept = 0
        print(f"### {ag}  ->  {tgt}")
        for name, src_real in sorted(user_skills.items()):
            tpath = os.path.join(tgt, name)
            if name not in existing:
                os.symlink(src_real, tpath)
                print(f"    [ADD] {name} -> {src_real}")
                added += 1
            elif existing[name] == src_real:
                kept += 1
            else:
                print(f"    [REPLACE] {name}: 删 agent 副本,改指公共池")
                backup_and_remove(ag, name, tpath)
                os.symlink(src_real, tpath)
                print(f"             -> {src_real}")
                repl += 1
        print(f"    => ADD {added} | REPLACE {repl} | 已正确跳过 {kept}")
    print("=" * 72)


def verify(user_skills, agents):
    print("验证各 agent 对公共池的覆盖:")
    print("=" * 72)
    allok = True
    for ag, tgt in agents.items():
        reached, broken = set(), 0
        if not os.path.isdir(tgt):
            print(f"  {ag}: 目标不存在 -> CHECK")
            allok = False
            continue
        for n in os.listdir(tgt):
            p = os.path.join(tgt, n)
            if os.path.islink(p):
                rp = realpath(p)
                if rp.startswith(USER_SRC + os.sep) or rp == USER_SRC:
                    reached.add(n)
                    if not os.path.exists(p):
                        broken += 1
        miss = user_skills.keys() - reached
        ok = (not miss) and (broken == 0)
        allok = allok and ok
        print(f"  {ag:10} 桥接 {len(reached):<3} 缺失 {len(miss):<3} 断链 {broken:<3} {'OK' if ok else 'CHECK'}")
        if miss:
            print("     缺失:", ", ".join(sorted(miss)))
    print("=" * 72)
    print("总状态:", "ALL OK" if allok else "CHECK NEEDED")


# ---------------------------------------------------------------------------
# 去重（dedup）：确保每个 agent 对同一 skill 只保留 1 份（指向公共池的真源）
# ---------------------------------------------------------------------------
def discover_entries(agent, skills_dir):
    """枚举一个 agent 所有会被识别为 skill 的条目。

    覆盖三种发现路径：
      - skills 目录（~/.agent/skills，含软链）
      - ~/.claude/commands/*.md（仅 claude；命令与 skill 同命名空间）
      - ~/.claude/plugins/**/SKILL.md（仅 claude；插件体系）
    codex / workbuddy 当前无 commands/plugins 重复风险，只扫 skills 目录。
    """
    entries = []
    # 1) skills 目录
    if os.path.isdir(skills_dir):
        for n in os.listdir(skills_dir):
            p = os.path.join(skills_dir, n)
            if os.path.isdir(p):
                rp = realpath(p)
                entries.append({
                    "name": n, "path": p, "kind": "skills",
                    "is_pool": rp.startswith(USER_SRC + os.sep) or rp == USER_SRC,
                    "real": rp,
                })
    # 2) commands（仅 claude）
    if agent == "claude":
        cmd = os.path.join(HOME, ".claude", "commands")
        if os.path.isdir(cmd):
            for fn in os.listdir(cmd):
                if fn.endswith(".md"):
                    entries.append({
                        "name": fn[:-3], "path": os.path.join(cmd, fn),
                        "kind": "command", "is_pool": False, "real": None,
                    })
    # 3) plugins（仅 claude）
    if agent == "claude":
        plug = os.path.join(HOME, ".claude", "plugins")
        if os.path.isdir(plug):
            for dp, dirs, files in os.walk(plug):
                if "SKILL.md" in files:
                    entries.append({
                        "name": os.path.basename(dp),
                        "path": os.path.join(dp, "SKILL.md"),
                        "kind": "plugin", "is_pool": False,
                        "real": realpath(dp),
                    })
    return entries


def dedup(user_skills, agents, fix):
    print("去重校验 - 每个 agent 对同一 skill 应只保留 1 份(指向公共池):")
    print("=" * 72)
    total_removed = 0
    for ag, skills_dir in agents.items():
        entries = discover_entries(ag, skills_dir)
        groups = {}
        for e in entries:
            groups.setdefault(e["name"], []).append(e)
        print(f"\n### {ag}  (发现 {len(entries)} 个 skill 条目, {len(groups)} 个不重名)")
        removed_here = 0
        for name in sorted(groups):
            es = groups[name]
            canonical = [e for e in es if e["kind"] == "skills" and e["is_pool"]]
            if not canonical:
                # 无公共池真源：可能是插件内部重复 / agent 独有。不自动删，仅报告。
                if len(es) > 1:
                    kinds = ", ".join(f"{e['kind']}:{os.path.basename(e['path'])}" for e in es)
                    print(f"  [仅报告] {name}: {len(es)} 份且无公共池真源 ({kinds})")
                    print(f"            -> 若是插件内部重复，请卸载对应插件；若是 agent 独有 skill，按规则2保留")
                continue
            extras = [e for e in es if not (e["kind"] == "skills" and e["is_pool"])]
            if not extras:
                continue
            print(f"  [重复] {name}: 真源= {canonical[0]['path']}")
            for e in extras:
                tag = {"command": "命令.md", "skills": "非池软链/目录", "plugin": "插件副本"}[e["kind"]]
                print(f"       - {tag:12} {e['path']}")
                if not fix:
                    continue
                if e["kind"] == "command":
                    backup_and_remove(ag, name, e["path"], sub="dedup-commands")
                    removed_here += 1
                elif e["kind"] == "skills":
                    # skills 目录内、同名但没指向公共池的软链/目录 -> 删，改为真源
                    backup_and_remove(ag, name, e["path"], sub="dedup-skills")
                    os.symlink(canonical[0]["real"], e["path"])
                    print(f"             -> 重建为 {canonical[0]['real']}")
                    removed_here += 1
                else:
                    print(f"       (插件副本 {e['path']} 不自动删，请卸载对应插件)")
        if fix:
            print(f"    => 本 agent 移除/修复 {removed_here} 个重复项")
            total_removed += removed_here
    print("=" * 72)
    if fix:
        print(f"去重完成: 共处理 {total_removed} 个可安全删除的重复项 (已备份到 {BACKUP_ROOT})")
    else:
        print("以上为只读报告。加 --fix 可实际移除『命令.md / 非池软链』类重复项(先备份)；插件内重复仍需手动卸载插件。")


# ---------------------------------------------------------------------------
# 中文化（cn）：把自有 skill 的英文/空 description 译为中文
# ---------------------------------------------------------------------------
BLOCK_INDICATORS = ("", ">-", "|-", ">", "|")


def owned_skill_files():
    """返回 [(name, path, scope)]，覆盖用户真正拥有的 skill：
       - 公共池全集
       - WorkBuddy 原生、非软链（指向池）的 skill
       不扫其它 agent 原生目录（属规则2 的 agent 独有，且会被桥接覆盖）。
    """
    out = []
    if os.path.isdir(USER_SRC):
        for n in sorted(os.listdir(USER_SRC)):
            d = os.path.join(USER_SRC, n)
            sm = os.path.join(d, "SKILL.md")
            if os.path.isdir(d) and os.path.isfile(sm):
                out.append((n, sm, "pool"))
    wb = DEFAULT_AGENTS.get("workbuddy")
    if wb and os.path.isdir(wb):
        for n in sorted(os.listdir(wb)):
            full = os.path.join(wb, n)
            if os.path.islink(full):
                continue
            if os.path.isdir(full):
                sm = os.path.join(full, "SKILL.md")
                if os.path.isfile(sm):
                    out.append((n, sm, "workbuddy-native"))
    return out


def parse_description(txt):
    """返回 (text, is_block, fm_match)。

    text: 有效的描述文本（块标量时拼接缩进行；无字段/空时返回 ""）
    is_block: 该描述是否为 YAML 块标量（>- / | 等，写入时需走 Edit 而非单行替换）
    fm_match: 正则匹配对象，用于单行重写
    """
    m = re.match(r"^(---\s*\n)(.*?)(\n---)", txt, re.S)
    if not m:
        return None, False, None
    fm = m.group(2)
    mm = re.search(r"^description:\s*(.*)$", fm, re.M)
    if not mm:
        return None, False, m   # 没有 description 字段
    first = mm.group(1).strip()
    if first in BLOCK_INDICATORS:
        # 块标量或空：收集其后的缩进行
        lines = fm.splitlines()
        block = []
        for i, ln in enumerate(lines):
            if re.match(r"^description:\s*", ln):
                j = i + 1
                while j < len(lines) and (lines[j].startswith(" ") or lines[j].startswith("\t")):
                    block.append(lines[j].strip())
                    j += 1
                return ("\n".join(block) if block else ""), True, m
        return "", True, m
    return first, False, m


def normalize_bilingual(desc):
    """归一化已知的中英夹杂模式（确定性、可安全改写）：
       - 剥掉开头的 'AI Berkshire skill:' / 'AI Berkshire 系列 skill:'
       - 把结尾的 'Source: skills/X' 改成 '。来源：skills/X'
       返回 (new_text, changed)
    """
    new = re.sub(r"^AI Berkshire (?:系列 )?skill[:：]\s*", "", desc)
    new = re.sub(r"\.?\s*Source:\s*skills/", "。来源：skills/", new)
    return new, (new != desc)


ENGLISH_SENTENCE = re.compile(r"(?:[A-Za-z][A-Za-z'\-]*\s+){3,}[A-Za-z][A-Za-z'\-]*")


def has_english_sentence(s):
    """判断是否仍含英文句子（>=4 个连续英文单词）。

    用『连续英文词』而非字母占比，避免把『中文为主、仅夹英文品牌名/文件名』
    的描述（如『来源：skills/bottleneck-hunter.md』『Remotion 最佳实践』）误判为英文。
    """
    return bool(ENGLISH_SENTENCE.search(s or ""))


def cn_backup_and_write(path, new_txt):
    rel = os.path.relpath(path, HOME)
    dst = os.path.join(BACKUP_ROOT, "cn", DATE_STR, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if not os.path.exists(dst):
        shutil.copy2(path, dst)
    open(path, "w", encoding="utf-8").write(new_txt)


def cn(agents, fix):
    print("中文化校验 - 自有 skill 的 description 应为中文(便于 '/' 命令可读):")
    print("=" * 72)
    print("范围: 公共池 ~/.agents/skills/ + WorkBuddy 原生(非软链) skill")
    print("      （53 个 Claude 插件 skill 受规则1约束不在此范围；需另处理）")
    print("-" * 72)
    files = owned_skill_files()
    normalized, needs, already_cn, errors = [], [], 0, 0
    for name, path, scope in files:
        try:
            txt = open(path, encoding="utf-8").read()
        except Exception:
            errors += 1
            continue
        text, is_block, fm_match = parse_description(txt)
        if text is None:
            needs.append((name, scope, "(无 description 字段)", is_block))
            continue
        if text.strip() == "":
            needs.append((name, scope, "(空 description)", is_block))
            continue
        new, changed = normalize_bilingual(text)
        if changed:
            if has_english_sentence(new):
                # 归一化后仍含英文句 -> 当作需翻译项（保留原文本供 agent 处理）
                needs.append((name, scope, text[:70], is_block))
                continue
            # 归一化成功 -> 已是纯中文
            if fix:
                new_line = "description: " + json.dumps(new, ensure_ascii=False)
                # 关键修复：在【整份文件】上替换 description 行，保留 frontmatter 其余字段与正文(body)，
                # 旧实现用 frontmatter 三段重建会丢失 '---' 之后的全部正文。
                new_txt = re.sub(r"^description:.*$", new_line, txt, count=1, flags=re.M)
                cn_backup_and_write(path, new_txt)
            normalized.append((name, scope, new[:40]))
            continue
        if has_english_sentence(text):
            needs.append((name, scope, text[:70], is_block))
        else:
            already_cn += 1

    if normalized:
        print(f"[归一化] {len(normalized)} 项" + ("（已写入）" if fix else "（dry，加 --fix 写入）:"))
        for n, sc, prev in normalized:
            print(f"   {n} ({sc}): {prev}...")
    if needs:
        print(f"\n[需 LLM 翻译] {len(needs)} 项（纯英文 / 空，脚本无法自动翻译，由 agent 用 Edit 写入中文）:")
        for n, sc, cur, is_block in needs:
            flag = " [块标量,需 Edit]" if is_block else ""
            print(f"   - {n} ({sc}){flag}: {cur}")
    print(f"\n已是中文: {already_cn} 项  |  解析错误: {errors}")
    print("=" * 72)
    if not fix:
        print("以上为只读报告。加 --fix 可自动写入『中英夹杂归一化』结果；纯英文项仍需手动翻译后重跑 --mode cn 直到 [需 LLM 翻译]=0。")
    else:
        if needs:
            print(f"归一化已写入。仍有 {len(needs)} 项纯英文/空需翻译：请用 Edit 写入中文描述，再重跑 `bridge.py --mode cn` 确认归零。")
        else:
            print("全部自有 skill 的 description 已为中文（含归一化项）。")


# ---------------------------------------------------------------------------
# 同步回 GitHub（sync）
# ---------------------------------------------------------------------------
def _sync_copy_own_skill():
    """把自有 skill（agent-skill-bridge）的当前真源复制到仓库 my-skills/ 下。"""
    src_pool = os.path.join(USER_SRC, OWN_BRIDGE)
    if os.path.isdir(src_pool):
        src = realpath(src_pool)
    else:
        src = os.path.join(HOME, ".workbuddy", "skills", OWN_BRIDGE)
    if not os.path.isdir(src):
        print(f"    [sync] 未找到自有 skill 源: {src}")
        return False
    dst = os.path.join(MY_REPO, "my-skills", OWN_BRIDGE)
    if os.path.isdir(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    print(f"    [sync] 复制自有 skill -> {dst}")
    return True


def run_sync():
    """第 5 步：把变更同步回 GitHub 仓库（my-agent-skills）。

    - 复制自有 skill 数据进仓库
    - 刷新 inventory 的「最新更新」列（若 refresh_inventory.py 存在）
    - 运行 sync.sh 提交并推送 main（无变更则 sync.sh 自动跳过）
    """
    print("\n=== 第 5 步：同步回 GitHub ===")
    if not os.path.isdir(os.path.join(MY_REPO, ".git")):
        print(f"    仓库不存在或非 git 目录: {MY_REPO} -> 跳过同步（不影响本地）")
        return
    # 1) 复制自有 skill 数据
    _sync_copy_own_skill()
    # 2) 刷新清单「最新更新」列
    refresh = os.path.join(MY_REPO, "scripts", "refresh_inventory.py")
    if os.path.isfile(refresh):
        print("    [sync] 刷新清单最新更新列...")
        subprocess.run([sys.executable, refresh], capture_output=True, text=True)
    # 3) 提交并推送
    sync = os.path.join(MY_REPO, "scripts", "sync.sh")
    if os.path.isfile(sync):
        print("    [sync] 提交并推送到 main...")
        r = subprocess.run(["bash", sync], capture_output=True, text=True)
        if r.stdout.strip():
            print(r.stdout.strip())
        if r.stderr.strip():
            print(r.stderr.strip())
    else:
        print(f"    [sync] 未找到 sync.sh: {sync}")


# ---------------------------------------------------------------------------
# 主入口
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(
        description="Bridge ~/.agents/skills/ into agent default skill dirs via symlinks, with dedup + cn.")
    ap.add_argument("--mode", choices=["dry", "apply", "verify", "dedup", "cn", "sync"], default="dry")
    ap.add_argument("--fix", action="store_true",
                    help="dedup/cn 模式下实际写入修改(默认只读报告)")
    ap.add_argument("--no-sync", action="store_true",
                    help="写操作(apply/cn --fix/dedup --fix)后不自动同步回 GitHub")
    ap.add_argument("--agents", default=",".join(DEFAULT_AGENTS.keys()),
                    help="逗号分隔的 agent 名; 必须是 DEFAULT_AGENTS 中已定义的键")
    args = ap.parse_args()

    agents = {}
    for a in [x.strip() for x in args.agents.split(",") if x.strip()]:
        if a in DEFAULT_AGENTS:
            agents[a] = DEFAULT_AGENTS[a]
        else:
            print(f"[跳过] 未知 agent: {a} (在脚本 DEFAULT_AGENTS 中扩展后可用)")
    if not agents:
        print("无有效 agent，退出")
        return

    user_skills = list_skills(USER_SRC)
    print(f"公共池 skill 数: {len(user_skills)}")
    if args.mode == "dry":
        plan(user_skills, agents)
    elif args.mode == "apply":
        apply(user_skills, agents)
        verify(user_skills, agents)
        if not args.no_sync:
            run_sync()
    elif args.mode == "verify":
        verify(user_skills, agents)
    elif args.mode == "dedup":
        dedup(user_skills, agents, fix=args.fix)
        if args.fix and not args.no_sync:
            run_sync()
    elif args.mode == "cn":
        cn(agents, fix=args.fix)
        if args.fix and not args.no_sync:
            run_sync()
    elif args.mode == "sync":
        run_sync()


if __name__ == "__main__":
    main()
