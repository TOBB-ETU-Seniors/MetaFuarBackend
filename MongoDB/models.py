from django.db import models

# Create your models here.


class Account(models.Model):
    _id = models.AutoField(primary_key=True)
    mail_address = models.EmailField()
    login_type = models.CharField(max_length=20)
    creation_date = models.DateTimeField()