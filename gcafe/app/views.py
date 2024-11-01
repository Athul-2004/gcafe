# cafe/views.py
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from .models import Customer, Game, System, Booking
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout



def index(request):
    games = Game.objects.all()
    context = {
        'games': games
    }
    return render(request,'index.html', context)

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Basic validation
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            auth_login(request, user) 
            return redirect('dashboard')  # Redirect to the dashboard

    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')

@login_required
def dashboard(request):
    # Fetch all systems and games
    systems = System.objects.all()
    games = Game.objects.all()

    # Organize data into a dictionary
    context = {
        'user': request.user,
        'systems': systems,
        'games': games
    }

    return render(request, 'dashboard.html', context)


def logout(request):
    logout(request)
    return redirect('login')


def create_booking(request):
    if request.method == 'POST':
        customer = Customer.objects.get(user=request.user)  # Assuming Customer is linked to User
        system_id = request.POST.get('system')
        game_id = request.POST.get('game')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        system = System.objects.get(id=system_id)
        game = Game.objects.get(id=game_id)

        # Create booking object
        booking = Booking(
            customer=customer,
            system=system,
            game=game,
            start_time=start_time,
            end_time=end_time
        )

        # Check if the system is available
        if booking.is_system_available():
            booking.save()
            messages.success(request, "Booking successfully created!")
            return redirect('dashboard')
        else:
            messages.error(request, "System is already booked for the selected time.")
            return redirect('create_booking')

    # If the request method is GET, show the booking form
    systems = System.objects.filter(is_available=True)  # Only show available systems
    games = Game.objects.all()

    return render(request, 'booking/create_booking.html', {'systems': systems, 'games': games})