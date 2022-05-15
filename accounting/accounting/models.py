import uuid
import random
from django.db import models


class ExternalUser(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, blank=True, editable=False)
    full_name = models.CharField(max_length=255, blank=True, editable=False)
    email = models.EmailField(max_length=255, blank=True, editable=False)
    role = models.CharField(max_length=32, blank=True, editable=False)
    balance = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name


def assign_cost():
    return random.randrange(-20, -10)


def complete_cost():
    return random.randrange(20, 40)


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
    jira_id = models.CharField(null=True, max_length=64)
    description = models.TextField()
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=STATUS_NEW)
    assign_cost = models.SmallIntegerField(default=assign_cost)
    complete_cost = models.SmallIntegerField(default=complete_cost)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'#{self.id}: {self.status}'


class AuditLog(models.Model):
    amount = models.SmallIntegerField()
    user = models.ForeignKey(ExternalUser, on_delete=models.CASCADE, related_name='audit_logs')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'#{self.user.email}: {self.amount}'
