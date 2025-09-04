from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=255, db_index=True, verbose_name='Название категории')

    def __str__(self):
        return self.name


class Source(models.Model):
    name = models.CharField(max_length=255, db_index=True, verbose_name='Название источника')
    category = models.ForeignKey(Categories, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.name} - {self.category.name}'


class Quetes(models.Model):
    text_quotes = models.TextField(unique=True)
    time_created = models.DateTimeField(auto_now_add=True)
    weight = models.IntegerField(default=1)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    source = models.ForeignKey(Source, on_delete=models.PROTECT)

    def __str__(self):
        return self.text_quotes
