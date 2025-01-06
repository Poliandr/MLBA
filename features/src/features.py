import pika
import numpy as np
import json
import time
from datetime import datetime
from sklearn.datasets import load_diabetes

# Загружаем датасет о диабете
X, y = load_diabetes(return_X_y=True)

# Создаём подключение по адресу rabbitmq:
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

# Создаём очереди
channel.queue_declare(queue='y_true')
channel.queue_declare(queue='features')

# Создаём бесконечный цикл для отправки сообщений в очередь
while True:
    try:
        # Формируем случайный индекс строки
        random_row = np.random.randint(0, X.shape[0] - 1)

        # Формируем id сообщения на основе временной метки
        message_id = datetime.timestamp(datetime.now())

        # Формируем сообщения
        message_y_true = {
            'id': message_id,
            'body': float(y[random_row])
        }

        message_features = {
            'id': message_id,
            'body': X[random_row].tolist()
        }

        # Публикуем сообщения
        channel.basic_publish(exchange='',
                            routing_key='y_true',
                            body=json.dumps(message_y_true))
        channel.basic_publish(exchange='',
                            routing_key='features',
                            body=json.dumps(message_features))

        print(f"Отправлено в y_true: {message_y_true}")
        print(f"Отправлено в features: {message_features}")

        # Интервал отправки сообщений
        time.sleep(5)

    except Exception as e:
        print(f"Ошибка при отправке сообщений: {e}")
        time.sleep(5)