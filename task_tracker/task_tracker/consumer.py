import json
import pika
import django
from sys import path
from os import environ

path.append('settings.py')
environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_tracker.settings')
django.setup()

from task_tracker.models import ExternalUser

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', heartbeat=600, blocked_connection_timeout=300))
channel = connection.channel()
channel.queue_declare(queue='accounts-stream')


def callback(ch, method, properties, body):
    account_obj = json.loads(body)
    print(account_obj)
    try:
        if properties.content_type == 'account_created':
            ExternalUser.objects.create(**account_obj)
        elif properties.content_type == 'account_updated':
            try:
                external_user = ExternalUser.objects.get(public_id=account_obj['public_id'])
                external_user.username = account_obj['username']
                external_user.full_name = account_obj['full_name']
                external_user.email = account_obj['email']
                external_user.role = account_obj['role']
                external_user.save()
            except ExternalUser.DoesNotExist:
                ExternalUser.objects.create(**account_obj)
        elif properties.content_type == 'account_deleted':
            try:
                ExternalUser.objects.get(public_id=account_obj['public_id']).delete()
            except ExternalUser.DoesNotExist:
                pass
    except KeyError:
        print('Incorrect account message.')


channel.basic_consume(queue='accounts-stream', on_message_callback=callback, auto_ack=True)
channel.start_consuming()
