# -*- coding:utf-8 -*-
# 队列的实现

class Stack(object):
    def __init__(self):
        self.stack = []

    # 进队
    def append(self, value):
        self.stack.append(value)

    # 出队
    def pop(self):
        return self.stack.pop(0)

    # 是否为空
    def is_empty(self):
        if len(self.stack):
            return False
        else:
            return True

    # 元素数量
    def count(self, value):
        return self.stack.count(value)



    