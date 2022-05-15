from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    reporter_str = forms.CharField(label='Reporter email', disabled=True, required=False)
    status_str = forms.CharField(label='Status', disabled=True, required=False)

    class Meta:
        model = Task
        fields = ['reporter_str', 'reporter', 'status_str', 'title', 'description']
        widgets = {
            'reporter':  forms.HiddenInput(),
        }

    @classmethod
    def status_default_str(cls):
        return str(cls._meta.model._meta.get_field('status').default)
