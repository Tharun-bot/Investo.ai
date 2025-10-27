from django.db import models

class MLModel(models.Model):
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=20)
    accuracy = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} v{self.version}"

class Prediction(models.Model):
    model = models.ForeignKey(MLModel, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10)
    prediction = models.CharField(max_length=10)
    confidence = models.FloatField()
    features_used = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
