from django.contrib import admin
from . models import Task,Priority,Category
# Register your models here.
admin.site.register(Task)
admin.site.register(Priority)
admin.site.register(Category)