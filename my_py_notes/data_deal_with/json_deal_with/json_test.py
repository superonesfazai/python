#coding:utf-8

import json

json_string = '{"arrayOfNums":[{"number":0},{"number":1},{"number":2}],\
                "arrayOfFruits":[{"fruit":"apple"},{"fruit":"banana"},\
                {"fruit":"pear"}]}'

json_obj = json.loads(json_string)

print(json_obj.get('arrayOfNums'))
print(json_obj.get('arrayOfNums')[1])
print(json_obj.get('arrayOfNums')[1].get('number')+\
        json_obj.get('arrayOfNums')[2].get('number'))
print(json_obj.get('arrayOfFruits')[2].get('fruit'))
