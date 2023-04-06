""" sample input
2
aaa1 b2 cc3
aaa3
"""

def isNum(n):
    if 48 <= ord(n) <= 57: # 숫자
        return 1
    else: # 문자
        return 0
dict = {}
line_cnt = int(input())
for _ in range(line_cnt):
    sentence = list(map(str, input().split())) # aaa1 bbb2 ddd3
    for word in sentence:
        tmp_str = ''
        tmp_int = ''
        for s in range(len(word)):
            if isNum(word[s]): # 숫자
                tmp_int += word[s]
            else: # 문자
                tmp_str += word[s]
        #exception
        if len(tmp_str) == 0: print('ERROR!! 문자 값이 없습니다.')
        if len(tmp_int) == 0: print('ERROR!! 숫자 값이 없습니다.')

        if tmp_str in dict: #dict에 키 값이 있으면
            dict[tmp_str] += int(tmp_int)
        else: #dict에 키 값이 없으면
            dict[tmp_str] = int(tmp_int)
print('res: ', dict)
print('--------------------------')
for k, v in dict.items():
    print(k,' : ', v)