from django.contrib import admin
from .models import customer,Product,Orders,materials,analytics
# Register your models here.

class customerAdmin(admin.ModelAdmin):
    pass
admin.site.register(customer,customerAdmin)

class productAdmin(admin.ModelAdmin):
    pass
admin.site.register(Product,productAdmin)

class ordersAdmin(admin.ModelAdmin):
    pass
admin.site.register(Orders,ordersAdmin)

class materialsAdmin(admin.ModelAdmin):
    pass
admin.site.register(materials,materialsAdmin)

class analyticssAdmin(admin.ModelAdmin):
    pass
admin.site.register(analytics,analyticssAdmin)
    