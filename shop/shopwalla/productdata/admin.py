from django.contrib import admin
from productdata.models import PRODUCTADD



class ADMINPANEL(admin.ModelAdmin):
    list_display=('idsss','name','img1','img2','img3','descriptions','cutprice','price')

admin.site.register(PRODUCTADD,ADMINPANEL)


# Register your models here.
