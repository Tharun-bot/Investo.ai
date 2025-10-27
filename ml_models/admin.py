from django.contrib import admin
from .models import MLModel, Prediction

@admin.register(MLModel)
class MLModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'version', 'accuracy', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'prediction', 'confidence', 'model', 'created_at']
    list_filter = ['prediction', 'created_at']
    search_fields = ['symbol']
