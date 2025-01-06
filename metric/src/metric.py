import pika
import json
import pandas as pd
import os

# Подключение к RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

# Объявление очередей
channel.queue_declare(queue='y_true')
channel.queue_declare(queue='y_pred')

# Словарь для временного хранения данных
messages = {}

log_file = '/app/logs/metric_log.csv'

# Проверим, есть ли файл логов, если нет — создадим с заголовками
if not os.path.exists(log_file):
    with open(log_file, 'w') as f:
        f.write("id,y_true,y_pred,absolute_error\n")

def write_log(message_id, y_true, y_pred):
    abs_error = abs(y_true - y_pred)
    with open(log_file, 'a') as f:
        f.write(f"{message_id},{y_true},{y_pred},{abs_error}\n")
    print(f"Записано в metric_log.csv: id={message_id}, y_true={y_true}, y_pred={y_pred}, absolute_error={abs_error}")

def check_and_log(message_id):
    record = messages[message_id]
    if 'y_true' in record and 'y_pred' in record:
        write_log(message_id, record['y_true'], record['y_pred'])
        # Удаляем запись, чтобы не захламлять память
        del messages[message_id]

def callback_y_true(ch, method, properties, body):
    message = json.loads(body)
    message_id = message['id']
    y_true = message['body']
    if message_id not in messages:
        messages[message_id] = {}
    messages[message_id]['y_true'] = y_true
    check_and_log(message_id)

def callback_y_pred(ch, method, properties, body):
    message = json.loads(body)
    message_id = message['id']
    y_pred = message['body']
    if message_id not in messages:
        messages[message_id] = {}
    messages[message_id]['y_pred'] = y_pred
    check_and_log(message_id)

channel.basic_consume(
    queue='y_true',
    on_message_callback=callback_y_true,
    auto_ack=True
)
channel.basic_consume(
    queue='y_pred',
    on_message_callback=callback_y_pred,
    auto_ack=True
)

print("Сервис metric запущен, ожидание сообщений...")
channel.start_consuming()
