import string
import math
from sklearn.model_selection  import train_test_split
#from ._validation import cross_validate
#from train_test_split import cross_validate
#from sklearn import cross_validtion

import re
from zhon.hanzi import punctuation

class n_gram:
    def read(self):
        filename = open("train.txt","r",encoding='UTF-8')
        temp  = []
        tri_temp = []
        for line in filename.readlines():
            line = line.strip()
            line = line.strip(string.punctuation)
            array_line = line.split()

            for i in array_line:
                self.length += 1
                if i not in self.unigram_data:
                    self.unigram_data[i] = 1
                else:
                    self.unigram_data[i] += 1

                temp.append(i)
                tri_temp.append(i)

                if len(temp) == 2:
                    temp_str = "".join(temp)
                    if temp_str not in self.bigram_data:
                        self.bigram_data[temp_str] = 1
                    else:
                        self.bigram_data[temp_str] += 1
                    temp.pop(0)

                if len(tri_temp) == 3:
                    temp_str = "".join(tri_temp)
                    if temp_str not in self.trigram_data:
                        self.trigram_data[temp_str] = 1
                    else:
                        self.trigram_data[temp_str] += 1
                    tri_temp.pop(0)
    
    #读文件   
    def read_test(self,path):
        file_test = open(path,"r",encoding='UTF-8')
        temp = []
        temp_tri = []
        for line in file_test.readlines():
            line = line.strip()
            line = line.strip(string.punctuation)
            array_line = line.split()

            for i in array_line:
                self.unigram_test.append(i)

                temp.append(i)
                temp_tri.append(i)
                if len(temp) == 2:
                    temp_str = "".join(temp)
                    self.bigrams_test.append(temp_str)
                    temp.pop(0)

                if len(temp_tri) == 3:
                    temp_str = "".join(temp_tri)
                    self.trigrams_test.append(temp_str)
                    temp_tri.pop(0)

    def __init__(self):
        self.unigram_data = {}
        self.bigram_data = {}
        self.trigram_data = {}
        self.length = 0
        self.unigram_test = []
        self.bigrams_test = []
        self.trigrams_test = []
        self.probability = 0
        self.perplexity = 1
    
    #1-gram模型
    def uni_gram_laplace_smooth(self):
        v = len(self.unigram_test)
        self.probability = 0

        for i in self.unigram_test:
            if i not in self.unigram_data:
                self.unigram_data[i] = 0

            #print("self.unigram_data[i]",self.unigram_data[i],"self.length",self.length)
            self.probability += (math.log2((self.unigram_data[i]+1)/(self.length+v)))*((self.unigram_data[i]+1)/(self.length+v))
        
        self.perplexity = -self.probability
        #self.perplexity = pow(2, -1*self.perplexity)

        print("1-gram 困惑度:",self.perplexity)

        
    
    #2-gram模型
    def big_gram_laplace_smooth(self):
        v = len(self.bigrams_test)
        self.probability = 0


        for i,j in zip(self.unigram_test,self.bigrams_test):
            if j not in self.bigram_data:
                self.bigram_data[j] = 0
            if i not in self.unigram_data:
                self.unigram_data[i] = 0
            self.probability += (math.log2((self.bigram_data[j]+1) / (self.unigram_data[i]+v)))*((self.bigram_data[j]+1) / (self.unigram_data[i]+v))
        
        self.perplexity=-self.probability
        #self.perplexity = pow(2, -self.probability)

        print("2-gram 困惑度：",self.perplexity)
    
    # 3-gram模型
    def tri_gam_laplace_smooth(self):
        v = len(self.trigrams_test)
        self.probability = 0

        for i,j,k in zip(self.unigram_test,self.bigrams_test,self.trigrams_test):
        
            if k not in self.trigram_data:
                self.trigram_data[k] = 0
            if j not in self.bigram_data:
                self.bigram_data[j] = 0
            if i not in self.unigram_data:
                self.unigram_data[i] = 0
            #print("self.trigram_data[k]",self.trigram_data[k],"self.bigram_data[j]",self.bigram_data[j])
            self.probability += (math.log2((self.trigram_data[k]+1) / (self.bigram_data[j]+v)))*((self.trigram_data[k]+1) / (self.bigram_data[j]+v))
        
        self.perplexity=-self.probability
        #self.perplexity = pow(2, -self.probability)

        print("3-gram 困惑度：",self.perplexity)

class train_and_test:
    def __init__(self):
        self.out_train = open('train.txt', 'w',encoding='UTF-8')
        self.out_test = open('test.txt', 'w',encoding='UTF-8')
        self.filename = open('1998-01-105-带音.txt','r',encoding='UTF-8')
        self.datalist = []

    def partition(self):
        '''
        re.sub(pattern, repl, string, count=0, flags=0)
        pattern：表示正则表达式中的模式字符串；
        repl：被替换的字符串（既可以是字符串，也可以是函数）；
        string：要被处理的，要被替换的字符串；
        count：匹配的次数, 默认是全部替换
        '''
        for line in self.filename.readlines():
            line = re.sub(r"/\w*","",line)
            line = re.sub((r"[%s]+"%(punctuation)), "", line)
            line = re.sub(r"\d*","",line)
            line = re.sub(r"-*","",line)
            line = re.sub(r"{.*}","",line)
            line = re.sub(r"\]\w*","",line)
            line = re.sub(r"\[","",line)
            self.datalist.append(line)

        c_train, c_test = train_test_split(self.datalist, test_size=0.2)
        for i in c_train:
        	self.out_train.write(''.join(i))#+'\n')

        for i in c_test:
        	self.out_test.write(''.join(i))#+'\n')

if __name__ == "__main__":
    p = train_and_test()
    p.partition()#划分训练集和测试集

    t = n_gram()
    t.read()
    t.read_test("test.txt")
    t.uni_gram_laplace_smooth()#1-gram
    t.big_gram_laplace_smooth()#2-grams
    t.tri_gam_laplace_smooth()#3-grams
