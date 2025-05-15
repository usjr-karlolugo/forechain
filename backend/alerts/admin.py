from django.contrib import admin
from .models import Alert


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ("title", "sentiment", "created_at")
    search_fields = ("title", "sentiment")
    list_filter = ("sentiment",)
