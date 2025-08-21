from django.contrib import admin
from userdata.models import USERDATA
# Register your models here.
class SHOWADMIN(admin.ModelAdmin):
    list_display=('name','phone','address','amount','country','state','pincode','city','idno')

admin.site.register(USERDATA,SHOWADMIN)