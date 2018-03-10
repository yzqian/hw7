# 507/206 Homework 7 Part 2
import json
count = 0
#### Your Part 2 solution goes here ####
result_file_name = 'directory_dict.json'
result_file = open(result_file_name, 'r')
contents = result_file.read()
directory_dict = json.loads(contents)
result_file.close()

for item in directory_dict.values():
    tittle_list = list(item.values())
    tittle = tittle_list[0]
    if tittle == 'PhD student':
        count +=1

#### Your answer output (change the value in the variable, count)####
print('The number of PhD students: ', count)
