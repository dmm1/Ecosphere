from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import translation
from django.utils.translation import gettext as _

def set_language(request):
    lang_code = request.GET.get('lang')
    if lang_code:
        translation.activate(lang_code)
        request.session[translation.LANGUAGE_SESSION_KEY] = lang_code
        return redirect('/')
    else:
        return redirect('/')

def index(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['user_id'] = user.id  # Manually create a session
            return redirect('/user/dashboard/')
        else:
            return HttpResponse(_('Invalid login credentials'))
    elif request.user.is_authenticated:
        return redirect('/user/dashboard/')
    return render(request, 'home/index.html')
def logout_view(request):
    logout(request)
    return redirect('/')
@login_required
def dashboard(request):
    return render(request, 'user/dashboard.html')

@login_required
def admin_view(request):
    return render(request, 'admin/index.html')