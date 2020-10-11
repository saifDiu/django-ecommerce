from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.
class customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=100, null=True)

    def __str__(self):
        return self.name


class product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True,blank=True)
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    @ property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url



class order(models.Model):
    customer = models.ForeignKey(customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_order = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    complete = models.BooleanField(default=False, null=True, blank = True)
    transaction_id = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.id)

    @ property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems ])
        return total


    @ property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems ])
        return total


class orderitem(models.Model):
    product = models.ForeignKey(product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)

    @ property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class shippingaddress(models.Model):
    customer = models.ForeignKey(customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_shipped = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return self.address
