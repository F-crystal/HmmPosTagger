from flask import Flask, render_template, request, redirect, url_for
import HmmPosTagger as hmm
import re


# 注册app
app = Flask(__name__)
app.debug=True

@app.route('/')
def index():  # 主页
    return render_template('index.html')

# 预先加载标注器, (试图)节约时间
hmmtagger = hmm.HmmPosTagger()
hmmtagger.init_restart('1998-01-2003版-带音.txt')
hmmtagger.train('1998-01-2003版-带音.txt')

@app.route('/tagger')
def tagger():  # 实战页面
    return render_template('tagger.html')

@app.route('/predict',methods=['GET','POST'])
def predict():
    if request.method == 'POST':
        content = request.form['content']  # 获取用户输入内容
        content = content.strip()
        sentence_lst = re.split("\n",content)  # 进行切分
        result = [hmmtagger.viterbi_predict(sentence)+"&" for sentence in sentence_lst]  # 获得结果列表（句子之间）用“&”连接
        return " ".join(result)  # 以字符串的形势进行传输
    

# 运行app
if __name__ == "__main__":
    app.run()