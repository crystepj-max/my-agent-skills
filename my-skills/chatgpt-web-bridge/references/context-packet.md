# Context Packet 合同

使用以下确切的顺序与标记：

```markdown
BEGIN_CONTEXT_PACKET
packet_id: <唯一本地 id>
requested_reasoner: <用户指定的可见模型，如 GPT-6>

## Objective
<一个决策或问题>

## Acceptance
- <可观察的结果>

## Task State
- <仓库任务：分支、改动状态、相关运行时事实；非仓库任务：背景、受众、范围与已知事实>

## Evidence
- <file:symbol、命令结果或材料出处，附简明事实>

## Constraints
- <兼容性、范围、审批与隐私边界>

## Questions
1. <面向深度推理的聚焦问题>
END_CONTEXT_PACKET
```

优先呈现 Objective、Acceptance、决定性证据与 Constraints。删除不影响决策的历史与实现细节。保留后续要在本地核验答案所需的路径与符号。查不到的事实标注 unknown，不得推断。

目标 1–3K 近似 token。更小的完整任务包有效。不相关的决策拆成多次交接，不要超出 3K。

需求分析与规划任务的写法：Objective 写要产出的分析或规划本身；Acceptance 写用户可验收的产出形态；Task State 写业务背景与受众；Evidence 只放已核实的材料出处；Questions 写需要 ChatGPT 深度展开的关键判断。
