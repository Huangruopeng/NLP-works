import codecs

#所有词性
ww = []
#所有的词性
pos = []

ww_pos_text = open('word_pos.txt', 'w')
test_text=open('test_data.txt','w')
pos_text = open('pos.txt', 'w')
ww_text = open('word.txt', 'w')
fin = codecs.open("1998-01-105-带音.txt", "r")
nn=0
while(True):
    text = fin.readline()
    # print(text)
    if(text == ""):
        break
    tmp = text.split()
    if tmp:
        tmp.pop(0)
        
        n = len(tmp)
        
        for i in range(0, n):
            word = tmp[i].split('/')
            index = word[1].find("]", 0) #处理复合词
            if(index!=-1):
                word[1]=word[1][:index]
            word[0]=word[0].replace('[', '')#处理复合词           
          
            nn=nn+1

            try:
                ww_pos_text.write(word[0] + '/' + word[1] + ' ')
                test_text.write(word[0]+" ")
            except:
                print(nn,word,tmp[i])
            
            if(word[1] not in pos):
                pos.append(word[1])
                pos_text.write(word[1])
                pos_text.write('\n')      
           
            if(word[0] not in ww):

                ww.append(word[0])
                ww_text.write(word[0])
                ww_text.write('\n')
ww_text.close()
pos_text.close()
ww_pos_text.close()



