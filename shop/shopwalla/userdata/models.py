from django.db import models


class USERDATA(models.Model):
    name=models.CharField(max_length=50)
    pincode=models.CharField(max_length=50)
    country=models.CharField(max_length=50,default='india')
    state=models.CharField(max_length=50)
    address=models.CharField(max_length=50)
    phone=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    amount=models.CharField(max_length=50)
    idno=models.CharField(max_length=50)

    

# Create your models here.
