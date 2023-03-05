import time
print('我是脚本，我正在被执行',str(time.time())[:10])
time.sleep(3)
print('我被执行完了',str(time.time())[:10])