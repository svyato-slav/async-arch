from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def logged_in(request):
    context = {}
    return render(request, 'authentication/logged_in.html', context)
