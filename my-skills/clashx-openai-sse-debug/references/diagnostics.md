# ClashX SSE 诊断参考

## 先核对当前设置

控制 API `127.0.0.1:9090` 和 HTTP 代理 `127.0.0.1:7890` 是原始配置中的默认示例。先在 ClashX 当前设置/配置中确认真实地址、端口、API 是否开启以及是否配置鉴权；不要把这些示例当成本机事实。若控制 API 有密钥，使用当前客户端要求的本机安全方式提供，禁止把密钥打印到终端、日志或对话。

进程与监听端口可以只读检查：

```bash
ps aux | rg '[C]lashX'
lsof -nP -iTCP -sTCP:LISTEN | rg 'Clash|7890|9090'
```

命令输出可能包含用户名、路径或启动参数；只保留诊断所需字段，不复制秘密。

## 只读控制 API 探针

先对照本机 ClashX 版本所支持的控制 API 路由。下列只是常见端点示例，接口可随版本或衍生客户端变化。所有请求应限于 `127.0.0.1`，设置短超时，并只输出必要字段。

```python
import json
import os
import urllib.error
import urllib.request

BASE = os.environ.get("CLASHX_API_BASE", "http://127.0.0.1:9090").rstrip("/")
TOKEN = os.environ.get("CLASHX_API_TOKEN")

def get_json(path):
    request = urllib.request.Request(BASE + path, method="GET")
    if TOKEN:
        # 按本机 API 文档确认鉴权头格式；不要打印 TOKEN。
        request.add_header("Authorization", "Bearer " + TOKEN)
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            return response.status, json.load(response)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
        return None, {"error": type(error).__name__}

status, rules_data = get_json("/rules")
print("rules_status:", status)
rules = rules_data.get("rules", []) if isinstance(rules_data, dict) else []
for rule in rules:
    payload = str(rule.get("payload", ""))
    if "openai" in payload.lower():
        print("matched_rule:", payload, "route:", rule.get("proxy"))

# 仅当该客户端当前版本支持此端点时再执行。
status, connections = get_json("/connections")
print("connections_status:", status)
items = connections.get("connections", []) if isinstance(connections, dict) else []
for item in items[:40]:
    metadata = item.get("metadata", {})
    host = metadata.get("host") or item.get("destination")
    process = metadata.get("process") or metadata.get("processPath")
    if host:
        print("connection:", host, "process:", process or "unknown")
```

API 鉴权头应按当前版本文档设置；某些版本/发行版使用不同字段或根本不暴露同一端点。不要因探针 404、401、500 就自动改设置或重启。

## 比较短请求与 SSE

使用与故障相同的网络、客户端和目标域名；尽量复用无业务数据的健康/模型列表 GET。将代理地址替换为实际配置。不要携带 Authorization、API key 或真实业务内容：

```bash
TARGET_URL='https://api.openai.com/v1/models'
PROXY_URL='http://127.0.0.1:7890'  # 替换为当前配置

curl --silent --show-error --max-time 15 --output /dev/null \
  --write-out 'proxy_status=%{http_code} elapsed=%{time_total}s\n' \
  --proxy "$PROXY_URL" "$TARGET_URL"
```

需要比较系统默认路径时，使用同一个 `TARGET_URL` 去掉 `--proxy`，并遵守用户所在网络的要求。只记录状态码、耗时和错误类别。HTTP `401` 说明远端返回了 HTTP 鉴权错误；它不能单独证明客户端授权可用、目标服务健康或 SSE 长连接稳定。

若已有用户安全批准的 SSE 测试端点，短时运行并记录连接是否持续、首个事件耗时、断开位置和退出码。没有适合的端点时，优先用用户实际请求的无副作用场景复现；不要默认向任意外部服务发送数据或拉取大文件。

DNS 检查应区分系统解析和代理端解析。可用本机 `socket.getaddrinfo()` 或当前 ClashX 版本明确支持的 DNS API 获取结果，但单个解析地址（包括 `108.160.x.x`）本身不足以证明 DNS 污染或代理故障。将结果与当前 resolver、配置和另一条网络路径对照。

## 经过授权的运行时节点切换

只有用户明确要求切换到某个候选节点时，才调用当前 API 的写入端点。先读取当前组和节点列表；确认目标节点存在，并记录原节点以便恢复。使用当前版本文档核对端点、鉴权头和请求体，不要套用固定 emoji 组名或写入猜测的节点名。

示例形状（将占位值替换为用户选定且已核实的值；仅在对应变更获授权后执行）：

```python
import json
import os
import urllib.parse
import urllib.request

base = os.environ["CLASHX_API_BASE"]
group = os.environ["CLASHX_PROXY_GROUP"]
node = os.environ["CLASHX_PROXY_NODE"]
token = os.environ.get("CLASHX_API_TOKEN")
url = base.rstrip("/") + "/proxies/" + urllib.parse.quote(group, safe="")
request = urllib.request.Request(
    url,
    data=json.dumps({"name": node}).encode(),
    method="PUT",
    headers={"Content-Type": "application/json"},
)
if token:
    request.add_header("Authorization", "Bearer " + token)
with urllib.request.urlopen(request, timeout=5) as response:
    print("status:", response.status)
```

通过 GET 再确认新节点；若连接变差，按已记录原节点恢复。不要同时修改规则、DNS 和系统代理，避免无法辨认是哪项改变影响结果。

## 配置更改或重启

若确有证据需要编辑配置，先确认配置的实际来源（本地文件、订阅或客户端托管）并备份该确切文件。只更改用户授权的单项；订阅可能会覆盖本地更改，应在当前客户端中确认保存位置与生效状态。优先使用 ClashX 菜单正常退出，再由用户或已授权流程启动应用；不要用 `kill -9`、清理配置或热重载接口作默认修复。

## 原始包的本机观察（待重新验证）

原始参考记录曾在某个未注明版本的本机环境中观察到：配置热重载后 DNS 探针异常、某些节点的 SSE 稳定性不同、订阅可能覆盖手工配置，以及客户端重启后连接恢复。这些经验可帮助提出假设，但记录没有足够的版本、时间和复现数据来证明因果关系；逐项按当前机器实测后再决定是否处理。
