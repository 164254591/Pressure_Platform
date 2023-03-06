import time

print('我是脚本01，我正在被执行', str(time.time())[:10])
time.sleep(30000)
print('脚本01被执行完了', str(time.time())[:10])
