from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def signup(request):
	if request.method == 'POST':
		if request.POST['password1'] == request.POST['password2']:
			# check to see if the username already exists
			try:
				User.objects.get(username=request.POST['username'])
				return render(request, 'accounts/signup.html', {'error': "Username has already been taken"})
			except User.DoesNotExist:
				user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
				login(request, user)
				return render(request, 'posts/home.html')
		else:
			return render(request, 'accounts/signup.html', {'error': "Passwords didn't match"})
	else:
		return render(request, 'accounts/signup.html')

def loginView(request):
	if request.method == 'POST':
		user = authenticate(username=request.POST['username'], password=request.POST['password'])
		if user is not None:
			login(request, user)
			# Check if there is a next parameter
			if 'next' in request.POST:
				return redirect(request.POST['next'])
        	# Redirect to a success page.
			return redirect('home')
		else:
			return render(request, 'accounts/login.html', {'error': "Username and Password didn't match"})
	else:
		return render(request, 'accounts/login.html')

def logoutView(request):
	if request.method == 'POST':
		logout(request)
		return redirect('home')