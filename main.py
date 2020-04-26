# -*- coding: utf-8 -*-
# Подключаем нужные библиотеки	
import requests
import time
import json
import itertools
from datetime import datetime
from user import USER_KEY



 # Вставьте свой API-ключ 	
key = USER_KEY

# Вставьте свой путь к файлу в бакете. Всё, что в ссылке стоит после знака вопроса, можно стереть — сервер всё равно это проигнорирует
filelink = 'https://storage.yandexcloud.net/audiototext-kurtat/programmisty.opus?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=fedd8eb0eedcc0503e1a5a1ac8d12e130e9cab837a40914ba3251650e9e01d2c&X-Amz-Date=20200409T014956Z&X-Amz-Credential=I89EjR7hpjWoYGE7xm7A%2F20200409%2Fru-central1%2Fs3%2Faws4_request'

# Показываем «Облаку», что мы будем распознавать именно длинное аудио
POST = "https://transcribe.api.cloud.yandex.net/speech/stt/v2/longRunningRecognize"

# Формируем сам текст запроса
body ={
    "config": {
        "specification": {
            "languageCode": "ru-RU"
        }
    },
    "audio": {
        "uri": filelink
    }
}

# Формируем заголовок запроса, в котором ссылаемся на API-ключ
header = {'Authorization': 'Api-Key {}'.format(key)}

# Отправляем запрос на распознавание
req = requests.post(POST, headers=header, json=body)

# Получаем технический ответ от сервера и выводим его
data = req.json()

print(data)

# Получаем идентификатор запроса
id = data['id']

# Запрашиваем на сервере статус операции, пока распознавание не будет завершено
print('Waiting', end='')
it = itertools.cycle(['.'] * 3 + ['\b \b'] * 3)
start_time = datetime.now()
while True:
    # Ждём одну секунду
    time.sleep(1)
    print(next(it), end='', flush=True)
    # Пытаемся получить ответ по нашему идентификатору запроса
    GET = "https://operation.api.cloud.yandex.net/operations/{id}"
    req = requests.get(GET.format(id=id), headers=header)
    req = req.json()

    # Если готово — выходим из цикла
    if req['done']: break


# Выводим готовый текст
print("\nMission complete! " + str(datetime.now()-start_time))
text =  ""
# for chunk in req['response']['chunks']:
#     # print(chunk['alternatives'][0]['text'])
#     text = text + (chunk['alternatives'][0]['text']+"\n")

with open('req.json', 'w') as f:
    f.write(str(req))
    f.close()

with open('response.json', 'w') as f:
    f.write(str(req['response']))
    f.close()

with open('text.txt', 'w') as f:
    for chunk in req['response']['chunks']:
    # print(chunk['alternatives'][0]['text'])
    # text = text + (chunk['alternatives'][0]['text']+"\n")
        if chunk['channelTag']=='1':
            f.write((chunk['alternatives'][0]['text']+"\n").capitalize())
        continue
    # f.write(text)
    f.close()


