import time
import threading
import json

from flask_cors import CORS
from flask import Flask, redirect, request

import sys
sys.path.append('Spider')
from spider_for_requests import run as runSpider
from setting import HTML_PATH

app = Flask(__name__)
cors = CORS(app)

job = {}  # 任务状态


def do_job(id, Path):
    global job
    global HTML_PATH
    if Path:
        HTML_PATH = Path
    else:
        Path = f'默认位置-脚本根目录/{HTML_PATH}'
    job[id] = '正在下载 保存在 ' + Path
    runlog=runSpider(id)
    if runlog == '已完成':
        job[id] = '已完成 保存在 ' + Path
    else:
        job[id] = runlog


@app.route('/job/<id>', methods=['POST'])
def create(id):
    """创建任务"""
    data = request.get_data()
    json_data = json.loads(data)
    
    Path = json_data.get("Path")
    
    threading.Thread(target=do_job, args=(id, Path,)).start()
    response = redirect(f'/job/{id}')  # 重定向到查询该任务状态
    return response


@app.route('/job/<id>', methods=['GET'])
def status(id):
    """查询任务状态"""
    return job.get(id, '不存在')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
