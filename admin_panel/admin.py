from import_export.admin import ImportExportModelAdmin
from django.contrib import admin


from .models import AdminUser, FakeAddress, Product
admin.site.register(AdminUser)
admin.site.register(Product)
admin.site.register(FakeAddress, ImportExportModelAdmin)

