from django.contrib import admin
from crawler import models

class ItemAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Item, ItemAdmin)
