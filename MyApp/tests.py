from django.test import TestCase

# Create your tests here.
import time

# a = time.strftime('%Y-%m-%d %H:%M:%S')
# print(a)

import threading
import time


def a(b):
    print('哈哈哈'+b ,time.strftime('%Y-%m-%d %H:%M:%S'))
    time.sleep(3)
    print('呵呵呵',time.strftime('%Y-%m-%d %H:%M:%S'))


# t = threading.Thread(target=a, args=('5'))  # target传函数名称，不要带括号；args传参数名，元组的方式
# t.setDaemon(True)
# t.start()
# t.join()

ts = []
for i in range(10):
    t = threading.Thread(target=a, args=('5'))
    t.setDaemon(True)
    ts.append(t)
for t in ts:
    t.start()
    # t.join()
for t in ts:
    t.join()


