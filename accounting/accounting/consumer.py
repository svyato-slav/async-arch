import json
import pika
import django
from sys import path
from os import environ

path.append('settings.py')
environ.setdefault('DJANGO_SETTINGS_MODULE', 'accounting.settings')
django.setup()

from accounting.models import ExternalUser, Task, AuditLog

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', heartbeat=600, blocked_connection_timeout=300))
channel = connection.channel()
channel.queue_declare(queue='accounts-stream')


def accounts_callback(ch, method, properties, body):
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


channel.basic_consume(queue='accounts-stream', on_message_callback=accounts_callback, auto_ack=True)
channel.start_consuming()


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', heartbeat=600, blocked_connection_timeout=300))
channel = connection.channel()
channel.queue_declare(queue='tasks-stream')


def tasks_callback(ch, method, properties, body):
    task_obj = json.loads(body)
    print(task_obj)
    try:
        if properties.content_type == 'task_created':
            task_obj['reporter'] = ExternalUser.objects.get(public_id=task_obj['reporter'])
            task_obj['assignee'] = ExternalUser.objects.get(public_id=task_obj['assignee']) if task_obj['assignee'] else None
            Task.objects.create(**task_obj)
        elif properties.content_type == 'task_updated':
            try:
                task = Task.objects.get(public_id=task_obj['public_id'])
                task.reporter = ExternalUser.objects.get(public_id=task_obj['reporter'])
                task.assignee = ExternalUser.objects.get(
                    public_id=task_obj['assignee']
                ) if task_obj['assignee'] else None
                task.description = task_obj['description']
                task.title = task_obj['title']
                task.jira_id = task_obj['jira_id']
                task.status = task_obj['status']
                task.save()
            except Task.DoesNotExist:
                Task.objects.create(**task_obj)
        elif properties.content_type == 'task_deleted':
            try:
                Task.objects.get(public_id=task_obj['public_id']).delete()
            except Task.DoesNotExist:
                pass
        elif properties.content_type == 'task_status_changed':
            try:
                task = Task.objects.get(public_id=task_obj['public_id'])
                task.status = task_obj['status']
                task.save()
            except Task.DoesNotExist:
                return
            if task.status == Task.STATUS_ASSIGNED:
                assignee = task.assignee
                assignee.balance += task.assign_cost
                assignee.save()
                AuditLog.objects.create(
                    amount=task.assign_cost,
                    user=assignee,
                    description=f"{task.title} assigned #{task.puplic_id}",
                )
            elif task.status == Task.STATUS_COMPLETED:
                assignee = task.assignee
                assignee.balance += task.complete_cost
                assignee.save()
                AuditLog.objects.create(
                    amount=task.complete_cost,
                    user=assignee,
                    description=f"{task.title} completed #{task.puplic_id}",
                )
    except KeyError:
        print('Incorrect task message.')


channel.basic_consume(queue='tasks-stream', on_message_callback=tasks_callback, auto_ack=True)
channel.start_consuming()
