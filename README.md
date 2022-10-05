# My HMMPosTagger
个人作业,使用北京大学计算语言学教育部重点实验室的现代汉语切分、标注、注音语料库-1998年1月份样例与规范数据生成语料库,对隐马尔可夫模型进行训练,实现对输入句子的词性标注序列预测

## 运行项目
推荐使用命令行运行项目

### 下载项目
```
git clone https://github.com/F-crystal/HmmPosTagger.git
```

### 打开根目录
```
cd HmmPosTagger
```

### 创建虚拟环境
```
python3 -m venv venv
```

### 运行虚拟环境
```
. venv/bin/activate
```

### 安装对应包
包括flask, torch, ltp等(推荐使用pip下载)
```
pip install flask
pip install torch
pip install ltp
```

### 打开文件目录
```
cd hmmpostagger
```

### 开始运行吧
```
flask run
```
