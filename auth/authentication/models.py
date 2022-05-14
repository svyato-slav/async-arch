import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from . import producer


class User(AbstractUser):
    ROLE_ADMIN = 'admin'
    ROLE_MANAGER = 'manager'
    ROLE_HEAD = 'head'
    ROLE_DEVELOPER = 'developer'
    ROLE_CHOICES = (
        (ROLE_ADMIN, 'Administrator'),
        (ROLE_HEAD, 'Head'),
        (ROLE_MANAGER, 'Manager'),
        (ROLE_DEVELOPER, 'Developer'),
    )
    public_id = models.UUIDField(default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=32, choices=ROLE_CHOICES)

    __original_role = None

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.__original_role = self.role

    def save(self, *args, **kwargs):
        if not self.id:
            event_data = {
                'public_id': str(self.public_id),
                'username': str(self.username),
                'email': self.email,
                'full_name': self.get_full_name(),
                'role': self.role
            }
            producer.publish('account_created', event_data)
        else:
            event_data = {
                'public_id': str(self.public_id),
                'username': str(self.username),
                'email': self.email,
                'full_name': self.get_full_name(),
                'role': self.role
            }
            producer.publish('account_updated', event_data)
        super(User, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super(User, self).delete(*args, **kwargs)
        event_data = {
            'public_id': str(self.public_id)
        }
        producer.publish('account_deleted', event_data)
