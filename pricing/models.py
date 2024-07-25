from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def _str_(self):
        return self.name

class Offer(models.Model):
    client_name = models.CharField(max_length=100)
    client_address = models.CharField(max_length=200)
    date = models.DateField()
    statement_1 = models.TextField(default='', blank=True)
    statement_2 = models.TextField(default='', blank=True)
    statement_3 = models.TextField(default='', blank=True)

    def _str_(self):
        return self.client_name

class OfferDetail(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, default=1)  # تعيين 1 كقيمة افتراضية
    service = models.ForeignKey(Service, on_delete=models.CASCADE, default=1)  # تعيين 1 كقيمة افتراضية
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total_price = self.service.price * self.quantity
        super().save(*args, **kwargs)