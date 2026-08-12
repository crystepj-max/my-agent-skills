import urllib.request, json, os

POOL = os.path.expanduser("~/.agents/skills")
REPO = "mattpocock/skills"
BRANCH = "main"
skills = {
    "wizard": "skills/engineering/wizard",
    "to-questionnaire": "skills/productivity/to-questionnaire",
    "wait-what": "skills/productivity/wait-what",
}

def api(path):
    req = urllib.request.Request(
        f"https://api.github.com/repos/{REPO}/{path}",
        headers={"User-Agent": "workbuddy", "Accept": "application/vnd.github+json"})
    return json.load(urllib.request.urlopen(req, timeout=30))

def raw(path):
    url = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/{path}"
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent":"wb"}), timeout=30).read()

# 1. recursive tree
tree = api(f"git/trees/{BRANCH}?recursive=1")["tree"]
blobs = [t for t in tree if t["type"] == "blob"]

for name, prefix in skills.items():
    files = [b for b in blobs if b["path"].startswith(prefix + "/")]
    dest = os.path.join(POOL, name)
    os.makedirs(dest, exist_ok=True)
    for b in files:
        rel = b["path"][len(prefix) + 1:]  # strip "skills/<cat>/<name>/"
        target = os.path.join(dest, rel)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        data = raw(b["path"])
        with open(target, "wb") as f:
            f.write(data)
        print(f"{name}: wrote {rel} ({len(data)} bytes)")
    print(f"--- {name} done, {len(files)} files ---")
print("ALL DONE")
