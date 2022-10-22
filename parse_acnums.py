

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
    return ac_nums_str


def str_to_num_pair(string):
    if middle_str in string:
        new_list = []
        for i in string.split(middle_str):
            new_list.append(int(i))
        return new_list
    else:
        return [int(string), int(string)]


def transform_to_nums(ac_str, default_num=5000):
    if ',' not in ac_str:
        #  应对csv文件的内容
        ac_str = ac_str.replace(former_str, '')
        single_nums = ac_str.split('\n')
        # print(single_nums)
        new_nums = []
        for item in single_nums:
            if item:
                new_nums.append(item)
        new_nums = [int(new_nums[int(i/2)]) for i in range(len(new_nums)*2)]
        return new_nums

    ac_str = ac_str.replace('\n', '')
    ac_str = ac_str.replace('\r', '')
    ac_str = ac_str.replace(' ', '')
    ac_str = ac_str.replace(former_str, '')
    ac_str = ac_str.rstrip(',')
    ac_list = ac_str.split(',')
    ac_list2 = []
    for item in ac_list:
        num_pair = str_to_num_pair(item)
        sub = num_pair[1] - num_pair[0] + 1
        if sub > default_num:
            for i in range(int(sub / default_num)):
                ac_list2 += [num_pair[0] + default_num * i, num_pair[0] + default_num * (i + 1) - 1]
            else:
                ac_list2 += [num_pair[1] - sub % default_num + 1, num_pair[1]]
        else:
            ac_list2 += num_pair
    return ac_list2


class AcNumAnalysis:
    ac_nums = []
    full_length = 0

    def __init__(self):
        self.default_num = 5000
        self.default_sep = 0

    def refresh(self, ac):
        if not ac:
            self.ac_nums = []
        elif type(ac) is str:
            from_file = ',' not in ac
            self.ac_nums = transform_to_nums(ac)
            if from_file:
                self.zip_ac_nums()
        elif type(ac) is list:
            self.ac_nums = ac
        self.full_length = self.get_length()

    def analysis(self):
        count = 0
        nums_to_remove = []
        if self.ac_nums[1] - self.ac_nums[0] >= self.default_num:
            to_return = [self.ac_nums[0], self.ac_nums[0] + self.default_num - 1]
            self.ac_nums[0] = self.ac_nums[0] + self.default_num
            print('\rOutput {} Accession Nums'.format(str(self.default_num)), end='')
            return num_pairs_to_str(to_return)
        for i in range(int(len(self.ac_nums) / 2)):
            new_num_pair = [self.ac_nums[2 * i], self.ac_nums[2 * i + 1]]
            sub = new_num_pair[1] - new_num_pair[0] + 1
            if count + sub <= self.default_num:
                count += sub
                nums_to_remove += new_num_pair
                # print('sub:{2}={1}-{0}'.format(new_num_pair[0], new_num_pair[1], sub))
                if count >= self.default_num - self.default_sep:
                    break
        print('\rOutput {} Accession Nums'.format(count), end='')

        str_list = num_pairs_to_str(nums_to_remove)
        for num in nums_to_remove:
            self.ac_nums.remove(num)
        return str_list, count

    def get(self):
        while self.ac_nums:
            yield self.analysis()

    def get_whole_list(self):
        ans_list = []
        while self.ac_nums:
            ans_list.append(self.analysis()[0])
        return ans_list

    def get_length(self):
        length = 0
        for i in range(int(len(self.ac_nums) / 2)):
            length += (self.ac_nums[2 * i + 1] - self.ac_nums[2 * i] + 1)
        return length

    def zip_ac_nums(self):
        new_ac_nums = []
        current_num_pair = []
        for i in range(int(len(self.ac_nums)/2)):
            if not current_num_pair:
                current_num_pair = [self.ac_nums[2*i], self.ac_nums[2*i+1]]
            else:
                if self.ac_nums[2*i] == current_num_pair[1] + 1:
                    current_num_pair[1] = self.ac_nums[2*i+1]
                else:
                    new_ac_nums += current_num_pair
                    current_num_pair = [self.ac_nums[2*i], self.ac_nums[2*i+1]]
        new_ac_nums += current_num_pair
        self.ac_nums = new_ac_nums


if __name__ == '__main__':
    a = AcNumAnalysis()
    with open('GISAID_hcov-19_ids_2022_07_20_12_50.csv') as f:
        a.refresh(f.read())
    w = a.get_whole_list()
    print(w[0])
    # print(len(w[0]))
