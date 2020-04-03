# -*- coding: utf-8 -*-
# Подключаем нужные библиотеки	
import requests
import time
import json
import itertools
from datetime import datetime

# Идентификатор ключа:
# ajeuec7739st1e707qc6
# Ваш секретный ключ:
# AQVN3nMOcaedC44D6YZ-qBMr0eQtlEYkkMk6vJh_

 # Вставьте свой API-ключ 	
key = 'AQVN3nMOcaedC44D6YZ-qBMr0eQtlEYkkMk6vJh_'

# Вставьте свой путь к файлу в бакете. Всё, что в ссылке стоит после знака вопроса, можно стереть — сервер всё равно это проигнорирует
filelink = 'https://storage.yandexcloud.net/audiototext-kurtat/coronus.opus'

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

    # Если не вышли из цикла — выводим сообщение
    #print("Wait!")

# Выводим готовый текст
print("\nMission complete! " + str(datetime.now()-start_time))
text =  ""
# for chunk in req['response']['chunks']:
#     # print(chunk['alternatives'][0]['text'])
#     text = text + (chunk['alternatives'][0]['text']+"\n")

with open('text.txt', 'w') as f:
    for chunk in req['response']['chunks']:
    # print(chunk['alternatives'][0]['text'])
    # text = text + (chunk['alternatives'][0]['text']+"\n")
        f.write((chunk['alternatives'][0]['text']+"\n").capitalize())
    # f.write(text)
    f.close()
# with open('req.txt', 'w') as f:
#     f.write(str(req))
#     f.close()

# with open('response.txt', 'w') as f:
#     f.write(str(req['response']))
#     f.close()

