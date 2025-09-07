import random

from django.db.models import F
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Sum, Count

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
    sort = request.GET.get('sort', 'likes')

    if sort == 'likes':
        quotes = Quotes.objects.order_by('-likes')[:10]
        title = "Топ по лайкам"
    elif sort == 'dislikes':
        quotes = Quotes.objects.order_by('-dislikes')[:10]
        title = "Топ по дизлайкам"
    else:
        quotes = Quotes.objects.order_by('-views')[:10]
        title = "Топ по просмотрам"

    return render(request, 'quotes/top.html', {'quotes': quotes, 'title': title})


def dashboard(request):
    total_quotes = Quotes.objects.count()
    total_likes = Quotes.objects.aggregate(Sum("likes"))["likes__sum"] or 0
    total_dislikes = Quotes.objects.aggregate(Sum("dislikes"))["dislikes__sum"] or 0
    total_views = Quotes.objects.aggregate(Sum("views"))["views__sum"] or 0

    # топ по лайкам
    top_quote = Quotes.objects.order_by("-likes").first()

    context = {
        "total_quotes": total_quotes,
        "total_likes": total_likes,
        "total_dislikes": total_dislikes,
        "total_views": total_views,
        "top_quote": top_quote,
    }
    return render(request, 'quotes/dashboard.html', context)
