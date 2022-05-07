from django.contrib import admin

from .models import Task, ExternalUser


class TaskAdmin(admin.ModelAdmin):
    list_display = ('public_id', 'title', 'status', )
    readonly_fields = ('public_id', )
    list_filter = ('status', )


class ExternalUserAdmin(admin.ModelAdmin):
    list_display = ('public_id', 'email', 'username', 'full_name', 'role')
    readonly_fields = ('public_id', 'email', 'username', 'full_name', 'role')


admin.site.register(Task, TaskAdmin)
admin.site.register(ExternalUser, ExternalUserAdmin)
