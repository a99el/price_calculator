from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .forms import LoginForm
from .models import Offer
from django.db.models import Sum
from django.urls import reverse

def home_view(request):
    return render(request, 'pricing/home.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_staff:  # Check if the user is an admin
                    return redirect('admin_dashboard')
                else:
                    return redirect('offer_detail')
            else:
                # Invalid login
                return render(request, 'pricing/login.html', {'error': 'Invalid username or password'})
    else:
        form = LoginForm()
    return render(request, 'pricing/login.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    def admin_dashboard(request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            User.objects.create_user(username=username, password=password)
            return redirect('admin_dashboard')
    return render(request, 'pricing/admin_dashboard.html')

@login_required
@user_passes_test(lambda u: u.is_staff)
def add_user_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        User.objects.create_user(username=username, password=password)
        return redirect('admin_dashboard')
    return redirect('admin_dashboard')

@login_required
def offer_detail_view(request):
    try:
        offer = Offer.objects.get(pk=1)  # Replace with your logic to fetch the offer
        total_price = offer.offerdetail_set.aggregate(total=Sum('total_price'))['total']
    except Offer.DoesNotExist:
        offer = None
        total_price = 0

    context = {
        'offer': offer,
        'total_price': total_price,
    }
    return render(request, 'pricing/offer_detail.html', context)


def index(request):
    try:
        offer = Offer.objects.get(pk=1)  # Replace with your logic to fetch the offer
        total_price = offer.offerdetail_set.aggregate(total=Sum('total_price'))['total']
    except Offer.DoesNotExist:
        offer = None
        total_price = 0

    context = {
        'offer': offer,
        'total_price': total_price,
    }
    return render(request, 'pricing/offer_detail.html', context)
