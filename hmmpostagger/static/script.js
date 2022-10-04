function isChinese(s){
    var pattern_Ch = new RegExp("[\u4E00-\u9FA5]"); //中文的模式
    var s = s.replace(/\s+/g, "");  // 去除空格
    s = s.replace(/[\r\n]/g, "");  // 去除换行
    console.log(s);
    cnt = 0;
    for(var i=0; i< s.length; i++){
        if (!pattern_Ch.test(s[i])){
            return false;
        }
    }
    return true;
}
function tagger(){
    document.getElementById('board').innerHTML = "";  // 清空结果
    var content = document.getElementById("userinput").value;
    if (content == ""){
        alert("请输入句子!") // 对空值进行处理
    }else{
        if(!isChinese(content)){
            alert("请输入中文!") // 对语言进行处理
            document.getElementById("userinput").value = "";  // 清空输入框
        }else{
            document.getElementById("loadtitle").innerHTML = "正在进行分析,请耐心进行等待"  // 更新标题元素
            document.getElementById('result').style.display="none";  // 结果不可见
            document.getElementById('analysis').disabled=true;  // 禁用按钮
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    myfunction(this.responseText);
                    document.getElementById("loadtitle").innerHTML = "输入中文句子, 点击按钮进行词性标注"; // 恢复标题
                    document.getElementById("userinput").value = "";  // 清空输入框
                    document.getElementById('analysis').disabled=false; // 启用按钮
                }
            };
            xhttp.open("POST", "/predict", true);  // 使用异步传输
            xhttp.setRequestHeader('Content-type','application/x-www-form-urlencoded')
            xhttp.send('content='+content);
        }
    }    
}
function myfunction(text){
    document.getElementById('result').style.display="block";  // 结果可见
    var parent = document.getElementById('board');
    seq_lst = text.split("&");  // 切分不同句子
    for(var i = 0; i < seq_lst.length-1;i++){
        seq = seq_lst[i].split(' ')  // 切分句子中的语块
        inner_html = '<p>'
        for(var j=0; j<seq.length;j++){
            token = seq[j].split('/')   // 切分原词和标注
            inner_html += token[0]+'/'+'<span>'+token[1]+'</span>'
            inner_html += "&nbsp;&nbsp;"
        }
        inner_html += '</p>'
        parent.innerHTML +=inner_html  // 向board中添加元素
    }
}