from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)


class CategoryChildren(models.Model):
    category_name = models.ForeignKey(Category, on_delete=models.CASCADE)
    category_children = models.ManyToManyField(Category, related_name='children')
