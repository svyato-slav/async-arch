import uuid
from django.db import models

from . import producer


class ExternalUser(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, blank=True, editable=False)
    full_name = models.CharField(max_length=255, blank=True, editable=False)
    email = models.EmailField(max_length=255, blank=True, editable=False)
    role = models.CharField(max_length=32, blank=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name


class Task(models.Model):
    STATUS_NEW = 'new'
    STATUS_ASSIGNED = 'assigned'
    STATUS_COMPLETED = 'completed'
    STATUS_CHOICES = (
        (STATUS_NEW, 'New'),
        (STATUS_ASSIGNED, 'Assigned'),
        (STATUS_COMPLETED, 'Completed'),
    )
    public_id = models.UUIDField(default=uuid.uuid4, editable=False)
    reporter = models.ForeignKey(ExternalUser, on_delete=models.CASCADE, related_name='tasks_reported')
    assignee = models.ForeignKey(ExternalUser, on_delete=models.CASCADE, related_name='tasks_assigned', null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=STATUS_NEW)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __init__(self, *args, **kwargs):
        super(Task, self).__init__(*args, **kwargs)
        self.__original_status = self.status

    def __str__(self):
        return f'#{self.id}: {self.status}'

    @classmethod
    def reassign_tasks(cls):
        queryset = cls.objects.filter(status__in=[cls.STATUS_ASSIGNED, cls.STATUS_NEW])
        for task in queryset:
            task.assignee = ExternalUser.objects.filter(role='developer').order_by('?').first()
            task.status = Task.STATUS_ASSIGNED
            task.save()

    def save(self, *args, **kwargs):
        if not self.id:
            event_data = {
                'public_id': str(self.public_id),
                'reporter': str(self.reporter.public_id),
                'assignee': str(self.assignee.public_id) if self.assignee else None,
                'description': self.description,
                'status': self.status
            }
            producer.publish('task_created', event_data)
        else:
            event_data = {
                'public_id': str(self.public_id),
                'reporter': str(self.reporter.public_id),
                'assignee': str(self.assignee.public_id) if self.assignee else None,
                'description': self.description,
                'status': self.status
            }
            producer.publish('task_updated', event_data)
        super(Task, self).save(*args, **kwargs)
        if self.status != self.__original_status:
            event_data = {
                'public_id': str(self.public_id),
                'new_status': self.status,
                'original_status': self.__original_status
            }
            producer.publish('task_status_changed', event_data)

    def delete(self, *args, **kwargs):
        super(Task, self).delete(*args, **kwargs)
        event_data = {
            'public_id': str(self.public_id)
        }
        producer.publish('task_deleted', event_data)
