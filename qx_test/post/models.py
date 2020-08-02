from django.db import models

# Create your models here.


class Category(models.Model):

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = verbose_name


class Post(models.Model):

    name = models.CharField(
        verbose_name="Name", max_length=150)
    user = models.CharField(
        verbose_name="User Name", max_length=150)
    category = models.ForeignKey(
        Category, verbose_name="Category", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = verbose_name
