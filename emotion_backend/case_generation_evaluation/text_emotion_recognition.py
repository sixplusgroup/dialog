'''
百度的对话情绪识别api
'''
import json

import requests

api_key = 'FWS8GdZsm73UxUS53QgiUYdo'
secret_key = '8VdjVGH8WP1glVp4kGx8NPgpCPSVEVWC'


def get_token():
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(
        api_key, secret_key)
    response = requests.get(host)
    if response:
        return response.json()['access_token']
    return None


def get_text_emotion(text):
    token = get_token()
    host = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/emotion?access_token={}'.format(token)
    d = {'text': text, 'scene': 'customer_service'}
    response = requests.post(host, data=json.dumps(d))
    if response:
        result = response.json()
        emotion = result['items'][0]['label']
        if len(result['items'][0]['subitems']) > 0:
            emotion = emotion + ' ' + result['items'][0]['subitems'][0]['label']
        return emotion
    return None


if __name__ == '__main__':
    print(get_text_emotion('您好，这里是果麦新风客服'))
