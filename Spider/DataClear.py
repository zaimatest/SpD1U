# DataClear.py
# 可手动执行。
import os
import re
import time
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urljoin  # 拼接url用

import setting
import adsolver
from ujson import load_json

import base64
import hashlib
from Crypto.Cipher import AES
import requests

import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s : %(message)s')


# 调用清理模块会把所有回车等等东西全部删除，因此单独写这个函数删除广告
def only_delete_ad(content, BAN_TEXT_LIST):
    ad_count = 0
    for ban in BAN_TEXT_LIST:
        if ban in content:
            content = content.replace(ban, '')
            ad_count += 1
    logging.info(f'>>处理广告{ad_count}条')
    return content


def __get_md5(self, url) -> str:
    img_url = self.__base_url + '/toimg/data/' + url
    response = requests.get(img_url)
    with open('temp.png', 'wb') as file_obj:
        file_obj.write(response.content)
    file = open("temp.jpg", "rb")
    return hashlib.md5(file.read()).hexdigest()


def get_HTML(path):
    if not os.path.exists(path):
        logging.info('HTML文件不存在')
    else:
        with open(path, 'r', encoding='utf-8') as f:
            HTML = f.read()
    return HTML


def Save_HTML(ROOTPATH, BOOKNAME, filename, HTML, PathType):
    suffix = '.txt'  # 后缀
    if PathType == 'One_file':
        path = ROOTPATH
        suffix = ''  # 传入单个文件的时候，已经带后缀了。
    else:
        path = os.path.join(ROOTPATH, BOOKNAME)

    if not os.path.exists(path):
        os.makedirs(path)

    if setting.SAVE_AS_ONE_FILE:
        with open(os.path.join(path, BOOKNAME) + suffix, 'a', encoding='utf-8') as f:
            f.write(filename + '\n  ' + HTML + '\n \n')
    else:
        with open(os.path.join(path, filename) + suffix, 'w', encoding='utf-8') as f:
            f.write(HTML)

    logging.info(f'已保存至文件{path}')


def get_ad_list():
    BAN_TEXT_LIST = []
    with open(setting.AD_LIST_PATH, 'r', encoding='UTF-8') as f:
        for ban in f.read().split('\n'):
            BAN_TEXT_LIST.append(ban)
    logging.info('屏蔽列表获取成功')
    return BAN_TEXT_LIST


# 根据逆向sojson.v5加密得到的排序方法，用于获取正确的文本顺序。
def get_true_HTML(HTML, ns):
    soup = BeautifulSoup(HTML, 'lxml')
    HTML = soup.find(id='chapter')
    # 加 'utf-8'，避免生成的字符串带有b前缀
    IncList = str(base64.b64decode(ns), 'utf-8').split(',')
    BookList = str(HTML).split("<br/><br/>")
    FNo = IncList[0]
    Booklength = len(BookList)
    Result = ''
    for I in range(1, Booklength + 1):
        Result += BookList[int(IncList[I]) - int(FNo)] + "<br/><br/>"
    return Result


# 判断页面是否需要重新排序
def check_NeedSort(HTML):
    soup = BeautifulSoup(HTML, 'lxml')
    if (len(soup.find_all(id="ad")) > 0) and (
            "_ii_rr(ns);" in list(
        SC.get_text() for SC in soup.find_all(name="script"))):
        return True
    else:
        return False


# 判断页面是否需要进行AES解密
def check_NeedDecipher(HTML):
    soup = BeautifulSoup(HTML, 'lxml')
    if re.search('secret', HTML):
        return True
    else:
        return False


