from todoApp.models import Todo
from django.contrib import admin

# Register your models here.
class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ("created",)

admin.site.register(Todo,TodoAdmin)