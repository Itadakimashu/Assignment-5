from django.shortcuts import render
from django.views.generic import FormView
from .forms import UserRegistrationForm,UserUpdateForm
from django.contrib.auth import login, logout,update_session_auth_hash
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.views import View
from django.shortcuts import redirect

from transactions.views import transaction_email

class UserRegistrationView(FormView):
    template_name = 'accounts/user_registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('profile')
    
    def form_valid(self,form):
        print(form.cleaned_data)
        user = form.save()
        login(self.request, user)
        print(user)
        return super().form_valid(form) # form_valid function call hobe jodi sob thik thake
    

class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    def get_success_url(self):
        return reverse_lazy('home')

class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('home')


class UserBankAccountUpdateView(View):
    template_name = 'accounts/profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the user's profile page
        return render(request, self.template_name, {'form': form})
    

class UserChangePasswordView(PasswordChangeView):
    template_name = 'accounts/change_password.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('home')


    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        transaction_email(self.request.user,'Password Changed Email',0,'accounts/password_change_email.html')
        return super().form_valid(form)

    
    
    