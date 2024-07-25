from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .forms import LoginForm, OfferDetailForm, ServiceForm, OfferForm
from .models import Offer, OfferDetail, Service
from django.db.models import Sum
from django.urls import reverse
from django.http import HttpResponse
from io import BytesIO
from datetime import datetime
from django.utils import timezone

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
                    return redirect('pricing:admin_dashboard')
                else:
                    return redirect('pricing:offer_detail')
            else:
                # Invalid login
                return render(request, 'pricing/login.html', {'error': 'Invalid username or password'})
    else:
        form = LoginForm()
    return render(request, 'pricing/login.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    if request.method == 'POST':
        if 'username' in request.POST and 'password' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            User.objects.create_user(username=username, password=password)
        else:
            # Logic for updating statements
            statement_1 = request.POST.get('statement_1')
            statement_2 = request.POST.get('statement_2')
            statement_3 = request.POST.get('statement_3')
            offer = Offer.objects.first()
            offer.statement_1 = statement_1
            offer.statement_2 = statement_2
            offer.statement_3 = statement_3
            offer.save()
        return redirect('pricing:admin_dashboard')

    users = User.objects.exclude(is_staff=True)  # Exclude admin users
    offer = Offer.objects.first()
    return render(request, 'pricing/admin_dashboard.html', {
        'users': users,
        'statement_1': offer.statement_1,
        'statement_2': offer.statement_2,
        'statement_3': offer.statement_3,
    })

@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_user_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if not user.is_staff:  # Ensure we don't delete admin users
        user.delete()
    return redirect('pricing:admin_dashboard')

@login_required
@user_passes_test(lambda u: u.is_staff)
def add_user_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        User.objects.create_user(username=username, password=password)
        return redirect('pricing:admin_dashboard')
    return redirect('pricing:admin_dashboard')

@login_required
@user_passes_test(lambda u: u.is_staff)
def update_statement(request):
    if request.method == 'POST':
        statement_1 = request.POST.get('statement_1')
        statement_2 = request.POST.get('statement_2')
        statement_3 = request.POST.get('statement_3')
        offer = Offer.objects.first()
        offer.statement_1 = statement_1
        offer.statement_2 = statement_2
        offer.statement_3 = statement_3
        offer.save()
        return redirect('pricing:admin_dashboard')
    return render(request, 'pricing/update_statement.html')

@login_required
def offer_detail_view(request):
    offer_form = OfferForm()
    offer = Offer.objects.first()
    offer_details = offer.offerdetail_set.all() if offer else []
    total_price = offer.offerdetail_set.aggregate(total=Sum('total_price'))['total'] if offer else 0
    current_date = timezone.now().strftime('%Y-%m-%d')

    context = {
        'offer': offer,
        'offer_details': offer_details,
        'offer_form': offer_form,
        'total_price': total_price,
        'current_date': current_date,
        'statement_1': offer.statement_1 if offer else '',
        'statement_2': offer.statement_2 if offer else '',
        'statement_3': offer.statement_3 if offer else '',
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