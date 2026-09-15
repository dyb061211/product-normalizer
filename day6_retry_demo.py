import time

count=0

def fake_request():
    global count
    count+=1
    print(f"正在执行第{count}请求")
    if count<3:
        raise ConnectionError("网络暂求失败")
    return "success"

max_attempts=3

for attempt in range(1,max_attempts+1):
    try:
        result=fake_request()
        print("请求成功",result)
        break
    except ConnectionError as exc:
        print(f"第{attempt}次失败",exc)
        if attempt==max_attempts:
            raise
        delay=2**(attempt-1)
        print(f"等待{delay}秒后重试...")
        time.sleep(delay)