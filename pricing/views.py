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
from xhtml2pdf import pisa

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
                    return redirect('offer_form')
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
        username = request.POST['username']
        password = request.POST['password']
        User.objects.create_user(username=username, password=password)
        return redirect('admin_dashboard')

    users = User.objects.exclude(is_staff=True)  # Exclude admin users
    return render(request, 'pricing/admin_dashboard.html', {'users': users})


@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_user_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if not user.is_staff:  # Ensure we don't delete admin users
        user.delete()
    return redirect('admin_dashboard')

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


@login_required
def offer_form_view(request):
    if request.method == 'POST':
        offer_form = OfferForm(request.POST)
        service_form = ServiceForm(request.POST)
        offer_detail_form = OfferDetailForm(request.POST)

        if offer_form.is_valid() and service_form.is_valid() and offer_detail_form.is_valid():
            offer = offer_form.save()
            service = service_form.save()
            offer_detail = offer_detail_form.save(commit=False)
            offer_detail.offer = offer
            offer_detail.service = service
            offer_detail.save()
            return redirect('offer_detail')
    else:
        offer_form = OfferForm()
        service_form = ServiceForm()
        offer_detail_form = OfferDetailForm()

    return render(request, 'pricing/offer_form.html', {
        'offer_form': offer_form,
        'service_form': service_form,
        'offer_detail_form': offer_detail_form,
    })


@login_required
def generate_pdf_view(request):
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

    html = render_to_string('pricing/offer_detail_pdf.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="offer.pdf"'
    pisa.CreatePDF(BytesIO(html.encode('utf-8')), dest=response)
    return response



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
