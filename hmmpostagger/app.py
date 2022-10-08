from flask import Flask, render_template, request, redirect, url_for
import HmmPosTagger as hmm
import EnHmmPosTagger as enhmm
import re
import os


# 注册app
app = Flask(__name__)
app.debug=True

@app.route('/')
def index():  # 主页
    return render_template('index.html')

# 预先加载标注器, (试图)节约时间
hmmtagger = hmm.HmmPosTagger()
if os.getcwd()[-12] == 'h':  # 视运行时的工作目录决定相对路径
    hmmtagger.init_restart(r'traindata.txt')
    hmmtagger.train(r'traindata.txt')
else:
    hmmtagger.init_restart(r'hmmpostagger/traindata.txt')
    hmmtagger.train(r'hmmpostagger/traindata.txt')

enhmmtagger = enhmm.EnHmmPosTagger()
if os.getcwd()[-12] == 'h':  # 视运行时的工作目录决定相对路径
    enhmmtagger.init_restart(r'data.txt')
    enhmmtagger.train(r'data.txt')
else:
    enhmmtagger.init_restart(r'hmmpostagger/data.txt')
    enhmmtagger.train(r'hmmpostagger/data.txt')

@app.route('/tagger')
def tagger():  # 实战页面
    return render_template('tagger.html')

@app.route('/predict_ch',methods=['GET','POST'])
def predict_ch():
    if request.method == 'POST':
        content = request.form['content']  # 获取用户输入内容
        content = content.strip()
        sentence_lst = re.split("\n",content)  # 进行切分
        result = [hmmtagger.viterbi_predict(sentence)+"&" for sentence in sentence_lst]  # 获得结果列表（句子之间）用“&”连接
        return " ".join(result)  # 以字符串的形势进行传输
    
@app.route('/predict_en',methods=['GET','POST'])
def predict_en():
    if request.method == 'POST':
        content = request.form['content']  # 获取用户输入内容
        content = content.strip()
        sentence_lst = re.split("\n",content)  # 进行切分
        result = [enhmmtagger.viterbi_predict(sentence)+"&" for sentence in sentence_lst]  # 获得结果列表（句子之间）用“&”连接
        return " ".join(result)  # 以字符串的形势进行传输

# 运行app
if __name__ == "__main__":
    app.run()