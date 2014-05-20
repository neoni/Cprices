from django.contrib import admin
from accounts import models


class ClientIdAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.ClientId, ClientIdAdmin)

