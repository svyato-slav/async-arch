def current_oauth_user(request):
    return {
        'current_oauth_user': request.session['user'],
    }
