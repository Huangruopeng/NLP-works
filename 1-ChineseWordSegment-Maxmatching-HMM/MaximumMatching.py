import pandas as pd
import numpy as np
import pickle

#加载字典
def get_dict(path):
    df = pd.read_csv(path, sep = " ", names = ["word", "1", "2"])
    wordDict = set(df['word'])
    return wordDict


class TrieNode(object):
    def __init__(self):
        self.children = {}
        self.end = False

class Trie(object):
    def __init__(self):
        self.root = TrieNode()

    #添加词语
    def add_words(self, words):
        node = self.root
        for word in words:
            if not word in node.children:
                node.children[word] = TrieNode()
            node = node.children[word]
        node.end = True if words else False

    #查找一个语句的从i开始的最长词语
    def search_words(self, words, start):
        end = start + 1
        node = self.root
        for i in range(start, len(words)):
            if words[i] in node.children:
                node = node.children[words[i]]
                if node.end:
                    end = i + 1
            else:
                return end
        return end

    def match(self, words):
        start = 0
        newWords = ""
        while start < len(words):
            end = self.search_words(words, start)
            newWords += "  " + words[start: end]
            start = end
        return newWords.strip()


#正向匹配
def positive_match(words, word_dict):
    maxLen = len(max(word_dict, key = lambda x: len(x)))
    length = len(words)
    start, end = 0, 0
    newWords = ""
    while start < length:
        end = min(length, start + maxLen)
        while start + 1 < end and (not words[start: end] in word_dict):
            end -= 1
        newWords += " " + words[start: end]
        start = end
    return newWords.strip()

#逆向匹配
def reverse_match(words, word_dict):
    maxLen = len(max(word_dict, key = lambda x: len(x)))
    length = len(words)
    start, end = length, length
    newWords = ""
    while end > 0:
        start = max(0, end - maxLen)
        while start + 1 < end and (not words[start: end] in word_dict):
            start += 1
        newWords = words[start: end] +  " " + newWords
        end = start
    return newWords.strip()


def get_num(x):
    ans_set, res_set = set(x[0].split("  ")), set(x[1].split("  "))
    get_num.answer_num += len(ans_set)
    get_num.result_num += len(res_set)
    get_num.result_correct_num += len(ans_set & res_set)

#加载词典****
word_path = "icwb2-data/gold/pku_training_words.txt"
word_dict =  set(pd.read_csv(word_path, names = ["word"], encoding = "gbk")["word"])


#测试*****
#构建字典树
trie = Trie()
list(map(trie.add_words, word_dict))

dev_path = "icwb2-data/testing/pku_test.txt"
dev_label_path = "icwb2-data/gold/pku_test_gold.txt" 

dev_data = pd.read_csv(dev_path, encoding = "gbk", names = ["origin"])
dev_label = pd.read_csv(dev_label_path, encoding = "gbk", names = ["correct_answer"])
dev_data = pd.concat([dev_data, dev_label], axis = 1)


#切分后数据
dev_data["result"] = dev_data["origin"].map(trie.match)

#计算P,R,F
get_num.answer_num, get_num.result_num, get_num.result_correct_num = 0, 0, 0
dev_data[["correct_answer", "result"]].apply(get_num, axis = 1)

P = get_num.result_correct_num/get_num.answer_num#测试召回率以及准确率
R = get_num.result_correct_num/get_num.result_num

F1 = 2*P*R/(P + R)
print("P is: ", P)
print("R is: ", R)
print("F1 is: ", F1)

