#设置用 setting.py

HTML_PATH='WriteBook'#爬取保存在本地的文本路径
CLEAR_PATH='Book'#清洗完毕的文本路径
TEXT_JSON_PATH='Spider/text.json'#img-文本映射json路径 如果从外部调用，要加上Spider
AD_LIST_PATH='Spider/solveList.txt' #广告屏蔽列表地址
FONTDICT_PATH='Spider/FontDisc.json'

DOMAIN_NAME='' #主域名

INDEX_NO='29/29392' #书名 何谓正邪 测试用

SAVE_AS_ONE_FILE=True #是否保存成一个文件

#测试用，True边爬边执行数据清洗，False为爬取原始HTML，爬完再做数据清洗，建议为True。
CLEAR_WHEN_SPIDER=True

SELE_TIME_OUT=30 #Selenium的超时设置
















