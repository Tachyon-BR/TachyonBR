from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.

class TextMD(models.Model):
    texto = RichTextField(blank=True, null=True)
    nombre = models.CharField(max_length=50)



