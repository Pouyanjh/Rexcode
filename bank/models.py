from django.db import models
from user.models import user


class Order(models.Model):
    title = models.CharField(max_length=200, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)
    user = models.CharField(max_length=100, blank=True)
    paymentmethod = models.CharField(max_length=200, blank=True)
    totalprice = models.IntegerField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(auto_now=True)
    isDelivered = models.BooleanField(default=False)
    deliveredat = models.DateTimeField(auto_now=True)
    createdat = models.DateTimeField(auto_now=True)



class zibal(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    user = models.ForeignKey(user, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    transId = models.CharField(max_length=100, unique=True)
    lastStatus = models.IntegerField(blank=True, null=True)
    amountPaid = models.IntegerField(blank=True, null=True)
    datepaid = models.DateTimeField(auto_now_add=True)
    cardNo = models.CharField(max_length=30, blank=True, null=True)
    Condition = models.CharField(max_length=200, blank=True)


    def __str__(self):
        return str(self.transId)