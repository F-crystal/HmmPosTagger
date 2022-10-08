from nltk.corpus import brown
from nltk.tag import pos_tag
import download


download.download_data()  # 下载对应的包和语料库
data = brown.words()
pos_dataset = pos_tag(data)
with open('data.txt','w',encoding='utf-8') as f:
    for i in range(len(pos_dataset)):
        pos_data = list(pos_dataset[i])
        f.write(pos_data[0] + '/' + pos_data[1] +'\n')
    

