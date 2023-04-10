#save_data.py，支持同步和异步
import os
from DataClear import clear
from setting import CLEAR_WHEN_SPIDER, SAVE_AS_ONE_FILE

#定义日志配置
import logging
logging.basicConfig(level=logging.INFO,
    format='%(asctime)s - %(levelname)s : %(message)s')


#这里是异步------------------------------------------------------------------------
async def AsyncSave_data(data, BOOKNAME, addway, sort_No, img_json, ad_list):
    if SAVE_AS_ONE_FILE:
        await AsyncSave_data2One_file(data, BOOKNAME, addway, img_json, ad_list)
    else:
        await AsyncSave_data_Chapters(data, BOOKNAME, addway, sort_No, img_json, ad_list)

#保存数据-分章节
async def AsyncSave_data_Chapters(data, BOOKNAME, addway, sort_No, img_json, ad_list): 
    root = f"./WriteBook/{BOOKNAME}/"
    curr_No = str(data.get('当前页数'))
    name = data.get('名字') + '-@' + str(sort_No) +".txt"
    path =root + name
    if CLEAR_WHEN_SPIDER:#True为清洗完在放入文件中，False为爬取原始HTML，后续再清洗
        BOOKTEXT=clear(data.get('全文'), name, img_json, ad_list).get('text')
    else:
        BOOKTEXT=data.get('全文')
    try:
        if not os.path.exists(root):
            os.makedirs(root)
        if (addway == 'w') and (os.path.exists(path)):
            logging.info("文件已存在")
        else:
            logging.info(f'正在向文件写入 {name} 的第{curr_No}页，请稍候')
            with open(path, addway, encoding='utf-8') as f: #'w' 'a'
                f.write(BOOKTEXT)
                #f.close()
                logging.info('文本【%s】的第%s页的数据保存成功', name, curr_No)
    except:
        logging.info("爬取失败") #'''


#保存数据-全文本
async def AsyncSave_data2One_file(data, BOOKNAME, addway, img_json, ad_list): 
    root='./WriteBook'
    path = root + f'/{BOOKNAME}.txt'
    curr_No = str(data.get('当前页数'))
    name = data.get('名字')
    if CLEAR_WHEN_SPIDER:#True为清洗完在放入文件中，False为爬取原始HTML，后续再清洗
        BOOKTEXT=clear(data.get('全文'), name, img_json, ad_list).get('text')
    else:
        BOOKTEXT=data.get('全文')
    try:
        if not os.path.exists(root):
            os.makedirs(root)
            
        logging.info(f'正在向文件写入 {name} 的第{curr_No}页，请稍候')
        with open(path, 'a', encoding='utf-8') as f: #'w' 'a'
            if addway=='w':
                f.write('\n' + name + '\n  ' + BOOKTEXT)
            else:
                f.write(BOOKTEXT)
            logging.info('文本【%s】的第%s页的数据保存成功', name, curr_No)
    except:
        logging.info("爬取失败") #'''


#这里是同步------------------------------------------------------------------------
def save_data(data, BOOKNAME, addway, sort_No, img_json, ad_list):
    if SAVE_AS_ONE_FILE:
        save_data2One_file(data, BOOKNAME, addway, img_json, ad_list)
    else:
        save_data_Chapters(data, BOOKNAME, addway, sort_No, img_json, ad_list)

#保存数据-分章节
def save_data_Chapters(data, BOOKNAME, addway, sort_No, img_json, ad_list): 
    root = f"./WriteBook/{BOOKNAME}/"
    curr_No = str(data.get('当前页数'))
    name = data.get('名字') + '-@' + str(sort_No) +".txt"
    path =root + name
    if CLEAR_WHEN_SPIDER:#True为清洗完在放入文件中，False为爬取原始HTML，后续再清洗
        BOOKTEXT=clear(data.get('全文'), name, img_json, ad_list).get('text')
    else:
        BOOKTEXT=data.get('全文')
    try:
        if not os.path.exists(root):
            os.makedirs(root)
        if (addway == 'w') and (os.path.exists(path)):
            logging.info("文件已存在")
        else:
            logging.info(f'正在向文件写入 {name} 的第{curr_No}页，请稍候')
            with open(path, addway, encoding='utf-8') as f: #'w' 'a'
                f.write(BOOKTEXT)
                #f.close()
                logging.info('文本【%s】的第%s页的数据保存成功', name, curr_No)
    except:
        logging.info("爬取失败") 


#保存数据-全文本
def save_data2One_file(data, BOOKNAME, addway, img_json, ad_list): 
    root='./WriteBook'
    path = root + f'/{BOOKNAME}.txt'
    curr_No = str(data.get('当前页数'))
    name = data.get('名字')
    if CLEAR_WHEN_SPIDER:#True为清洗完在放入文件中，False为爬取原始HTML，后续再清洗
        BOOKTEXT=clear(data.get('全文'), name, img_json, ad_list).get('text')
    else:
        BOOKTEXT=data.get('全文')
    try:
        if not os.path.exists(root):
            os.makedirs(root)
            
        logging.info(f'正在向文件写入 {name} 的第{curr_No}页，请稍候')
        with open(path, 'a', encoding='utf-8') as f: #'w' 'a'
            if addway=='w':
                f.write('\n' + name + '\n  ' + BOOKTEXT)
            else:
                f.write(BOOKTEXT)
            logging.info('文本【%s】的第%s页的数据保存成功', name, curr_No)
    except:
        logging.info("爬取失败") 
