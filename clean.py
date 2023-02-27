# from harvesttext import HarvestText

# def clean(text):
#     ht0 = HarvestText()
#     result = ht0.clean_text(text, norm_html=True)
#     return result



# -*- coding: utf-8 -*-
from goose3 import Goose
from goose3.text import StopWordsChinese

def clean(url):
    # 初始化，设置中文分词
    g = Goose({'stopwords_class': StopWordsChinese})
    #提取，可以传入 url 或者 html 文本：
    article = g.extract(url=url)
    #article = g.extract(raw_html=html)
    return article.title, article.cleaned_text