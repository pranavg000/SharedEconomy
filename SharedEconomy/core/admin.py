from django.contrib import admin
from .models import Buyer,Traveller,Product,ProductBuyer


admin.site.register(Buyer)
admin.site.register(Traveller)
admin.site.register(Product)
admin.site.register(ProductBuyer)