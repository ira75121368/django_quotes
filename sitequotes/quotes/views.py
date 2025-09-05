import random

from django.db.models import F
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect

from .models import Quotes


def index(request):
    quotes = list(Quotes.objects.all())

    weights = [q.weight for q in quotes]
    quote = random.choices(quotes, weights=weights, k=1)[0]

    quote.increment_views()

    return render(request, 'quotes/index.html', {"quote": quote})


def like_quote(request, pk):
    quote = get_object_or_404(Quotes, pk=pk)
    Quotes.objects.filter(pk=quote.pk).update(likes=F('likes') + 1)
    return (redirect('index'))


def dislike_quote(request, pk):
    quote = get_object_or_404(Quotes, pk=pk)
    Quotes.objects.filter(pk=quote.pk).update(dislikes=F('dislikes') + 1)
    return (redirect('index'))


def top(request):
    return render(request, 'quotes/top.html')
# Create your views here.
