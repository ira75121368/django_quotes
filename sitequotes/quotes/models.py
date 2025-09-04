from django.core.exceptions import ValidationError
from django.db import models
import re


class Categories(models.Model):
    name = models.CharField(max_length=255, db_index=True, verbose_name='Название категории')

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


def normalized_text(text: str) -> str:
    """ Приводит цитату в определенное состояние для исключения от дубликатов """
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).split()
    return text


class Source(models.Model):
    name = models.CharField(max_length=255, db_index=True, verbose_name='Название источника')
    category = models.ForeignKey(Categories, on_delete=models.PROTECT, verbose_name='Категория')

    class Meta:
        verbose_name = "Источник"
        verbose_name_plural = "Источники"

    def __str__(self):
        return f'{self.name} - {self.category.name}'


class Quotes(models.Model):
    text_quotes = models.TextField(unique=True, verbose_name='Цитата')
    normalize_text = models.TextField(unique=True, editable=False)
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    weight = models.IntegerField(default=1, verbose_name='Вес')
    likes = models.PositiveIntegerField(default=0, verbose_name='Лайки')
    dislikes = models.PositiveIntegerField(default=0, verbose_name='Дизлайки')
    views = models.PositiveIntegerField(default=0, verbose_name='Просмотры')
    source = models.ForeignKey(Source, on_delete=models.PROTECT, null=False, verbose_name='Источник')

    class Meta:
        verbose_name = "Цитата"
        verbose_name_plural = "Цитаты"

    def __str__(self):
        return self.text_quotes

    def clean(self):
        """ Проверка на уникальность + 'не более трёх' """
        self.normalize_text = normalized_text(self.text_quotes)

        if self.source and self.source.quotes_set.count() >= 3:
            raise ValidationError('У этого источника уже есть 3 цитаты')

    def validate_unique(self, exclude=None):
        super().validate_unique(exclude)
        if Quotes.objects.exclude(pk=self.pk).filter(normalize_text=self.normalize_text).exists():
            raise ValidationError({"text_quotes": "Такая цитата уже существует."})


    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
