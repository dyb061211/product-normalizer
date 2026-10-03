# Diagnosis Rules

## Run Status
1.status==success
- 这个意味着这次运行过程完整，程序没有出错，但不代表数据没有错误

2.status==failed
- 这个意味着这次运行过程失败，程序中止，没有完整运行完

## Status and Issues Combination

1.success+issues[]==0
- 代表这次运行过程成功并且并且没有发现当前 validation 规则定义的问题

2.success+issues[]>0
- 代表这次运行过程成功但是数据有问题，有不合理的地方

3.failed+issues[]==0
- 代表这次运行过程失败，后续都没有执行采集issues的代码

4.failed+issues[]>0
- 代表这次运行过程失败，并且采集到issues

## Error Message

1.Error Message
- 这个代表status==failed的具体原因，但是error message为空时不能编造虚假信息

2.validation issues
- 这个代表原厂数据提供不合理或者有错误

## Tool Failure

- Tool Error表示获取数据失败
- status==failed表示业务运行失败
- 不能把 Tool Error 当成 run failed
