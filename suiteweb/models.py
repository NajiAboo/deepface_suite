from django.db import models

# Create your models here.

class ExampleModel(models.Model):
    model_pic = models.ImageField(upload_to = 'pic_folder/', default = 'pic_folder/None/no-img.jpg')
    