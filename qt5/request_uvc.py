import requests
import json
from threading import Thread
import os


########  定义一个静态类
class statics(object):
    story = 0
    able = 0


i_story_able = statics()

# url = 'http://121.4.213.28'
url = 'http://127.0.0.1:8089'

headerBlock = {
    'type': 'http.request.start',
    'cache-control': "no-cache",
    'scheme': 'http',
    'root_path': '',
    'http_version': '1.1',
    'method': 'GET',
    'path': '/'
}


################ 获取参数
def query(valuesBlock):
    try:
        valueJson = json.dumps(valuesBlock, indent=4)
        r = requests.get(url, headers=headerBlock,
                         data=valueJson,
                         timeout=2)
    except requests.exceptions.ConnectTimeout:
        print('网络连接有问题，或当前访问人数过多，请检查重试')

    # print(r.content.decode('utf-8'))
    v = json.loads(r.content.decode('utf-8'))

    path_li = './download_text/bean'
    if not os.path.exists(path_li):  # 判断文件存在否，不然创建
        os.makedirs(path_li)

    for index in range(v['number']):
        path_list = [path_li, 'bean' + str(index) + '.txt']
        head = ''
        for path in path_list:
            head = os.path.join(head, path)
        print(head)
        with open(head, "w", encoding='UTF-8') as file:  # ”w"代表着每次运行都覆盖内容
            file.write(v['x' + str(index)][0] + "\n" + v['x' + str(index)][1] + "\n" + v['x' + str(index)][2])


def request_init():
    valuesBlock = {
        'function': 'data'
    }
    for i in range(1):
        # with concurrent.futures.ThreadPoolExecutor() as executor:
        #     future = executor.submit(query)
        t = Thread(target=query(valuesBlock))
        t.start()


# def query(valuesBlock):
#     try:
#         valueJson = json.dumps(valuesBlock, indent=4)
#         r = requests.get(url, headers=headerBlock,
#                          data=valueJson,
#                          timeout=2)
#     except requests.exceptions.ConnectTimeout:
#         print('网络连接有问题，或当前访问人数过多，请检查重试')
#
#     # print(r.content.decode('utf-8'))
#     v = json.loads(r.content.decode('utf-8'))
#
#     path_li = './download_text/{}'.format(v['datasetName'])
#     if not os.path.exists(path_li):  # 判断文件存在否，不然创建
#         os.makedirs(path_li)
#
#     for index in range(v['number']):
#         path_list = [path_li, v['datasetName'] + str(index) + '.txt']
#         head = ''
#         for path in path_list:
#             head = os.path.join(head, path)
#         with open(head, "w", encoding='UTF-8') as file:  # ”w"代表着每次运行都覆盖内容
#             file.write(v['x' + str(index)][0] + "\n" + v['x' + str(index)][1] + "\n" + v['x' + str(index)][2])
#
#
# def request_init(dataset_name):
#     valuesBlock = {
#         'function': 'data_download',
#         'datasetName':dataset_name
#     }
#     for i in range(1):
#         # with concurrent.futures.ThreadPoolExecutor() as executor:
#         #     future = executor.submit(query)
#         t = Thread(target=query(valuesBlock))
#         t.start()

############## 获取数据集成功后名称存入数据库
def query_data_save(valuesBlock):
    try:
        valueJson = json.dumps(valuesBlock, indent=4)
        r = requests.get(url, headers=headerBlock,
                         data=valueJson,
                         timeout=2)
    except requests.exceptions.ConnectTimeout:
        print('网络连接有问题，或当前访问人数过多，请检查重试')

    v = json.loads(r.content.decode('utf-8'))
    return v


def dataset_save(dataset_name):
    valuesBlock = {
        'function': 'dataset_save',
        'dataset_name': dataset_name
    }
    v = query_data_save(valuesBlock)
    return v


############## 获取历史记录
def query_history(valuesBlock):
    try:
        valueJson = json.dumps(valuesBlock, indent=4)
        r = requests.get(url, headers=headerBlock,
                         data=valueJson,
                         timeout=2)
    except requests.exceptions.ConnectTimeout:
        print('网络连接有问题，或当前访问人数过多，请检查重试')

    v = json.loads(r.content.decode('utf-8'))
    ## story值达到一定变为零
    if v['flag']:
        i_story_able.story = 0
    else:
        i_story_able.story = i_story_able.story + 2
    if v['flag2']:
        i_story_able.able = 0
    else:
        i_story_able.able = i_story_able.able + 2

    return v


def request_history_init():
    valuesBlock = {
        'function': 'getHistory',
        'key_story': i_story_able.story,
        'key_able': i_story_able.able
    }
    v = query_history(valuesBlock)
    return v
