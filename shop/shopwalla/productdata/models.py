from django.db import models



class PRODUCTADD(models.Model):
      idsss=models.CharField(max_length=15)
      name=models.CharField(max_length=75)
      img1=models.FileField(upload_to='databook/')
      img2=models.FileField(upload_to='databook/')
      img3=models.FileField(upload_to='databook/')
      descriptions=models.CharField(max_length=500)
      cutprice=models.CharField(max_length=10)
      price=models.DecimalField(max_digits=10,decimal_places=2)
# Create your models here.
