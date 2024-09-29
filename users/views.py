from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth import login

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('')  # Перенаправление на страницу профиля
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})