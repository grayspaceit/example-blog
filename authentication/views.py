from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View, UpdateView, DetailView, TemplateView
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.auth import views as auth_views

#custom classes and modules
from authentication.forms import SignUpForm, ProfileForm
from authentication.tokens import account_activation_token

from . forms import *
from . models import *

class HomePage(TemplateView):
    template_name = 'index.html'


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'


"""
############   account activation using email   ########
"""
# Sign Up View
class SignUpView(View):
    form_class = SignUpForm
    template_name = 'accounts/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        current_site = get_current_site(request)
        print(current_site)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = False # Deactivate account till it is confirmed
            user.save()

            current_site = get_current_site(request)
            print(current_site)
            subject = 'Activate Your Example Blog Account'
            message = render_to_string('emails/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            messages.success(request, ('Please Confirm your email to complete registration.'))

            return redirect('login')

        return render(request, self.template_name, {'form': form})


from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from authentication.tokens import account_activation_token
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.email_confirmed = True
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, ('Your account have been confirmed.'))
            return render(request, "accounts/profile.html", context={'pk':uid})
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('index')


from django.contrib.auth.mixins import LoginRequiredMixin

class UserProfile(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'accounts/profile.html'


# Edit Profile View
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'auth/login/'
    redirect_field_name ="/"
    model = CustomUser
    form_class = ProfileForm
    template_name = 'accounts/profile_update_form.html'
