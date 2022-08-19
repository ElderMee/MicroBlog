import hashlib
import http.client
import json
import random
from urllib import parse

from flask import current_app
from flask_babel import _


def translate(q, fromLang, toLang):
    if 'APPID' not in current_app.config or not current_app.config['APPID']:
        return _('Error:the translation service is not configured.')
    if 'BD_TRANSLATOR_KEY' not in current_app.config or not current_app.config['BD_TRANSLATOR_KEY']:
        return _('Error:the translation service is not configured.')
    appid = current_app.config['APPID']
    secretKey = current_app.config['BD_TRANSLATOR_KEY']

    httpClient = None
    myurl = '/api/trans/vip/translate'
    salt = random.randint(32768, 65536)

    sign = appid + q + str(salt) + secretKey
    m1 = hashlib.md5()
    m1.update(sign.encode(encoding='utf-8'))
    sign = m1.hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + parse.quote(q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign

    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)

        response = httpClient.getresponse()  # response是HTTPResponse对象
        r = response.read().decode('utf-8')
        d = json.loads(r)

        l = d['trans_result']
        l1 = l[0]['dst']

        return (l1)
    except Exception as e:
        print(e)
    finally:
        if httpClient:
            httpClient.close()
