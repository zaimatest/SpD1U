HTML = """
我也很舒服。」他起身要走，大海蓓蕾送他到门口，诚恳地说：「祝你武运昌隆，狄先生。」「谢谢你。」狄<img data-cfsrc="/toimg/data/5798715549.png" style="display:none;visibility:hidden;" /><noscript><img src="/toimg/data/5798715549.png" /></noscript>豪<img data-cfsrc="/toimg/data/0744208851.png" style="display:none;visibility:hidden;" /><noscript><img src="/toimg/data/0744208851.png" /></noscript>边穿鞋子，<img data-cfsrc="/toimg/data/0744208851.png" style="display:none;visibility:hidden;" /><noscript><img src="/toimg/data/0744208851.png" /></noscript>边笑说：「下次有机会……再切磋<img data-cfsrc="/toimg/data/0744208851.png" style="display:none;visibility:hidden;" /><noscript><img src="/toimg/data/0744208851.png" /></noscript>下吧。」大海蓓蕾明<img data-cfsrc="/toimg/data/5825662041.png" style="display:none;visibility:hidden;" /><noscript><img src="/toimg/data/5825662041.png" /></noscript>他的意思，害羞地笑了笑，微微点了点<img data-cfsrc="/toimg/data/7092415778.png" style="display:none;visibility:hidden;" /><noscript><img src="/toimg/data/7092415778.png" /></noscript>
"""
HTML1 = """据说这个门派是一个神秘的古老门派，<img data-cfsrc="/toimg/data/4208731327.png" style="display:none;visibility:hidden;"/><noscript>未</noscript>曾在"""


import os
import re
import time
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urljoin #拼接url用


import base64
import hashlib
from Crypto.Cipher import AES

'''
soup=BeautifulSoup(HTML, 'lxml')
soup_as=soup.find_all(name='img')
if len(soup_as) > 0: #有的文本不含img，排除。
    for soup_a in soup_as: 
        if 'data-cfsrc' in str(soup_a):
            img_Url = soup_a.attrs['data-cfsrc']
            print(img_Url) # '''
HTML_img = {
            "imgName": "4208731327.png",
            "text": "未",
            "md5": "bb564c93458158b0cf0aa5b5cd1c7692"
        }
img_aName = '4208731327.png'
HTML_img["text"] = '未'
HTML1 = HTML1.replace(f'<img data-cfsrc="/toimg/data/{img_aName}" style="display:none;visibility:hidden;"/><noscript>{HTML_img["text"]}</noscript>', HTML_img['text'])
print(HTML1)