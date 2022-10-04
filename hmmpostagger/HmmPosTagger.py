# encoding:utf-8
# !/usr/bin/python3
import numpy as np
import participle


class HmmPosTagger(object):
    """
    使用北京大学计算语言学教育部重点实验室的现代汉语切分、标注、注音语料库-1998年1月份样例与规范数据生成语料库，
    对隐马尔可夫模型进行训练，实现对输入句子的词性标注序列预测
    """

    def __init__(self):
        # 初始化语料库(生成状态的集合和可观测符号的集合）
        self._word2id = {}  # 形如{word: id}，其中id用于矩阵的序号
        self._pos2id = {}  # 形如{pos: id}，其中id用于矩阵的序号

        # 初始化转移矩阵、发射矩阵与初始矩阵
        self.A = None
        self.B = None
        self.pi = None

        # 初始化集合长度
        self._pos_length = 0
        self._word_length = 0

    def init_restart(self, dic_file: str, file_type: str = 'gbk') -> None:
        """
        用语料库文件重新生成进行初始化
        :param dic_file: 一个表示语料库文件名称的字符串
        :param file_type: 读取文件时的解码方式，如'gbk'，'utf-8'
        :return: 
        """
        with open(dic_file, encoding=file_type) as data:
            for line in data:
                line = line.strip()  # 去掉头尾空格
                items = line.split(' ')[1:]  # 将内容用空格切分开，并去掉前面的序号
                for item in items:
                    if item == '':  # 忽略空值
                        continue
                    item_list = item.split('/')  # 将每个块拆分成词语和它的词性标注
                    word = item_list[0]  # 获得单词
                    pos = item_list[1]  # 获得词性
                    if len(pos) >= 3:  # 增加对于异常值的处理
                        if ']' in pos:
                            except_items = pos.split(']')
                            pos = except_items[0]
                            items.append(']/' + except_items[1])
                        if '#' in pos:
                            except_items = pos.split('#')
                            pos = except_items[0]
                            items.append( '#/' + except_items[1])
                        if '！' in pos:
                            except_items = pos.split('！')
                            pos = except_items[0]
                            items.append('！/' + except_items[1])

                    # 将词语和词性分别转移到对应的集合中
                    if word not in self._word2id:
                        self._word2id[word] = len(self._word2id)
                    if pos not in self._pos2id:
                        self._pos2id[pos] = len(self._pos2id)

        # 获取对应的集合长度
        self._pos_length = len(self._pos2id)  # 状态集合长度
        self._word_length = len(self._word2id)  # 观测符号集合长度

        # 用长度重新生成矩阵
        self.pi = np.zeros(self._pos_length)  # 初始矩阵：pi[i]表示初始状态是i的概率
        self.A = np.zeros((self._pos_length, self._pos_length))  # 转移矩阵：A[i][j]表示从i状态转移到j状态的概率
        self.B = np.zeros((self._pos_length, self._word_length))  # 发射矩阵：B[i][j]表示在i状态下是观测符号j的概率

    def train(self, train_file: str, file_type: str = 'gbk') -> None:
        """
        利用语料库文件训练模型
        :param train_file: 一个表示训练数据文件名称的字符串
        :param file_type: 读取文件时的解码方式，如'gbk'，'utf-8'
        :return:
        """
        with open(train_file, encoding=file_type) as train_data:
            for line in train_data:
                pre_pos = ''  # 用来记录上一时刻的状态
                line = line.strip()  # 去掉头尾空格
                items = line.split(' ')[1:]  # 将内容用空格切分开，并去掉前面的序号
                for item in items:
                    if item == '':  # 忽略空值
                        continue
                    item_list = item.split('/')  # 将每个块拆分成词语和它的词性标注
                    word = item_list[0]  # 获得单词
                    pos = item_list[1]  # 获得词性
                    if len(pos) >= 3:  # 增加对于异常值的处理
                        if ']' in pos:
                            except_items = pos.split(']')
                            pos = except_items[0]
                            items.append(']/' + except_items[1])
                        if '#' in pos:
                            except_items = pos.split('#')
                            pos = except_items[0]
                            items.append( '#/' + except_items[1])
                        if '！' in pos:
                            except_items = pos.split('！')
                            pos = except_items[0]
                            items.append('！/' + except_items[1])

                    word_id = self._word2id[word]  # 获得单词对应id
                    pos_id = self._pos2id[pos]  # 获得词性对应id

                    # 生成矩阵
                    if not pre_pos:  # 是初始状态
                        self.pi[pos_id] += 1
                        self.B[pos_id][word_id] += 1
                    else:  # 不是初始状态
                        self.A[self._pos2id[pre_pos]][pos_id] += 1
                        self.B[pos_id][word_id] += 1

                    pre_pos = pos  # 更改上一时刻状态

        # 转为概率矩阵（对矩阵进行正则化）
        self.pi = self.pi / sum(self.pi)
        for i in range(self._pos_length):
            if sum(self.A[i]):
                self.A[i] /= sum(self.A[i])
            self.B[i] /= sum(self.B[i])

    def viterbi_predict(self, input_seq) -> str:
        """
        利用viterbi算法计算并输出最有可能的词性标注序列
        :param input_seq:输入的中文句子字符串
        :return:输入字符串对应的词性标注序列
        """
        input_seq = input_seq.strip()  # 去除头尾空格
        token_list = participle.participle(input_seq)  # 获得分词结果
        token_ids = [self._word2id[token] for token in token_list]  # 获得每个词对应的id
        tokens_length = len(token_ids)  # 获得token序列长度

        # viterbi_matrix[i][j] 表示第i时刻为状态j的概率
        # 等于viterbi_matrix[i-1][j]乘以转移概率再乘以发射概率中的最大值
        viterbi_matrix = np.zeros((tokens_length, self._pos_length))
        back_move = np.zeros((tokens_length, self._pos_length), dtype=int)  # back_move[i][j] 表示i时刻状态为j概率最大时的上一个状态

        for i in range(self._pos_length):  # 初始状态的概率计算
            viterbi_matrix[0][i] = self.pi[i] * self.B[i][token_ids[0]]  # 记录初始状态下的概率

        for i in range(1, tokens_length):  # 除了初始时刻的概率计算
            for j in range(self._pos_length):  # 当前时刻的状态
                viterbi_matrix[i][j] = -99
                for k in range(self._pos_length):  # 上一时刻的状态
                    score = viterbi_matrix[i-1][k] * self.A[k][j] * self.B[j][token_ids[i]]
                    if score > viterbi_matrix[i][j]:
                        viterbi_matrix[i][j] = score  # 记录最大概率
                        back_move[i][j] = k  # 记录上一个时刻的状态
        # 回溯最优路径
        best_path_ids = [0 for _ in range(tokens_length)]
        best_path_ids[tokens_length - 1] = int(np.argmax(viterbi_matrix[tokens_length - 1]))
        for i in range(tokens_length - 2, -1, -1):
            best_path_ids[i] = back_move[i + 1][best_path_ids[i + 1]]  # 获取id序列

        id2pos = list(self._pos2id.keys()) # 利用pos to id的字典的键生成id to pos的列表
        best_path = [id2pos[best_path_ids[i]] for i in range(tokens_length)]  # 获取词性序列
        result = [f'{x}/{y}' for x, y in zip(token_list, best_path)]
        return ' '.join(result)


if __name__ == '__main__':
    tagger = HmmPosTagger()
    tagger.init_restart(r'traindata.txt')
    tagger.train(r'traindata.txt')
    sentence = input()
    print(tagger.viterbi_predict(sentence))