# 对HTML进行AES解密。
def get_true_HTML_AES(secret_Data, secret_pw, ad_list=[]):
    AText = ''
    data = secret_Data[1:len(secret_Data) - 1]
    pw = secret_pw[1:len(secret_pw) - 1]

    pw = hashlib.md5(pw.encode(encoding='UTF-8')).hexdigest()
    IV = bytes(pw[0:16].encode('utf-8'))
    KEY = bytes(pw[-16:].encode('utf-8'))

    decode = base64.b64decode(data)
    cryptor = AES.new(KEY, AES.MODE_CBC, IV)
    AText = cryptor.decrypt(decode)
    AText = AText.decode("utf-8")
    # 第二页解密出的文本没有图片和div节点在，顺便把这些东西清洗了
    AText = re.sub('<br/>', '', AText)
    AText = re.sub('&nbsp;', '', AText)
    AText = re.sub('\xa0', '', AText)
    AText = re.sub('', '', AText)
    AText = re.sub('', '', AText)
    AText = re.sub('', '', AText)
    AText = re.sub('', '', AText)
    AText = re.sub('', '', AText)
    AText = re.sub('', '', AText)
    AText = re.sub('', '', AText)
    if ad_list:
        AText = only_delete_ad(AText, ad_list)  # 广告清理
    return AText


def clear(HTML, filename, img_json, ad_list):
    soup = BeautifulSoup(HTML, 'lxml')
    logging.info(f'待清洗文件{filename}获取成功')

    if re.search('.*-@', filename, re.S):
        filename = re.search('.*-@', filename, re.S).group()
        filename = filename.replace('-@', '')

    # 注意，这里的清洗判断条件未加入广告清洗的判断
    if (len(soup.find_all(name='div')) < 1) and (
            len(soup.find_all(name='img')) < 1):
        logging.info('该文件无需清洗')
        HTML = only_delete_ad(HTML, ad_list)  # 广告清理
        return {'filename': filename, 'text': HTML.strip()}

    for I in list((5 - i) for i in range(1, 5)):  # 避免遗留大量空格而做的处理
        SpaceStr = '&nbsp;' * I
        HTML = re.sub(SpaceStr, '', HTML)  # 替换&nbsp;
        SpaceStr = '\xa0' * I
        HTML = re.sub(SpaceStr, '', HTML)  # 替换\xa0

    HTML = HTML.replace('<br>', '')  # 替换换行
    HTML = HTML.replace('<br/>', '')  # 替换换行
    HTML = HTML.replace('<br >', '')  # 替换换行
    HTML = HTML.replace('<br />', '')  # 替换换行
    HTML = HTML.replace('\n', '')  # 替换换行

    HTML_imgs = []
    soup_as = soup.find_all(name='img')
    if len(soup_as) > 0:  # 有的文本不含img，排除。
        for soup_a in soup_as:
            # img_Url=urljoin(setting.DOMAIN_NAME, soup_a.attrs['src'])
            # 2024.03.27 - 节点改变，不止是含有 <img src，还包括了 <img data-cfsrc
            # 全新节点1：
            # <img data-cfsrc="/toimg/data/5798715549.png" style="display:none;visibility:hidden;" /><noscript><img src="/toimg/data/5798715549.png" /></noscript>
            # 全新节点2:
            # <img data-cfsrc="/toimg/data/4208731327.png" style="display:none;visibility:hidden;"/><noscript>未</noscript>
            if ('src' in str(soup_a)) and ('data-cfsrc' not in str(soup_a)):
                img_Url_1 = urljoin(setting.DOMAIN_NAME, soup_a.attrs['src'])
                img_aName_1 = re.search('/(\w)*?.png', soup_a.attrs['src'], re.S).group()  # img_Url
                img_aName_1 = img_aName_1.replace('/', '')
                img_dist_1 = {'img_Url': img_Url_1,
                            'img_aName': img_aName_1,
                            'text': ''}
                # 去重
                if not (img_dist_1 in HTML_imgs):
                    HTML_imgs.append(img_dist_1)

            if 'data-cfsrc' in str(soup_a):
                img_Url_2 = urljoin(setting.DOMAIN_NAME, soup_a.attrs['data-cfsrc'])
                img_aName_2 = re.search('/(\w)*?.png', soup_a.attrs['data-cfsrc'], re.S).group()  # img_Url
                img_aName_2 = img_aName_2.replace('/', '')
                img_dist_2 = {'img_Url': img_Url_2,
                            'img_aName': img_aName_2,
                            'text': ''}
                # 去重
                if not (img_dist_2 in HTML_imgs):
                    HTML_imgs.append(img_dist_2)

        # 注入文本：
        for HTML_img in HTML_imgs:
            for img2text in img_json['texts']:
                if HTML_img['img_aName'] == img2text['imgName']:
                    HTML_img['text'] = img2text['text']

        # 此处置空，用于后续更新
        # 用于获取图片-文本映射json中没有的图片，并根据其MD5码
        # 分析本地的json库是否存在该图片，如果没有，下载至本地，

        # 替换文本：
        for HTML_img in HTML_imgs:
            if HTML_img['text'] != '':
                img_aName = HTML_img['img_aName']
                img_text = HTML_img['text']
                # 2024.03.27 新加入
                HTML = HTML.replace(img_aName, img_text)

                HTML = HTML.replace('<noscript>', '')
                HTML = HTML.replace('</noscript>', '')

                HTML = HTML.replace('<img src="/toimg/data/', '')

                noscript_is_str_1 = f'<img data-cfsrc="/toimg/data/{img_text}" style="display:none;visibility:hidden;'
                HTML = HTML.replace(noscript_is_str_1, '')

                HTML = HTML.replace(img_aName, img_text)

                # OLD
                # HTML = HTML.replace(f'<img src="/toimg/data/{img_aName}">', HTML_img['text'])
                # HTML = HTML.replace(f'<img src="/toimg/data/{img_aName}"/>', HTML_img['text'])
                # HTML = HTML.replace(f'<img src="/toimg/data/{img_aName}" />', HTML_img['text'])
        print(HTML_imgs)
        print(HTML)

    soup_div = BeautifulSoup(HTML, 'lxml')  # 清除隐藏节点
    del_divs = soup_div.find_all(name='div', attrs={'id': 'chapter'})
    if len(del_divs) > 0:
        for del_div in del_divs:
            HTML = HTML.replace(str(del_div), '')

    div_tags = re.findall('<div.*?>', HTML, re.S)  # 提取出所有的<div 标签>
    if len(div_tags) > 0:
        for div_tag in div_tags:
            HTML = HTML.replace(str(div_tag), '')  # 清除<div 标签>
            HTML = HTML.replace('</div>', '')

    HTML = adsolver.solve_ad_text(HTML, ad_list)  # 广告清理

    # 清洗残留符号
    HTML = HTML.replace('" />', '')
    HTML = HTML.replace('"/>', '')
    HTML = HTML.replace('">', '')

    logging.info(f'文件【{filename}】清洗成功')

    # print(HTML)
    return {'filename': filename, 'text': HTML.strip()}  # 返回章节名，返回的文本删除前后空白


