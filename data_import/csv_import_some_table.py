# -*- coding:utf-8 -*-
import pymysql
import csv
import time
read_csv_name="oj_only_problem_code.csv"
csvFile=open("{}".format(read_csv_name),"r",encoding="utf8")
reader=csv.reader(csvFile)
# for item in reader:
# 	print(item)
#连接数据库
db_config={
	"host":"127.0.0.1",
	"port":3306,
	"user":"root",
	"password":"123456",
	"db":"child_programming",
	"charset":"utf8"
}
#打开数据库
db_test_login=pymysql.connect(**db_config)
#使用cursor()方法获取操作游标
cursor_test_login=db_test_login.cursor()
#SQL查询语句
# sql_insert_test_re_problem = "INSERT INTO problem(id,title,difficulty,description,input_sample,output_sample,source,create_time,time_limit,memory_limit) VALUES(%d,'%s','%s','%s','%s','%s','%s','%s','%s','%s')"
sql_insert_test_re_problem = "INSERT INTO problemCode(code, language_id_id, problem_id_id) VALUES('%s',%d,%d)"
try:
	flag=1
	for row in reader:
		#执行SQL语句
		code = row[1]
		language_id = int(row[2])
		problem_id = int(row[3])

		# id = int(row[0])
		# title=row[1]
		# difficult=0
		# title_describe=row[3]
		# input_describe=row[4]
		# output_describe=row[5]
		# describe=""
		# if title_describe!="" and title_describe!=None:
		# 	describe+=title_describe
		# if input_describe!="" and input_describe!=None:
		# 	describe+="\n"+input_describe
		# if output_describe!=""and input_describe!=None:
		# 	describe+="\n"+output_describe
		# input_numbers=row[6]
		# output_numbers=row[7]
		
		# c_plus_code=row[8]
		# python_code=row[9]

		# source=row[10]

		#id   language
		#1		C++
		#2		python2
		#3		python3
		# source=row[11]
		# time_limit=row[12]
		# memory_limit=row[13]
		# time=row[16]

		create_time=time.strftime("%Y-%m-%d %H:%M:%S")#24小时格式
		
		# print("title:",title)
		# print("difficult:",difficult)
		# print("describe:",describe)
		# print("input_numbers:",input_numbers)
		# print("output_numbers:",output_numbers)
		# print("source:",source)
#sql_insert_test_re_problem =   "INSERT INTO test_re_problem(title,difficult,`describe`,input_numbers,output_numbers,source,time_limit,memory_limit,create_time) VALUES (%s,%s,%s,%s,%s,%s)"
		# cursor_test_login.execute(sql_insert_test_re_problem % (id,pymysql.escape_string(title),difficult,pymysql.escape_string(describe),pymysql.escape_string(input_numbers),pymysql.escape_string(output_numbers),pymysql.escape_string(source),create_time,3000,65536))
		cursor_test_login.execute(sql_insert_test_re_problem % (pymysql.escape_string(code), language_id, problem_id))

		db_test_login.commit()
		if flag%100==0:
			print(flag)
		flag+=1
except pymysql.Error as e: 
	# 若存在异常则抛出 
	print(e.args) 
cursor_test_login.close()

