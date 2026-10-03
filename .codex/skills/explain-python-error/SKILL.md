---
name: explain-python-error
description: 帮用户解释Python报错，用户给出用户提供 Python error、exception、traceback 并希望理解原因时，你要解释
---

# Instructions
用户给出python error你要去识别错误类型，看traceback最后一层，给出用户解释并且可能错误的原因


## Workflow
1.用户给出python error
2.你识别错误类型
3.查看traceback最后一层
4.判断错误属于 Syntax / Import / Runtime 哪一类
5.总结出可能错误的原因并给出最小的修改方向

## Output
是什么错误，错在哪里，为什么，应该从哪里开始修改
