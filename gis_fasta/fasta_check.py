import pickle

obj_filename = ''
with open(obj_filename, 'rb') as f:
    info_dict = pickle.load(f)
count_dict = {}
def count(num_list):
    add = 0
    for i in range(int(len(num_list)/2)):
        add += (num_list[2*i+1] - num_list[2*i] + 1)
    return add

for dates_str in info_dict:
    count_dict[dates_str] = count(info_dict[dates_str])

print('各日期的序列数量为')
print(count_dict)

al = 0
for i in count_dict.values():
    al += i

print('总和%d'% al)

