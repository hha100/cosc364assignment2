file = open("a.txt", 'r')
lines = file.readlines()
file.close()
split_lines = []

for i in lines:
    split_lines.append(i.split())
for h, k in enumerate(split_lines):
    k[1] = float(k[1])
    split_lines[h] = k
    
print(split_lines)
sum1 = 0
sum2 = 0
sum3 = 0
sum4 = 0
sum5 = 0
sum6 = 0
sum7 = 0
for i in split_lines:
    if i[0][2] == '1':
        sum1 += i[1]
    elif i[0][2] == '2':
        sum2 += i[1]
    elif i[0][2] == '3':
        sum3 += i[1]    
    elif i[0][2] == '4':
        sum4 += i[1]   
    elif i[0][2] == '5':
        sum5 += i[1]    
    elif i[0][2] == '6':
        sum6 += i[1]    
    elif i[0][2] == '7':
        sum7 += i[1]    
print("Sum1 = {}, Sum2 = {}, Sum3 = {}, Sum4 = {}, Sum5 = {}, Sum6 = {}, Sum7 = {}, ".format(sum1, sum2, sum3, sum4, sum5, sum6, sum7))

"""
split_dict = {}
for k in split_lines:
    split_dict[k[0]] = k[1]
for i in split_dict:

    
print(split_dict)
"""