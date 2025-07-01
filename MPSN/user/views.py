from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import View
from django.urls import reverse_lazy
from .form import *
from django.views.generic import FormView, CreateView

@login_required(redirect_field_name='regstration/login.html')
def profile(request):
    return render(request,'profile/index.html')


class RegisterView(FormView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy("user:profile")
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)