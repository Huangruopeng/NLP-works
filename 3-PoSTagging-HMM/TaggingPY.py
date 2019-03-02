import importlib,sys
importlib.reload(sys)
import codecs

#所有词
ww = []
#所有的词性
pos = []
#每个词出现的评率
fre = {}
#先验概率矩阵
pi = {}
#状态转移概率矩阵
A = {}
#观测概率矩阵
B = {}
B1 = {}
#dp概率
dp = {}
#路径记录
pre = []

ww_text = open('word.txt', 'r')#未标记的词集
pos_text = open('pos.txt', 'r')#词性集
test_text = open('test_data.txt','r')#测试集
fin = codecs.open('word_pos.txt', 'r')#训练集
tag_result = open('tag_result.txt','w')#标注结果

for each in ww_text:
    ww.append(each.replace('\n', ''))#添加所有词
for each in pos_text:
    pos.append(each.replace('\n', ''))#添加所有词性

ww_text.close()
pos_text.close()

#初始化概率矩阵
n = len(pos)
for i in pos:
    pi[i] = 0
    fre[i] = 0
    A[i] = {}
    B[i] = {}
    B1[i] = {}
    for j in pos:
        A[i][j] = 0
    for j in ww:
        B[i][j] = 0
        B1[i][j] = 0

#计算概率矩阵
line = 0

while(True):
    text = fin.readline()
    if(text == '\n'):
        continue
    if(text == ""):#结束
        break
    tmp = text.split()#按空格分割
    len_temp = len(tmp)#语料长度
    line += 1
    for i in range(0, len_temp):
        word = tmp[i].split('/')#按/分割
        pre = tmp[i-1].split('/')#前一个词按/分割]
        #print(word[1])
        fre[word[1]] += 1#统计该词出现频率
        if(i == 1):
            pi[word[1]] += 1#先验概率
        elif(i > 0):
            A[pre[1]][word[1]] += 1#状态转移矩阵概率
        B[word[1]][word[0]] += 1 #观察概率矩阵
        B1[word[1]][word[0]] += 1
fin.close()


for i in pos:
    
    for j in pos:#避免概率0
        A[i][j] += 1
        # print(A[i][j])
    for j in ww:
        B[i][j] += 1
        # print(B[i][j])

for i in pos:
    pi[i] = pi[i]*1.0/line
    for j in pos:
        A[i][j] = A[i][j]*1.0/(fre[i])
    for j in ww:
        B[i][j] = B[i][j]*1.0/(fre[i])
        # print(B[i][j])
print("训练结束！")
print("正在测试，请耐心等待。。。")

while(True):
    text_line = test_text.readline()
   
    if(text_line == ""):
        break    
    text = text_line.split()

    '''
    test_text_string= test_text.read()
    text = test_text_string.split(" ")#按空格分割
    '''
    res = {}
    max_res = {}
    for i in text:
        res[i] = []


    num = len(text)
    for i in range(0, num):
        for j in pos:
            if(B1[j][text[i]] != 0):
                res[text[i]].append(j)

    #维特比算法
    max_end = ""
    for i in range(0, num-1):
        max = 0
   
        for each in res[text[i]]:
            for each1 in res[text[i+1]]:
                if(A[each][each1] > max):
                    max = A[each][each1]
                    max_res[i] = each
                    if(i == num-2):
                        max_end = each1

    max_res[num-1] = max_end

    for i in range(0, num):
        tag_result.write(text[i] + '/' + max_res[i] + ' ')

tag_result = open('tag_result.txt','r')#标注结果
reference = open('ww_pos.txt', 'r')#训练集
start=0 
end=10000 #这里可以自己设置测试范围
a=tag_result.read().split()[start:end]
b=reference.read().split()[start:end]

correctnum=0
num=0
for t1,t2 in zip(a,b):
    num+=1
    if t1.split('/')[1]==t2.split('/')[1]:
        correctnum+=1

print("正确率为:",correctnum/num) 