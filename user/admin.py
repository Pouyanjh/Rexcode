from django.contrib import admin
from .models import user

@admin.register(user)

class useradmin(admin.ModelAdmin):
  list_display = ['email', 'id', 'username']
  search_fields = ['id']
