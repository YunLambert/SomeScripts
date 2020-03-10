# A simple script to check using txt
import os
import re

rx = 'AN第1此作业_\d+_'
submitted_list = []
student_list = []
submit_num = 0
for line in open('./2020homework/log.txt', 'r', encoding="utf-8"):
    # print(line)
    submit_num = submit_num+ 1
    # submitted_list.append(''.join(filter(str.isdigit, line)))
    try:
        # print(re.match(rx, line).group())
        
        t = line.replace(re.match(rx, line).group(), "")
        t = t.replace("\n", "")
        # print(t)
        submitted_list.append(t)
    except:
        print("Error:Format error!")
for line in open('./2020homework/student_lists.txt', 'r', encoding = 'utf-8'):
    t = line.replace("\n", "")
    if t in submitted_list:
        continue
    else:
        student_list.append(t)
# print(submitted_list)
print("未交作业同学:")
print(student_list)
print("已交作业人数:{}".format(submit_num))  
