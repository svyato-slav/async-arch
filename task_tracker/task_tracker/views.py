from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render
from django.views.generic.edit import CreateView
from .models import Task, ExternalUser
from .forms import TaskForm


def index(request):
    tasks = Task.objects.all()
    context = {
        'tasks': tasks
    }
    return render(request, 'tasks/index.html', context)


def add(request):
    return render(request, 'tasks/task_form.html', context)


class TaskFormView(CreateView):
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = '/tasks/'

    def get_initial(self):
        try:
            external_user = get_object_or_404(ExternalUser, public_id=self.request.session['user']['sub'])
        except KeyError:
            raise PermissionDenied
        return {
            'status_str': self.get_form_class().status_default_str(),
            'reporter_str': external_user.email,
            'reporter': external_user
        }


def detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    context = {
        'user': request.session['user'],
        'task': task
    }
    return render(request, 'tasks/detail.html', context)


def reassign_tasks(request):
    Task.reassign_tasks()
    return HttpResponseRedirect('/tasks/')
