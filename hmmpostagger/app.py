from flask import Flask, render_template, request, redirect, url_for
import HmmPosTagger as hmm
import re


# 注册app
app = Flask(__name__)
app.debug=True

@app.route('/')
def index():  # 重定向到主页
    return redirect(url_for('index'))

@app.route('/index')
def welcome():  # 主页
    return render_template('index.html')

# 预先加载标注器, 节约时间
hmmtagger = hmm.HmmPosTagger()
hmmtagger.init_restart('../hmm/1998-01-2003版-带音.txt')
hmmtagger.train('../hmm/1998-01-2003版-带音.txt')

@app.route('/tagger')
def tagger():  # 实战页面
    return render_template('tagger.html')

@app.route('/predict',methods=['GET','POST'])
def predict():
    if request.method == 'POST':
        content = request.form['content']
        sentence_lst = re.split("\n",content)
        result = [hmmtagger.viterbi_predict(sentence)+"&" for sentence in sentence_lst]
        return " ".join(result)
    

# 运行app
if __name__ == "__main__":
    app.run()