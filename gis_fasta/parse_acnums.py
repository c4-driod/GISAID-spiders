former_str = 'EPI_ISL_'
middle_str = '-'
sep = ', '


def num_pairs_to_str(nums_list):
    def num_pair_to_str(num1, num2):
        if num1 == num2:
            return former_str + str(num1)
        else:
            return former_str + str(num1) + middle_str + str(num2)

    ac_nums_str = ''
    for i in range(int(len(nums_list) / 2)):
        ac_nums_str += num_pair_to_str(nums_list[2 * i], nums_list[2 * i + 1])
        ac_nums_str += sep
    ac_nums_str = ac_nums_str.rstrip(sep)
    # print('请求字符串为：%s' % ac_nums_str)
    return ac_nums_str


def str_to_num_pair(string):
    if middle_str in string:
        new_list = []
        for i in string.split(middle_str):
            new_list.append(int(i))
        return new_list
    else:
        return [int(string), int(string)]


def transform_to_nums(ac_str):
    # 去除杂质字符
    ac_str = ac_str.replace('\n', '')
    ac_str = ac_str.replace('\r', '')
    ac_str = ac_str.replace(' ', '')
    ac_str = ac_str.replace(former_str, '')
    ac_str = ac_str.rstrip(',')
    # 解析各数对
    ac_list = ac_str.split(',')
    # 真·数对存放位置
    ac_list2 = []
    for item in ac_list:
        # 将数字字符串转为整数对
        num_pair = str_to_num_pair(item)
        sub = num_pair[1] - num_pair[0] + 1
        if sub > 10000:
            # 处理差值大于10000的数对，将其分成多个小于等于10000的数对
            for i in range(int(sub/10000)):
                ac_list2 += [num_pair[0]+10000*i, num_pair[0]+10000*(i+1)-1]
            else:
                ac_list2 += [num_pair[1] - sub % 10000 + 1, num_pair[1]]
        else:
            ac_list2 += num_pair
    return ac_list2


class AcNumAnalysis:
    """
    整个过程中，ac_nums是在不断变少的
    """
    ac_nums = []
    full_length = 0

    def refresh(self, ac):
        # 用ac刷新数字列表，以开始新一次提取
        if type(ac) is str:
            self.ac_nums = transform_to_nums(ac)
        elif type(ac) is list:
            self.ac_nums = ac
        self.full_length = self.get_length()

    def analysis(self):
        # 分析，并输出最靠前的总和10000以内的数对集
        count = 0
        # 记录加入的数
        nums_to_remove = []
        # 找到从开头算起，总和10000及以内的最后一个数， 标记index为mark
        for i in range(int(len(self.ac_nums)/2)):
            new_num_pair = [self.ac_nums[2*i], self.ac_nums[2*i + 1]]
            sub = new_num_pair[1] - new_num_pair[0] + 1

            if count + sub <= 10000:
                count += sub
                nums_to_remove += new_num_pair
                # print('sub:{2}={1}-{0}'.format(new_num_pair[0], new_num_pair[1], sub))
                if count > 9900:
                    break
        print('输出{}个序列'.format(count))

        # 将加入计算的数转化成字符串列表
        str_list = num_pairs_to_str(nums_to_remove)
        # 删除加入的数
        for num in nums_to_remove:
            self.ac_nums.remove(num)
        return str_list

    def get(self):
        while self.ac_nums:
            yield self.analysis()

    def get_whole_list(self):
        ans_list = []
        while self.ac_nums:
            ans_list.append(self.analysis())
        return ans_list

    def get_length(self):
        # 防止线程不安全
        length = 0
        for i in range(int(len(self.ac_nums)/2)):
            length += (self.ac_nums[2*i + 1] - self.ac_nums[2*i] + 1)
        return length


if __name__ == '__main__':
    # test
    bc_str = former_str+'0'+middle_str+'10001,'+former_str+'10004'+middle_str+'40888,'
    a = AcNumAnalysis()
    a.refresh(bc_str)
    for j in a.get():
        print(j)
