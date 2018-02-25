# coding=utf-8

import requests
from qiniu import Auth, put_data

qiniu_access_key = '1H3USr1wF7hQ80AeRlq_BF0KoEnoJq2atE4UULwp'
qiniu_secret_key = 'awFedibl6FB3L-4FSXG1NY4Qq3MFwiDoZcNFDKTF'


q = Auth(qiniu_access_key, qiniu_secret_key)
bucket_name = 'guppies'
base_url = 'http://oa3rslghz.bkt.clouddn.com/'


def upload_url_to_qiniu(key, url):
    r = requests.get(url)
    return upload_stream_to_qiniu(key, r.content)


def upload_stream_to_qiniu(key, data):
    token = q.upload_token(bucket_name, key, 3600)

    ret, info = put_data(token, key, data)
    return "{base_url}{key}".format(base_url=base_url, key=key)
