from django.shortcuts import render, redirect
from .form import SignUpForm

# Create your views here.
def login(request):
    return render(request, 'accounts/login.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})