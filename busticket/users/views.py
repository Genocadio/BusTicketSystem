from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def home(request):
    return HttpResponse('<h1>Home</h1>')
def signup(request):
    if request.method == 'POST':
        form = signupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = signupForm()
    return render(request, 'signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = loginForm()
    return render(request, 'login.html', {'form': form})
