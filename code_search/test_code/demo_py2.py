# -*- coding: UTF-8 -*-
 
# Filename : test.py
# author by : www.runoob.com
 
# 用户输入数字
num1 = eval(input('输入第一个数字：'))
num2 = eval(input('输入第二个数字：'))
 
# 求和
sum = float(num1) + float(num2)
 
# 显示计算结果
print(('数字 {0} 和 {1} 相加结果为： {2}'.format(num1, num2, sum)))