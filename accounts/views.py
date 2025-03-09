from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.views.generic import FormView
from .forms import CustomUserForm
# Create your views here.


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('articles:all-articles')


class CustomLogoutView(LogoutView):
    next_page = 'accounts:login'


class CustomRegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = CustomUserForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('articles:all-articles')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
            return super(CustomRegisterView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('articles:all-articles')
        return super(CustomRegisterView, self).get(*args, **kwargs)
