---
name: run-diagnosis
description: 诊断一次product-normalizer的状态和问题，用户要求分析失败原因、validation issues、问题或完整诊断就应该执行，不要让“只查询一个简单字段 / 最近 runs 列表”也轻易匹配进来
---

# Instructions
诊断某一次 run 的状态和问题，具体执行规则交给下面的 Workflow。

## Workflow
1.确认用户给了run_id，如果没有，就询问用户，不要猜测
2.使用get_run_detail(run_id)查看此次运行过程是否存在，不存在直接返回
3.查看get_run_detail(run_id)返回的status
4.查看get_run_issues(run_id)返回的issues
5.区分情况：
- 需要解释 status / issues / error_message 组合时，再读取 references/diagnosis-rules.md
- get_run_detail运行失败，直接停止后续的get_run_issues，说明连status都不知道
- get_run_detail运行成功，但是get_run_issues运行失败，说明status成功获取，但是无法取得issues
- tool返回错误，说明其工具调用失败，没有取得相应数据，不能编造虚假数据
- mcp connect error，说明都没有走到tool,无法取得对应数据
- 获取 run detail 和 issues 时，只使用 product-normalizer MCP 提供的
get_run_detail 和 get_run_issues。
如果对应 MCP Tool 不可用、连接失败或调用失败：
不得通过 Shell、直接 Python import、Repository、SQLite 等方式绕过 MCP 获取数据
明确说明当前无法取得所需 run 数据
不得根据历史信息或已有记忆生成诊断
6.分析其结果，并返回给用户


## Output
这个是哪个run
最终状态是什么
有多少问题
主要问题是什么
总体诊断是什么