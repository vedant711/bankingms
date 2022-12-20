from django.db import models

# Create your models here.

TRANSACTION_TYPE = (
    ('CREDIT','CREDIT'),
    ('DEBIT','DEBIT')
)

class User(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=80)
    password = models.CharField(max_length=80)
    balance = models.DecimalField(decimal_places=2,max_digits=20)
    pin = models.IntegerField()

class Transactions(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=80, choices=TRANSACTION_TYPE)
    amount = models.DecimalField(decimal_places=2,max_digits=20)
    balance = models.DecimalField(decimal_places=2,max_digits=20)