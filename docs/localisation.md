In your views, use django.utils.translation.activate() to switch to the desired language.

templates:
<!-- templates/home/index.html -->
{% load i18n %}
<form method="post">
    <div class="form-group">
        <input type="text" name="username" class="form-control" placeholder="{% trans 'Username' %}" required>
    </div>
    <div class="form-group">
        <input type="password" name="password" class="form-control" placeholder="{% trans 'Password' %}" required>
    </div>
    <button type="submit" class="btn btn-primary btn-block">{% trans 'Log In' %}</button>
</form>


python code:
from django.utils.translation import gettext as _
message = _("Hello, world!")

from django.utils.translation import gettext as _

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


Create message files using Django's makemessages command. 
This command will create a .po file for each language in the LOCALE_PATHS directory.

python manage.py makemessages -l de

Translate the messages in the .po files.  

Compile the message files using Django's compilemessages command. 
This command will create a .mo file for each .po file.

python manage.py compilemessages

Troubleshooting Windows:

The error message you're seeing indicates that Django's makemessages command can't find the msguniq program, which is part of the GNU gettext tools. This program is used to generate unique translation strings.  To resolve this issue, you need to install GNU gettext tools on your system. Here's how you can do it:  
Download the latest version of gettext from the GNU gettext website.  
Extract the downloaded file to a directory, for example, C:\gettext.  
Add the bin directory of the extracted gettext directory to your system's PATH environment variable. If you extracted gettext to C:\gettext, you would add C:\gettext\bin to your PATH.  
Restart your command prompt to apply the changes.  
After following these steps, the makemessages command should be able to find msguniq and other gettext tools, and it should work as expected