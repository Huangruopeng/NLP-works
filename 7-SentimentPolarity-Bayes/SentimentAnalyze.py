from nltk.corpus import stopwords
import numpy as np 
import sys


class MySentiment:
    def Bayes(self):
        tp,fp,tn,fn= 0,0,0,0  
        for line in self.temp_pos_test:#判断正面词
            pos_factor = 1.0
            neg_factor = 1.0
            for word in line.split():
                if word in self.subj:
                    pos_factor*= self.Pos_Data[word]
                    neg_factor*= self.Neg_Data[word]
            if pos_factor >= neg_factor:
                tp +=1
            else:
                fn +=1
    
        for line in self.temp_neg_test:#判断消极词
            pos_factor = 1.0
            neg_factor = 1.0
            for word in line.split():
                if word in self.subj:
                    pos_factor *= self.Pos_Data[word]
                    neg_factor *= self.Neg_Data[word]
            if pos_factor > neg_factor:
                fp+=1
            else:
                tn+=1
                
        print("Pos Precision:",tp/(tp+fp))
        print("Pos Recall:",tp/(tp+fn))
        print("Pos F-score:",(2*(tp/(tp+fp))*(tp/(tp+fn)))/(tp/(tp+fp)+tp/(tp+fn)))
        
        print("Neg Precision:",tn/(tn+fn))
        print("Neg Recall:",tn/(tn+fp))
        print("Neg F-score:",(2*(tn/(tn+fn))*(tn/(tn+fp)))/(tn/(tn+fn)+tn/(tn+fp)))
    
    def ReadData(self):
        self.Pos_Data={} # 初始化数据，读文件
        self.Neg_Data={}

        pos = []
      
        for line in open("./data/positive.pos",encoding = "utf-8").readlines():#读取正例
            pos.append(line.strip().lower())#保证都是小写
    
        neg = []
        for line in open("./data/negative.neg",encoding="utf-8").readlines():#读取反例
            neg.append(line.strip().lower())#保证都是小写
    
        train_num = int(len(pos)*0.80)
        temp_Pos_Data = pos[:train_num]
        temp_Neg_Data = neg[:train_num]

        self.temp_pos_test = pos[train_num:]
        self.temp_neg_test = neg[train_num:]

        self.subj = [line.split()[2].split('=')[-1] for line in open('./data/subjclueslen1-HLTEMNLP05.tff','r').readlines()]
        
        ret = list(set(self.subj))
            
        self.subj = ret
    
        for i in self.subj:
            self.Pos_Data[i]=0
            self.Neg_Data[i]=0
    
        for line in temp_Pos_Data:#选取有效词
            for word in line.split():
                if word in self.subj:
                    self.Pos_Data[word]+=1

        for line in temp_Neg_Data:
            for word in line.split():
                if word in self.subj:
                    self.Neg_Data[word]+=1

        for word in self.subj:
            temp = self.Pos_Data[word]
            ntem = self.Neg_Data[word]
            self.Pos_Data[word]=temp/(temp+ntem+1)
            self.Neg_Data[word]=ntem/(temp+ntem+1)

    
if __name__ == '__main__':
    test=MySentiment()    
    test.ReadData()
    test.Bayes()
    