# 清洗对应目录下的文本
def Start_clear():
    Strat = time.time()
    ad_list = get_ad_list()  # 获取广告屏蔽列表
    img_json = load_json(setting.TEXT_JSON_PATH)  # 获取图片对应文本字典
    root = setting.HTML_PATH  # -根目录
    Booklist = os.listdir(root)  # 获取文件夹内书名目录列表

    for BookName in Booklist:  # 注意这里获取到的指示文件夹名-BookName ：书名
        if os.path.isdir(os.path.join(root, BookName)):  # 判断路径是否目录
            Chapterlist = os.listdir(os.path.join(root, BookName))  # 获取书名文件夹内文本列表
            for Chapter in Chapterlist:  # Chapter ：章节名
                if os.path.join(root, BookName, Chapter).endswith('.txt'):  # 判断是否txt文本
                    HTML = get_HTML(os.path.join(root, BookName, Chapter))
                    Data = clear(HTML, Chapter, img_json, ad_list)
                    Save_HTML(setting.CLEAR_PATH, BookName, Data['filename'],
                              Data['text'], PathType='Many_file')
        else:
            if BookName.endswith('.txt'):  # 判断是否txt文本
                HTML = get_HTML(os.path.join(root, BookName))
                Data = clear(HTML, BookName, img_json, ad_list)
                Save_HTML(setting.CLEAR_PATH, BookName, Data['filename'],
                          Data['text'], PathType='One_file')  # '''
    logging.info('清洗耗时：%s秒', str(time.time() - Strat))


def main():
    Start_clear()


if __name__ == '__main__':
    main()
