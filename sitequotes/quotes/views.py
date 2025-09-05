import random
from django.shortcuts import render
from .models import Quotes


def index(request):
	quotes = list(Quotes.objects.all())

	weights = [q.weight for q in quotes]
	quote = random.choices(quotes, weights=weights, k=1)[0]

	quote.increment_views()

	return render(request, 'quotes/index.html', {"quote": quote})

def top(request):
	return render(request, 'quotes/top.html')
# Create your views here.
