from django.contrib import admin
from .models import jurisdiction

# Register your models here.
@admin.register(jurisdiction)
class jurisdiction_Admin(admin.ModelAdmin):
	list_display=('account','status',)