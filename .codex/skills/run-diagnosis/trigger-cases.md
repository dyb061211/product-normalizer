# Trigger Cases

## Should Trigger
1.这次 {run_di} 有什么 validation issues
- why:这是在明确请求分析某一次 run 的问题信息，因此属于 run diagnosis 范围

2.分析{run_id}的问题
- why:用户明确要求分析某一次 run 的问题，而不是只读取一个字段

3.{run_id}运行状态错误的原因是什么
- why:用户已经明确询问错误的原因

4.给我一个{run_id}的诊断
- why:诊断应该包括validation issues

5.帮我看看 {run_id} 到底哪里出问题了
- why:它没有直接说 diagnosis，但明显不是只问一个字段，而是在要求完整排查

## Should Not Trigger
1.你好！
- why：这只是一个普通的问候

2.最近有哪些runs
- why:这个只是查询最近有哪些运行过程

3.{run_id}的运行状态是什么？
- why：这个只是询问状态，所以只要返回status就行了

4.MAX_TOOL_ROUNDS 是多少？
- why:这个run diagnosis没有关系

5.{run_id} 是什么时候创建的？
- why:这个只问time，并没有询问run diagnosis


## Boundary Cases
1.帮我看看{run_id}
- why：这个可能只想看detail，也可能是想看完整诊断

2.{run_id}情况怎么样?
- why：这个可能只想看detail，也可能是想看完整诊断
