from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Offer(models.Model):
    client_name = models.CharField(max_length=100)
    client_address = models.CharField(max_length=200)
    date = models.DateField()

    def __str__(self):
        return self.client_name

class OfferDetail(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total_price = self.service.price * self.quantity
        super().save(*args, **kwargs)
