from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse



# Auth
def redirect_if_logged_in(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home'))  
        return view_func(request, *args, **kwargs)
    return _wrapped_view
