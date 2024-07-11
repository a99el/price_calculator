from django.shortcuts import render
from .models import Offer
from django.db.models import Sum


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
