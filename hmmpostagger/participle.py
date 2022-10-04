# encoding:utf-8
# !/usr/bin/python3
import torch
from ltp import LTP
from typing import List


def participle(input_str: str) -> List[str]:
    """
    使用哈工大研发的ltp模型进行分词
    :param input_str: 输入的中文句子字符串
    :return: 输出的分词结果列表
    """
    ltp = LTP("LTP/small")  # 默认加载 Small 模型

    # 将模型移动到 GPU 上
    if torch.cuda.is_available():
        # ltp.cuda()
        ltp.to("cuda")

    output = ltp.pipeline([input_str], tasks=["cws"])
    # 使用字符串格式作为返回结果
    return output.cws[0]
