import time
from threading import Thread, Lock
from skimage import io
import os
import PIL.Image as Image


#  二值化
def Towb(image):
    threshold = 100
    for i in range(len(image)):
        for j in range(len(image[i])):
            for k in range(len(image[i, j])):
                if image[i, j, k] < threshold:
                    image[i, j, k] = 0
                else:
                    image[i, j, k] = 255


#  裁剪到不留白
def cutData(data):
    xmin, ymin, xmax, ymax = 100000, 100000, -10000, -10000
    datax = len(data)
    datay = len(data[0])
    #  获取边界值
    for i in range(datax):
        for j in range(datay):
            if data[i, j, 0] == 0:
                #  黑色像素点
                if i < xmin:
                    xmin = i
                if i > xmax:
                    xmax = i
                if j < ymin:
                    ymin = j
                if j > ymax:
                    ymax = j
    #  裁剪
    data = data[xmin:xmax + 1, ymin:ymax + 1]
    return data


#  字母顺序先后规则
def CharOrder(char1, char2):
    rawList = ['2', '3', '4', '5', '6', '7', '8', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'k', 'm', 'n', 'p', 'r', 'w',
               'x', 'y']
    easyList = ['2', '3', '7', 'c', 'n', 'r', 'x', 'f']
    thirdEasyList = ['r']

    rightChar = str('rightChar')
    #  首先确保字符是两个列表中的
    if char1 not in rawList or char2 not in rawList:
        return '字符不在检查范围内！'

    def ifIn(char1, char2, lis):
        return char1 in lis and char2 not in lis

    def ise(c1, c2):
        if ifIn(c1, c2, thirdEasyList) or ifIn(c1, c2, easyList):
            return True

    if ise(char1, char2):
        rightChar = char2
    elif ise(char2, char1):
        rightChar = char1
    else:
        rightChar = char1

    return rightChar


def transChar(c):
    c = c[0]
    return c


class CharOcr:
    def __init__(self, charsdir='./charsPrecise'):
        self.charsdir = charsdir
        if not os.path.exists(self.charsdir):
            os.mkdir(self.charsdir)
        self.load()

    #  字符数组列表 [[name,array],]
    CharArrayList = list()

    #  储存字符图片
    def store(self, CharName, CharArray):
        imgToStore = Image.fromarray(CharArray)
        imgToStore.save(self.charsdir + CharName + '.png')

    #  加载指定名字的字符数组到CharArrayList
    def loadOne(self, CharName):
        CharArray = io.imread(self.charsdir + '/' + CharName + '.png')
        #  二值化数组
        Towb(CharArray)
        #  裁剪不留白
        CharArray = cutData(CharArray)
        self.CharArrayList.append([CharName, CharArray])

    #  加载目录下的所有图片为字符数组
    def load(self):
        for file in os.listdir(self.charsdir):
            filename = os.path.splitext(file)
            if filename[-1] == '.png':
                name = filename[0]
                self.loadOne(name)

    #   匹配一个字符，并描成黄色
    def findOneChar(self, TargetArray, CharArray):
        # plt.subplot(1,2,1)
        # plt.imshow(CharArray)
        answerList = list()
        data = CharArray
        datax = len(data)
        datay = len(data[0])

        #  对比两个相同大小数组中，thedata中是否包含data
        def oneCheck(thedata):
            #  允许的最大不同像素数
            maxWrong = 0
            counter = 0
            for i in range(datax):
                for j in range(datay):
                    if data[i, j, 0] == 0:
                        #  字符数据为黑色
                        if thedata[i, j, 0] == 255:
                            #  而目标数据为白色
                            if counter < maxWrong:
                                counter += 1
                            else:
                                return False
            return True

        # 对验证码图片特定部位进行扫描
        for ti in [23, 24, 30, 31]:
            # 第24、25、31、32
            for tj in range(11, 138 - datay + 1):
                #  12~138
                ifSame = oneCheck(TargetArray[ti:ti + datax, tj:tj + datay])
                if ifSame:
                    answerList.append((ti, tj))

        def onedraw(datatocheck, x, y):
            for i in range(datax):
                for j in range(datay):
                    if data[i, j, 0] == 0:
                        #  绘制成绿色
                        datatocheck[x + i, y + j, 0] = 0
                        datatocheck[x + i, y + j, 1] = 255
                        datatocheck[x + i, y + j, 2] = 0

        for cord in answerList:
            onedraw(TargetArray, cord[0], cord[1])

        return answerList

    #  找到所有可能的字符
    def findChar(self, TargetArray):
        #  结果字典{x:name,}
        AnswerDict = dict()
        lock = Lock()

        #  单个字符扫描
        def DoOneChar(Name, CharArray):
            answerList = self.findOneChar(TargetArray, CharArray)
            if len(answerList) != 0:
                for y, x in answerList:
                    #  如果有结果，将[name,x]加入theAnswer
                    lock.acquire()
                    if x in AnswerDict:
                        AnswerDict[x] = CharOrder(AnswerDict[x], Name[0])
                    else:
                        AnswerDict[x] = Name[0]
                    lock.release()

        #  每个字符都试一遍
        for Name, CharArray in self.CharArrayList:
            thread = Thread(target=DoOneChar, args=(Name, CharArray))
            thread.start()
            thread.join()

        #  结果横坐标储存列表
        xList = list()

        #  横坐标计算列表
        ansList = list()
        for x in AnswerDict:
            ansList.append(x)
        ansList.sort()

        #  最终字符
        answer = ''

        def getFinalStr(maxSep=15):
            answer = str('')
            #  计算正确排序
            for i in range(len(ansList)):
                # print('xList:'+str(xList))
                if i == 0:
                    #  第一个识别出来的元素，默认为正常识别
                    answer += AnswerDict[ansList[0]]
                    xList.append(ansList[0])
                elif ansList[i] - xList[-1] > maxSep:
                    #  如果和前一个字符距离大于定值，为正常识别，加入最终字符串
                    answer += AnswerDict[ansList[i]]
                    xList.append(ansList[i])
                else:
                    #  和前一个字符距离小于定值，算法解决
                    char1 = AnswerDict[ansList[i]]
                    char2 = AnswerDict[xList[-1]]
                    finalchar = CharOrder(char2, char1)
                    if finalchar == char1 and char1 != char2:
                        #  新字符是正确的
                        xList[-1] = ansList[i]
                        answer = answer[:-1]
                        answer += char1
            return answer

        if len(AnswerDict) <= 5:
            print('len<5')
            answer = getFinalStr()
        else:
            maxSep = 15
            for i in range(3):
                answer = getFinalStr(maxSep)
                length = len(answer)
                if length == 5:
                    break
                elif length > 5:
                    maxSep += 1
                    answer = getFinalStr(maxSep)
                else:
                    maxSep -= 1
                    answer = getFinalStr(maxSep)

        return answer

    #  识别图片中的字符
    def Ocr(self, TargetFileName):
        TargetArray = io.imread(TargetFileName)
        #  二值化目标图片
        Towb(TargetArray)
        #  裁剪目标图片到不留白
        # TargetArray = cutData(TargetArray)决定不裁剪
        answer = self.findChar(TargetArray)
        return answer


if __name__ == '__main__':
    #  测试
    ocrr = CharOcr()
    t1 = time.time()
    ans = ocrr.Ocr('test4.png')
    t2 = time.time()
    print('用时：', t2 - t1, 's')
    print(ans)
