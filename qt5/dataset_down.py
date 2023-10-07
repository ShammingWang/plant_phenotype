# -*- coding=utf-8
import logging
import sys
import json
import os

from qcloud_cos3 import CosConfig
from qcloud_cos3 import CosS3Client
from qcloud_cos3.cos_threadpool import SimpleThreadPool

# 正常情况日志级别使用INFO，需要定位时可以修改为DEBUG，此时SDK会打印和服务端的通信信息
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

secret_id = 'AKIDymOnyuc6MNAl8HvKVSAev41jDTWYP3Sd'  # 替换为用户的 SecretId，请登录访问管理控制台进行查看和管理，
secret_key = 'zjFWYO0Nn0zkGXcT5UlrkS1NWVJuITTJ'  # 替换为用户的 Secret
region = 'ap-nanjing'  # 桶的Location 可以client.list_buckets 查看获取
# COS支持的所有region列表参见https://cloud.tencent.com/document/product/436/6224
token = None  # 如果使用永久密钥不需要填入token，如果使用临时密钥需要填入，临时密钥生成和使用指引参见https://cloud.tencent.com/document/product/436/14048
config = CosConfig(Region=region, Secret_id=secret_id, Secret_key=secret_key, Token=token)
client = CosS3Client(config)

# 用户的 bucket 信息
Bucket = 'scanner-1313227732'

delimiter = ''

# 列出当前目录子节点，返回所有子节点信息
def listCurrentDir(prefix):
    file_infos = []
    sub_dirs = []
    marker = ""
    count = 1

    while True:
        response = client.list_objects(Bucket, prefix, delimiter, marker)
        # 调试输出
        # json_object = json.dumps(response, indent=4)
        count += 1

        if "CommonPrefixes" in response:
            common_prefixes = response.get("CommonPrefixes")
            sub_dirs.extend(common_prefixes)

        if "Contents" in response:
            contents = response.get("Contents")
            file_infos.extend(contents)

        if "NextMarker" in response.keys():
            marker = response["NextMarker"]
        else:
            break
    # 如果 delimiter 设置为 "/"，则需要进行递归处理子目录，
    # sorted(sub_dirs, key=lambda sub_dir: sub_dir["Prefix"])
    # for sub_dir in sub_dirs:
    #     print(sub_dir)
    #     sub_dir_files = listCurrentDir(sub_dir["Prefix"])
    #     file_infos.extend(sub_dir_files)

    sorted(file_infos, key=lambda file_info: file_info["Key"])
    # for file in file_infos:
    #     print(file)
    return file_infos

# 下载文件到本地目录，如果本地目录已经有同名文件则会被覆盖；
# 如果目录结构不存在，则会创建和对象存储一样的目录结构
def downLoadFiles(file_infos):
    localDir = "./download_dataset/"

    pool = SimpleThreadPool()
    for file in file_infos:
        # 文件下载 获取文件到本地
        file_cos_key = file["Key"]
        localName = localDir + file_cos_key

        # 如果本地目录结构不存在，递归创建
        if not os.path.exists(os.path.dirname(localName)):
            os.makedirs(os.path.dirname(localName))

        # skip dir, no need to download it
        if str(localName).endswith("/"):
            continue

        # 实际下载文件
        # 使用线程池方式
        # pool.add_task(client.download_file,Bucket, file_cos_key, localName)

        # 简单下载方式
        response = client.get_object(
            Bucket=Bucket,
            Key=file_cos_key,
        )
        response['Body'].get_stream_to_file(localName)

    pool.wait_completion()
    return None


# 功能封装，下载对象存储上面的一个目录到本地磁盘
def downLoadDirFromCos(prefix):
    global file_infos
    file_infos = listCurrentDir(prefix)

    downLoadFiles(file_infos)
    return None

def dataset_init():
    start_prefix = 'usr1_eve/masks/input1/'    #（测试）
    downLoadDirFromCos(start_prefix)

# def dataset_init(dataset_name):
#     start_prefix = 'usr1_eve/masks/{}'.format(dataset_name)
#     downLoadDirFromCos(start_prefix)