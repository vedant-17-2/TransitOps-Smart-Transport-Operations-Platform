from django.db import models


class BaseModel(models.Model):
    """Abstract base model with automatic timestamps for all TransitOps models."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
